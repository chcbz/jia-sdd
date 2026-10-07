#!/usr/bin/env bash
set -euo pipefail
umask 077
run=/tmp/cyf-aam-resume-20261007
[ ! -e "$run" ] || { echo 'Fresh task directory required'; exit 2; }
mkdir -p "$run/evidence" "$run/control"
exec > >(tee "$run/evidence/server-run.log") 2>&1
printf 'START %s\n' "$(date -Iseconds)"
root_sha="$1"; api_sha="$2"; web_sha="$3"; client_sha="$4"
for value in "$root_sha" "$api_sha" "$web_sha" "$client_sha"; do [[ "$value" =~ ^[a-f0-9]{40}$ ]] || exit 2; done
clone_exact() {
 local from="$1" to="$2" url="$3" branch="$4" sha="$5"
 git clone --shared --no-checkout "$from" "$to"
 git -C "$to" remote set-url origin "$url"
 git -C "$to" fetch --no-tags origin "refs/heads/$branch:refs/remotes/origin/$branch"
 [ "$(git -C "$to" rev-parse "refs/remotes/origin/$branch")" = "$sha" ]
 git -C "$to" checkout --detach "$sha"
 [ "$(git -C "$to" rev-parse HEAD)" = "$sha" ]
 [ -z "$(git -C "$to" status --porcelain)" ]
 printf 'CHECKOUT %s %s %s\n' "$to" "$sha" "$(git -C "$to" rev-parse HEAD^{tree})"
}
clone_exact /home/isp/wsps/cyf "$run/root" https://gitee.com/chcbz/jia-sdd.git codex/archive-agent-maintenance "$root_sha"
clone_exact /home/isp/wsps/cyf/api "$run/root/api" https://gitee.com/chcbz/jia.git codex/archive-agent-maintenance-api "$api_sha"
clone_exact /home/isp/wsps/cyf/web "$run/root/web" https://gitee.com/chcbz/cyf-web-kit.git codex/archive-agent-maintenance-web "$web_sha"
clone_exact /home/isp/wsps/chcbz/isp-install "$run/isp-install" https://gitee.com/chcbz/isp-install.git codex/archive-agent-maintenance-client "$client_sha"
python3 - <<'PY'
import socket
s=socket.socket(); s.bind(('127.0.0.1',34061)); s.close()
PY
mkdir "$run/mysql-data"
/usr/sbin/mysqld --no-defaults --initialize-insecure --user=root --datadir="$run/mysql-data" > "$run/evidence/mysql-initialize.log" 2>&1
/usr/sbin/mysqld --no-defaults --user=root --datadir="$run/mysql-data" --socket="$run/mysql.sock" --pid-file="$run/mysql.pid" --log-error="$run/evidence/mysql-server.log" --bind-address=127.0.0.1 --port=34061 --mysqlx=0 --skip-log-bin --innodb-buffer-pool-size=128M --max-connections=60 &
mysql_pid=$!
cleanup_mysql() {
 if [ -r "/proc/$mysql_pid/cmdline" ] && tr '\0' ' ' < "/proc/$mysql_pid/cmdline" | grep -F -- "--datadir=$run/mysql-data" >/dev/null; then
   mysqladmin --no-defaults --socket="$run/mysql.sock" -u root shutdown || true
   wait "$mysql_pid" || true
 fi
}
trap cleanup_mysql EXIT
until mysqladmin --no-defaults --socket="$run/mysql.sock" -u root ping >/dev/null 2>&1; do
 kill -0 "$mysql_pid"; sleep 1
 done
password=$(python3 -c 'import secrets; print(secrets.token_hex(24))')
mysql --no-defaults --socket="$run/mysql.sock" -u root <<SQL
CREATE DATABASE cyf_h02_aam_resume_20261007;
CREATE DATABASE cyf_h03_aam_resume_20261007;
CREATE DATABASE cyf_h05a_aam_resume_20261007;
CREATE DATABASE aam_runtime_schema_test;
CREATE USER 'aam_dev'@'127.0.0.1' IDENTIFIED BY '$password';
GRANT ALL ON cyf_h02_aam_resume_20261007.* TO 'aam_dev'@'127.0.0.1';
GRANT ALL ON cyf_h03_aam_resume_20261007.* TO 'aam_dev'@'127.0.0.1';
GRANT ALL ON cyf_h05a_aam_resume_20261007.* TO 'aam_dev'@'127.0.0.1';
GRANT ALL ON aam_runtime_schema_test.* TO 'aam_dev'@'127.0.0.1';
SELECT @@port, @@datadir, @@server_uuid, @@log_bin;
SQL
for lane in H02 H03 H05A; do
 db=$(echo "$lane" | tr '[:upper:]' '[:lower:]')
 export "CYF_${lane}_MYSQL_ISOLATED=true" "CYF_${lane}_MYSQL_URL=jdbc:mysql://127.0.0.1:34061/cyf_${db}_aam_resume_20261007" "CYF_${lane}_MYSQL_DATABASE_CONFIRM=cyf_${db}_aam_resume_20261007" "CYF_${lane}_MYSQL_USER=aam_dev" "CYF_${lane}_MYSQL_PASSWORD=$password"
