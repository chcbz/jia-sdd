#!/usr/bin/env bash
set -euo pipefail
umask 077
base=/tmp/cyf-aam-merge-develop-20261008
out="$base/evidence/attempt4"
root_sha="$1";api_sha="$2";web_sha="$3";client_sha="$4"
for sha in "$root_sha" "$api_sha" "$web_sha" "$client_sha";do [[ "$sha" =~ ^[0-9a-f]{40}$ ]];done
[ -f "$base/evidence/attempt2/final-source-snapshot.json" ]
[ ! -e "$out" ] || exit 2
[ -z "$(git -C "$base/root" status --porcelain)" ]
[ -z "$(git -C "$base/root/api" status --porcelain)" ]
[ -z "$(git -C "$base/root/web" status --porcelain)" ]
[ -z "$(git -C "$base/isp-install" status --porcelain)" ]
mkdir -p "$out" "$base/mysql-data-attempt4"
exec > >(tee "$out/server-run.log") 2>&1
printf 'START_API_ATTEMPT4 %s\n' "$(date -Iseconds)"
git -C "$base/root" fetch origin codex/archive-agent-maintenance
git -c submodule.recurse=false -C "$base/root" checkout --detach "$root_sha"
git -C "$base/root/api" fetch origin codex/archive-agent-maintenance-api
git -C "$base/root/api" checkout --detach "$api_sha"
[ "$(git -C "$base/root" rev-parse HEAD:api)" = "$api_sha" ]
git -C "$base/root/web" fetch origin codex/archive-agent-maintenance-web
git -C "$base/root/web" checkout --detach "$web_sha"
git -C "$base/isp-install" fetch origin codex/archive-agent-maintenance-client
git -C "$base/isp-install" checkout --detach "$client_sha"
[ "$(git -C "$base/root" rev-parse HEAD:web)" = "$web_sha" ]
cat > "$base/control/environment.gradle" <<'GRADLE'
beforeSettings { settings ->
 if (settings.settingsDir.canonicalPath == '/tmp/cyf-aam-merge-develop-20261008/root/api') {
  settings.pluginManagement { includeBuild(new File(settings.settingsDir, 'plugin').absolutePath) }
 }
}
gradle.beforeProject { project ->
 if (project == project.rootProject) {
  project.ext.snapshotsRepoUrl = 'https://maven.aliyun.com/repository/public'
  project.ext.releasesRepoUrl = 'https://maven.aliyun.com/repository/public'
  project.ext.repoUsername = ''
  project.ext.repoPassword = ''
 }
}
allprojects {
 tasks.withType(Test).configureEach {
  outputs.upToDateWhen { false }
  maxParallelForks = 1
  maxHeapSize = '256m'
  jvmArgs '-XX:+UseSerialGC', '-XX:ActiveProcessorCount=2', '-XX:MaxMetaspaceSize=192m', '-Xss256k'
 }
}
GRADLE
python3 - <<'PY'
import socket
s=socket.socket();s.bind(('127.0.0.1',34061));s.close()
PY
/usr/sbin/mysqld --no-defaults --initialize-insecure --user=root --datadir="$base/mysql-data-attempt4" > "$out/mysql-init.log" 2>&1
/usr/sbin/mysqld --no-defaults --user=root --datadir="$base/mysql-data-attempt4" --socket="$base/mysql-attempt4.sock" --pid-file="$base/mysql-attempt4.pid" --log-error="$out/mysql-server.log" --bind-address=127.0.0.1 --port=34061 --mysqlx=0 --skip-log-bin --innodb-buffer-pool-size=128M --max-connections=60 &
mysql_pid=$!
cleanup_mysql() {
 if [ -r "/proc/$mysql_pid/cmdline" ] && tr '\0' ' ' < "/proc/$mysql_pid/cmdline" | grep -F -- "--datadir=$base/mysql-data-attempt4" >/dev/null; then
  mysqladmin --no-defaults --socket="$base/mysql-attempt4.sock" -u root shutdown
  wait "$mysql_pid" || true
  printf 'OWN_MYSQL_SHUTDOWN_OBSERVED %s\n' "$(date -Iseconds)"
 fi
}
trap cleanup_mysql EXIT
until mysqladmin --no-defaults --socket="$base/mysql-attempt4.sock" -u root ping >/dev/null 2>&1; do kill -0 "$mysql_pid";sleep 1;done
password=$(python3 -c 'import secrets; print(secrets.token_hex(24))')
mysql --no-defaults --socket="$base/mysql-attempt4.sock" -u root <<SQL
CREATE DATABASE cyf_h02_aam_merge_20261008;
CREATE DATABASE cyf_h03_aam_merge_20261008;
CREATE DATABASE cyf_h05a_aam_merge_20261008;
CREATE DATABASE aam_runtime_schema_test;
CREATE USER 'aam_dev'@'127.0.0.1' IDENTIFIED BY '$password';
GRANT ALL ON cyf_h02_aam_merge_20261008.* TO 'aam_dev'@'127.0.0.1';
GRANT ALL ON cyf_h03_aam_merge_20261008.* TO 'aam_dev'@'127.0.0.1';
GRANT ALL ON cyf_h05a_aam_merge_20261008.* TO 'aam_dev'@'127.0.0.1';
GRANT ALL ON aam_runtime_schema_test.* TO 'aam_dev'@'127.0.0.1';
SELECT @@port, @@datadir, @@server_uuid, @@log_bin;
SQL
for lane in H02 H03 H05A; do
 db=$(echo "$lane" | tr '[:upper:]' '[:lower:]')
 export "CYF_${lane}_MYSQL_ISOLATED=true" "CYF_${lane}_MYSQL_URL=jdbc:mysql://127.0.0.1:34061/cyf_${db}_aam_merge_20261008" "CYF_${lane}_MYSQL_DATABASE_CONFIRM=cyf_${db}_aam_merge_20261008" "CYF_${lane}_MYSQL_USER=aam_dev" "CYF_${lane}_MYSQL_PASSWORD=$password"
