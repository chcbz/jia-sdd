set -eu
umask 077
test "$PIPELINE_ID" = 4403172
test "$CI_COMMIT_SHA" = 'a47d2ac684e11cea1d307741091cb123afd2ac75'
printf '%s\n' 'fba8d49564946f381a02b7aee0bdfaeab48091be7ca5eb871f7dc4ac2eeeff6b  /usr/local/sbin/cyf-web-flow-deploy' | sha256sum -c -
test ! -e '/home/isp/baks/cyf-web-1.16.2-20261016'
mkdir -m 700 '/home/isp/baks/cyf-web-1.16.2-20261016'
cp -p /home/isp/hosts/cyf/web/kit/index.html '/home/isp/baks/cyf-web-1.16.2-20261016/index.html'
if test -f /var/lib/cyf-web-flow/record.json; then cp -p /var/lib/cyf-web-flow/record.json '/home/isp/baks/cyf-web-1.16.2-20261016/record.json'; fi
sha256sum '/home/isp/baks/cyf-web-1.16.2-20261016/index.html' > '/home/isp/baks/cyf-web-1.16.2-20261016/index.sha256'
package="/var/lib/cyf-web-flow/downloads/$BUILD_NUMBER/package.tgz"
artifact_sha=$(sha256sum "$package" | cut -d ' ' -f 1)
/usr/local/sbin/cyf-web-flow-deploy "$PIPELINE_ID" "$BUILD_NUMBER" "$CI_COMMIT_SHA" '1.16.2' "$artifact_sha"