done
export CYF_AAM_SCHEMA_TEST_MYSQL_URL=jdbc:mysql://127.0.0.1:34061/aam_runtime_schema_test CYF_AAM_SCHEMA_TEST_MYSQL_USER=aam_dev CYF_AAM_SCHEMA_TEST_MYSQL_PASSWORD="$password"
export JAVA_HOME=/home/isp/apps/jdk21 PATH=/home/isp/apps/jdk21/bin:$PATH GRADLE_USER_HOME=/home/isp/.gradle
cat > "$run/control/force-tests.gradle" <<'GRADLE'
allprojects { tasks.withType(Test).configureEach { outputs.upToDateWhen { false } } }
GRADLE
cd "$run/root/api"
date -u +%FT%TZ > "$run/evidence/api-started-utc.txt"
set +e
flock /tmp/cyf-gradle.lock /home/isp/apps/gradle/9.3.1/bin/gradle :agent:jia-agent-service:archivePlatformContracts :agent:jia-agent-service:archiveMaintenanceSecurity :chat:jia-chat-service:archiveMaintenanceMvp :chat:jia-chat-service:archiveRegression --init-script "$run/control/force-tests.gradle" --continue --no-daemon --max-workers=1 '-Dorg.gradle.jvmargs=-Xmx768m -XX:MaxMetaspaceSize=384m' 2>&1 | tee "$run/evidence/api-gradle.log"
gradle_exit=${PIPESTATUS[0]}
set -e
printf '%s\n' "$gradle_exit" > "$run/evidence/api-gradle.exit.txt"
for pair in agent:archivePlatformContracts agent:archiveMaintenanceSecurity chat:archiveMaintenanceMvp chat:archiveRegression; do
 module=${pair%:*}; task=${pair#*:}; mkdir -p "$run/evidence/$task"
 cp "$module/jia-$module-service/build/test-results/$task/"TEST-*.xml "$run/evidence/$task/"
done
python3 - "$run" <<'PY'
import json,pathlib,hashlib,xml.etree.ElementTree as E,subprocess,datetime,sys
r=pathlib.Path(sys.argv[1]); suites=[]
start=datetime.datetime.fromisoformat((r/'evidence/api-started-utc.txt').read_text().strip().replace('Z','+00:00')).timestamp()
for name in ('archivePlatformContracts','archiveMaintenanceSecurity','archiveMaintenanceMvp','archiveRegression'):
 files=sorted((r/'evidence'/name).glob('TEST-*.xml')); d={'suite':name,'tests':0,'failures':0,'errors':0,'skipped':0,'failure_set':[],'xml':[],'xml_all_fresh':True}
 for f in files:
  e=E.parse(f).getroot()
  for key in ('tests','failures','errors','skipped'): d[key]+=int(e.get(key,0))
  for t in e.findall('testcase'):
   if t.find('failure') is not None or t.find('error') is not None: d['failure_set'].append(t.get('classname')+'#'+t.get('name'))
  # cp preserves content, original task mtime checked separately below
  source=r/'root/api'/('agent' if name.startswith('archivePlatform') or name=='archiveMaintenanceSecurity' else 'chat')/('jia-agent-service' if name.startswith('archivePlatform') or name=='archiveMaintenanceSecurity' else 'jia-chat-service')/'build/test-results'/name/f.name
  fresh=source.stat().st_mtime>=start; d['xml_all_fresh'] &= fresh
  d['xml'].append({'file':name+'/'+f.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'fresh':fresh})
 d['pass']=d['tests']-d['failures']-d['errors']-d['skipped']; suites.append(d)
git=lambda p,*a:subprocess.check_output(['git','-C',str(p),*a],text=True).strip()
output={'results':suites,'gradle_exit':int((r/'evidence/api-gradle.exit.txt').read_text()),'api_commit':git(r/'root/api','rev-parse','HEAD'),'api_tree':git(r/'root/api','rev-parse','HEAD^{tree}'),'source_unchanged':not git(r/'root/api','status','--porcelain'),'natural_completion':True,'mysql_port':34061,'task_own_datadir':str(r/'mysql-data'),'production_operation':False}
(r/'evidence/api-result.json').write_text(json.dumps(output,indent=2)+'\n')
for d in suites: print('SUITE',d['suite'],d['tests'],d['pass'],d['failures'],d['skipped'],d['xml_all_fresh'])
PY
cleanup_mysql
trap - EXIT
for key in client web; do
 if [ "$key" = client ]; then checkout="$run/isp-install/conf/codex-ws-agent"; prior=/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent; else checkout="$run/root/web"; prior=/home/isp/wsps/cyf/web; fi
 cd "$checkout"
 if cmp -s package-lock.json "$prior/package-lock.json" && [ -d "$prior/node_modules" ]; then
   cp -a "$prior/node_modules" .
   echo "DEPENDENCIES $key reused exact-lockfile node_modules copy"
 else
   npm ci > "$run/evidence/$key-install.log" 2>&1
 fi
 set +e
 npm test 2>&1 | tee "$run/evidence/$key-test.log"
 result=${PIPESTATUS[0]}
 set -e
 printf '%s\n' "$result" > "$run/evidence/$key-test.exit.txt"
 if [ "$key" = web ]; then
   set +e
   npm run build 2>&1 | tee "$run/evidence/web-build.log"
   result=${PIPESTATUS[0]}
   set -e
   printf '%s\n' "$result" > "$run/evidence/web-build.exit.txt"
 fi
done
for p in "$run/root/api" "$run/root/web" "$run/isp-install"; do git -C "$p" status --short; git -C "$p" rev-parse HEAD HEAD^{tree}; done
printf 'END %s\n' "$(date -Iseconds)"