done
export CYF_AAM_SCHEMA_TEST_MYSQL_URL=jdbc:mysql://127.0.0.1:34061/aam_runtime_schema_test CYF_AAM_SCHEMA_TEST_MYSQL_USER=aam_dev CYF_AAM_SCHEMA_TEST_MYSQL_PASSWORD="$password"
export JAVA_HOME=/home/isp/apps/jdk21 PATH=/home/isp/apps/jdk21/bin:$PATH GRADLE_USER_HOME=/root/.gradle
cd "$base/root"
bash ./sddw verify archive-agent-maintenance | tee "$out/sddw-verify.log"
cd "$base/root/api"
date -u +%FT%TZ > "$out/api-started-utc.txt"
set +e
flock /tmp/cyf-gradle.lock /home/isp/apps/gradle/9.3.1/bin/gradle :agent:jia-agent-service:archivePlatformContracts :agent:jia-agent-service:archiveMaintenanceSecurity :chat:jia-chat-service:archiveMaintenanceMvp :chat:jia-chat-service:archiveRegression :chat:jia-chat-service:mmdU2TypedInspection :chat:jia-chat-service:chatConversationReplay --init-script "$base/control/environment.gradle" --continue --no-daemon --max-workers=1 '-Dorg.gradle.jvmargs=-Xmx448m -XX:MaxMetaspaceSize=256m -Xss256k -XX:+UseSerialGC -XX:ActiveProcessorCount=2' 2>&1 | tee "$out/api-gradle.log"
gradle_exit=${PIPESTATUS[0]}
set -e
printf '%s\n' "$gradle_exit" > "$out/api-gradle.exit.txt"
python3 - "$base" <<'PY'
import sys,pathlib,subprocess,json,datetime,hashlib,xml.etree.ElementTree as E,shutil
b=pathlib.Path(sys.argv[1]);out=b/'evidence/attempt4';start=datetime.datetime.strptime((out/'api-started-utc.txt').read_text().strip(),'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc).timestamp();suites=[]
for module,task in [('agent','archivePlatformContracts'),('agent','archiveMaintenanceSecurity'),('chat','archiveMaintenanceMvp'),('chat','archiveRegression'),('chat','mmdU2TypedInspection'),('chat','chatConversationReplay')]:
 source=b/'root/api'/module/('jia-'+module+'-service')/'build/test-results'/task;dest=out/task;dest.mkdir(exist_ok=True)
 d={'task':task,'tests':0,'failures':0,'errors':0,'skipped':0,'failure_set':[],'fresh_xml':[],'stale_ignored':[]}
 for f in sorted(source.glob('TEST-*.xml')):
  if f.stat().st_mtime<start:d['stale_ignored'].append(f.name);continue
  e=E.parse(f).getroot()
  for k in ['tests','failures','errors','skipped']:d[k]+=int(e.get(k,0))
  for t in e.findall('testcase'):
   if t.find('failure') is not None or t.find('error') is not None:d['failure_set'].append(t.get('classname')+'#'+t.get('name'))
  shutil.copyfile(f,dest/f.name);d['fresh_xml'].append({'file':f.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
 d['pass']=d['tests']-d['failures']-d['errors']-d['skipped'];suites.append(d);print('SUITE',task,d['tests'],d['pass'],d['failures'],d['errors'],d['skipped'])
git=lambda p,*a:subprocess.check_output(['git','-C',str(p),*a],universal_newlines=True).strip()
result={'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'api_commit':git(b/'root/api','rev-parse','HEAD'),'api_tree':git(b/'root/api','rev-parse','HEAD^{tree}'),'source_unchanged':not git(b/'root/api','status','--porcelain'),'gradle_exit':int((out/'api-gradle.exit.txt').read_text()),'suites':suites,'all_requested_suites_have_fresh_xml':all(d['fresh_xml'] for d in suites),'production_operation':False,'whole_feature_accepted':False}
(out/'api-result.json').write_text(json.dumps(result,indent=2)+'\n')
PY
cleanup_mysql
trap - EXIT
python3 - "$base" <<'SNAPSHOT'
import pathlib,subprocess,json,sys,datetime,socket
b=pathlib.Path(sys.argv[1]);repos={}
for key,p in [('root',b/'root'),('api',b/'root/api'),('web',b/'root/web'),('client',b/'isp-install')]:
 def g(*a):return subprocess.check_output(['git','-C',str(p),*a],universal_newlines=True).strip()
 repos[key]={'commit':g('rev-parse','HEAD'),'tree':g('rev-parse','HEAD^{tree}'),'status':g('status','--porcelain'),'source_unchanged':not g('status','--porcelain')}
s=socket.socket();port_closed=s.connect_ex(('127.0.0.1',34061))!=0;s.close()
(b/'evidence/attempt4/final-source-snapshot.json').write_text(json.dumps({'at':datetime.datetime.now().astimezone().isoformat(),'repos':repos,'own_mysql_port34061_closed':port_closed,'client_web_verification':'separate_node_final_run_required','production_operations':False,'whole_feature_accepted':False},indent=2)+'\n')
SNAPSHOT
flock -n /tmp/cyf-gradle.lock true && echo 'FINAL_GRADLE_LOCK_AVAILABLE' || echo 'LOCK_CURRENTLY_BUSY_NO_OWN_BUILD_RUNNING'
printf 'END_API_ATTEMPT4 %s\n' "$(date -Iseconds)"
