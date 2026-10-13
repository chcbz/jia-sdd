#!/usr/bin/env bash
set -euo pipefail
umask 077
base=/tmp/cyf-aam-merge-develop-20261013
out="$base/evidence/api-attempt1"
[ ! -e "$out" ]; mkdir -p "$out" "$base/mysql-data-attempt1"
[ -z "$(git -C "$base/root/api" status --porcelain)" ]
api_tree=$(git -C "$base/root/api" rev-parse 'HEAD^{tree}')
selector='archivePlatformContracts archiveMaintenanceSecurity archiveMaintenanceMvp archiveRegression mmdU2TypedInspection chatConversationReplay validateLayering'
fixture_digest=$(sha256sum "$base/control/server-api-scoped.sh" | cut -d' ' -f1)
export CYF_ORCHESTRATOR_NOTIFICATION_OUTBOX="$base/control/notifications.jsonl"
unset CYF_ORCHESTRATOR_NOTIFY_CMD CYF_LOCAL_RELEASE_OPT_IN CYF_LOCAL_GRADLE_ACTIVE
exec > >(tee "$out/server-run.log") 2>&1
printf 'START_SCOPED_API %s\n' "$(date -Iseconds)"
cat > "$base/control/environment.gradle" <<'GRADLE'
beforeSettings { settings ->
 if (settings.settingsDir.canonicalPath == '/tmp/cyf-aam-merge-develop-20261013/root/api') {
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
/usr/sbin/mysqld --no-defaults --initialize-insecure --user=root --datadir="$base/mysql-data-attempt1" > "$out/mysql-init.log" 2>&1
/usr/sbin/mysqld --no-defaults --user=root --datadir="$base/mysql-data-attempt1" --socket="$base/mysql-attempt1.sock" --pid-file="$base/mysql-attempt1.pid" --log-error="$out/mysql-server.log" --bind-address=127.0.0.1 --port=34061 --mysqlx=0 --skip-log-bin --innodb-buffer-pool-size=128M --max-connections=60 &
mysql_pid=$!
cleanup_mysql() {
 if [ -r "/proc/$mysql_pid/cmdline" ] && tr '\0' ' ' < "/proc/$mysql_pid/cmdline" | grep -F -- "--datadir=$base/mysql-data-attempt1" >/dev/null; then
  mysqladmin --no-defaults --socket="$base/mysql-attempt1.sock" -u root shutdown
  wait "$mysql_pid" || true
  printf 'OWN_MYSQL_SHUTDOWN_OBSERVED %s\n' "$(date -Iseconds)"
 fi
}
trap cleanup_mysql EXIT
until mysqladmin --no-defaults --socket="$base/mysql-attempt1.sock" -u root ping >/dev/null 2>&1; do kill -0 "$mysql_pid";sleep 1;done
password=$(python3 -c 'import secrets; print(secrets.token_hex(24))')
mysql --no-defaults --socket="$base/mysql-attempt1.sock" -u root <<SQL
CREATE DATABASE cyf_h02_aam_merge_20261013;
CREATE DATABASE cyf_h03_aam_merge_20261013;
CREATE DATABASE cyf_h05a_aam_merge_20261013;
CREATE DATABASE aam_runtime_schema_test;
CREATE USER 'aam_dev'@'127.0.0.1' IDENTIFIED BY '$password';
GRANT ALL ON cyf_h02_aam_merge_20261013.* TO 'aam_dev'@'127.0.0.1';
GRANT ALL ON cyf_h03_aam_merge_20261013.* TO 'aam_dev'@'127.0.0.1';
GRANT ALL ON cyf_h05a_aam_merge_20261013.* TO 'aam_dev'@'127.0.0.1';
GRANT ALL ON aam_runtime_schema_test.* TO 'aam_dev'@'127.0.0.1';
SELECT @@port, @@datadir, @@server_uuid, @@log_bin;
SQL
for lane in H02 H03 H05A; do
 db=$(echo "$lane" | tr '[:upper:]' '[:lower:]')
 export "CYF_${lane}_MYSQL_ISOLATED=true" "CYF_${lane}_MYSQL_URL=jdbc:mysql://127.0.0.1:34061/cyf_${db}_aam_merge_20261013" "CYF_${lane}_MYSQL_DATABASE_CONFIRM=cyf_${db}_aam_merge_20261013" "CYF_${lane}_MYSQL_USER=aam_dev" "CYF_${lane}_MYSQL_PASSWORD=$password"
done
export CYF_AAM_SCHEMA_TEST_MYSQL_URL=jdbc:mysql://127.0.0.1:34061/aam_runtime_schema_test CYF_AAM_SCHEMA_TEST_MYSQL_USER=aam_dev CYF_AAM_SCHEMA_TEST_MYSQL_PASSWORD="$password"
export JAVA_HOME=/home/isp/apps/jdk21 PATH=/home/isp/apps/jdk21/bin:$PATH GRADLE_USER_HOME=/root/.gradle
cd "$base/root/api"
date -u +%FT%TZ > "$out/api-started-utc.txt"
set +e
python3 "$base/root/ops/orchestration/cyf_orchestrator.py" gradle --cwd "$base/root/api" --tree-sha "$api_tree" --selector "$selector" --fixture-digest "$fixture_digest" AAM-MERGE-DEVELOP-20261013 -- /home/isp/apps/gradle/9.3.1/bin/gradle :agent:jia-agent-service:archivePlatformContracts :agent:jia-agent-service:archiveMaintenanceSecurity :chat:jia-chat-service:archiveMaintenanceMvp :chat:jia-chat-service:archiveRegression :chat:jia-chat-service:mmdU2TypedInspection :chat:jia-chat-service:chatConversationReplay validateLayering --init-script "$base/control/environment.gradle" --continue --no-daemon --max-workers=1 '-Dorg.gradle.jvmargs=-Xmx448m -XX:MaxMetaspaceSize=256m -Xss256k -XX:+UseSerialGC -XX:ActiveProcessorCount=2' 2>&1 | tee "$out/api-gradle.log"
gradle_exit=${PIPESTATUS[0]}
set -e
printf '%s\n' "$gradle_exit" > "$out/api-gradle.exit.txt"
python3 - "$base" <<'PY'
import sys,pathlib,subprocess,json,datetime,hashlib,xml.etree.ElementTree as E,shutil
b=pathlib.Path(sys.argv[1]);out=b/'evidence/api-attempt1';start=datetime.datetime.strptime((out/'api-started-utc.txt').read_text().strip(),'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc).timestamp();suites=[]
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

[ -z "$(git -C "$base/root/api" status --porcelain)" ]
printf 'END_SCOPED_API %s\n' "$(date -Iseconds)"
