#!/usr/bin/env bash
set -euo pipefail
umask 077
base=/tmp/cyf-aam-resume-20261007
run="$base/runtime"
[ -f "$base/evidence/api-result.json" ] && [ ! -e "$run" ]
mkdir -p "$run/evidence" "$run/io" "$run/artifacts" "$run/mysql-data" "$run/redis" "$run/rabbit-home" "$run/rabbit-data" "$run/rabbit-log"
exec > >(tee "$run/evidence/runtime-launch.log") 2>&1
python3 - <<'PY'
import socket
for p in (34161,34162,34163,34164,18121,18124):
 s=socket.socket();s.bind(('127.0.0.1',p));s.close()
PY
export JAVA_HOME=/home/isp/apps/jdk21 PATH=/home/isp/apps/jdk21/bin:/home/isp/apps/erlang/bin:$PATH GRADLE_USER_HOME=/home/isp/.gradle
export CYF_RUNTIME_CLASSPATH_FILE="$run/io/classpath.txt"
cd "$base/root/api"
flock /tmp/cyf-gradle.lock /home/isp/apps/gradle/9.3.1/bin/gradle :chat:jia-chat-starter:archiveRealRuntimeClasspath --no-daemon --max-workers=1 '-Dorg.gradle.jvmargs=-Xmx768m -XX:MaxMetaspaceSize=384m' > "$run/evidence/classpath.log" 2>&1
mysql_pid='';redis_pid='';rabbit_pid='';java_pid='';client_pid='';web_pid=''
stop_exact() { local pid="$1" marker="$2"; if [ -n "$pid" ] && [ -r "/proc/$pid/cmdline" ] && tr '\0' ' ' < "/proc/$pid/cmdline" | grep -F -- "$marker" >/dev/null; then kill -TERM "$pid" || true; fi; }
export HOME="$run/rabbit-home" RABBITMQ_NODENAME=aam_resume_20261007@localhost RABBITMQ_NODE_IP_ADDRESS=127.0.0.1 RABBITMQ_NODE_PORT=34162
export RABBITMQ_MNESIA_BASE="$run/rabbit-data" RABBITMQ_LOG_BASE="$run/rabbit-log" RABBITMQ_PID_FILE="$run/rabbit.pid" RABBITMQ_CONFIG_FILE="$run/rabbit-config"
export RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS='-kernel inet_dist_listen_min 34163 inet_dist_listen_max 34163 inet_dist_use_interface {127,0,0,1}'
export RABBITMQ_ENABLED_PLUGINS_FILE="$run/enabled_plugins"
printf '[].\n' > "$run/enabled_plugins"
printf '[{rabbit,[{tcp_listeners,[{"127.0.0.1",34162}]}]}].\n' > "$run/rabbit-config.config"
cleanup() {
 stop_exact "$client_pid" "$base/isp-install/conf/codex-ws-agent/agent-client.mjs"
 if [ -n "$web_pid" ] && [ -r "/proc/$web_pid/cmdline" ] && [ "$(readlink -f "/proc/$web_pid/cwd")" = "$base/root/web" ] && tr '\0' ' ' < "/proc/$web_pid/cmdline" | grep -F "createServer" >/dev/null; then kill -TERM "$web_pid" || true; fi
 stop_exact "$java_pid" cn.jia.fixture.archive.ArchiveRealRuntimeFixtureApplication
 if [ -n "$rabbit_pid" ] && [ -s "$run/rabbit.pid" ]; then p=$(cat "$run/rabbit.pid"); if [ -r "/proc/$p/cmdline" ] && tr '\0' ' ' < "/proc/$p/cmdline" | grep -F -- "$RABBITMQ_NODENAME" >/dev/null; then /home/isp/apps/rabbitmq/sbin/rabbitmqctl -n "$RABBITMQ_NODENAME" stop > "$run/evidence/rabbit-stop.log" 2>&1 || true; fi; fi
 if [ -n "$redis_pid" ] && [ -r "/proc/$redis_pid/cwd" ] && [ "$(readlink -f "/proc/$redis_pid/cwd")" = "$run/redis" ]; then kill -TERM "$redis_pid" || true; fi
 if [ -n "$mysql_pid" ] && [ -r "/proc/$mysql_pid/cmdline" ] && tr '\0' ' ' < "/proc/$mysql_pid/cmdline" | grep -F -- "--datadir=$run/mysql-data" >/dev/null; then mysqladmin --no-defaults --socket="$run/mysql.sock" -u root shutdown || true; fi
}
trap cleanup EXIT
/usr/sbin/mysqld --no-defaults --initialize-insecure --user=root --datadir="$run/mysql-data" > "$run/evidence/mysql-init.log" 2>&1
/usr/sbin/mysqld --no-defaults --user=root --datadir="$run/mysql-data" --socket="$run/mysql.sock" --pid-file="$run/mysql.pid" --log-error="$run/evidence/mysql.log" --bind-address=127.0.0.1 --port=34161 --mysqlx=0 --skip-log-bin --innodb-buffer-pool-size=128M &
mysql_pid=$!
for i in $(seq 1 60); do mysqladmin --no-defaults --socket="$run/mysql.sock" -u root ping >/dev/null 2>&1 && break; kill -0 "$mysql_pid"; sleep 1; done
password=$(python3 -c 'import secrets; print(secrets.token_hex(24))')
mysql --no-defaults --socket="$run/mysql.sock" -u root <<SQL
CREATE DATABASE cyf_aam_runtime_resume_20261007;
CREATE USER 'aam_dev'@'127.0.0.1' IDENTIFIED BY '$password';
GRANT ALL ON cyf_aam_runtime_resume_20261007.* TO 'aam_dev'@'127.0.0.1';
SQL
export CYF_H02_MYSQL_ISOLATED=true CYF_H02_MYSQL_URL=jdbc:mysql://127.0.0.1:34161/cyf_aam_runtime_resume_20261007 CYF_H02_MYSQL_DATABASE_CONFIRM=cyf_aam_runtime_resume_20261007 CYF_H02_MYSQL_USER=aam_dev CYF_H02_MYSQL_PASSWORD="$password"
export CYF_FIXTURE_MYSQL_SERVER_PORT=34161 CYF_FIXTURE_MYSQL_DATA_DIRECTORY="$run/mysql-data"
export CYF_FIXTURE_HOST=127.0.0.1 CYF_FIXTURE_PORT=18121 CYF_FIXTURE_WEB_ORIGIN=http://127.0.0.1:18124
export CYF_FIXTURE_READY_FILE="$run/io/ready.json" CYF_FIXTURE_RESULT_FILE="$run/io/result.json" CYF_FIXTURE_ADMIN_TOKEN_FILE="$run/io/admin.jwt" CYF_FIXTURE_ARTIFACT_ROOT="$run/artifacts"
export CYF_FIXTURE_JWT_ISSUER=cyf-aam-isolated-20261007 CYF_FIXTURE_JWT_AUDIENCE=cyf-aam-runtime-fixture CYF_FIXTURE_ACTOR=aam_fixture_owner CYF_FIXTURE_OWNER=aam_fixture_owner CYF_FIXTURE_CLIENT=aam_fixture_client
export CYF_FIXTURE_AGENT_ID=agt_0123456789abcdef0123456789abcdef CYF_FIXTURE_API_KEY_ID=aam_fixture_key CYF_FIXTURE_API_KEY="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
export CYF_REDIS_HOST=127.0.0.1 CYF_REDIS_PORT=34164 CYF_REDIS_PASSWORD="$password"
(cd "$run/redis"; exec /home/isp/apps/redis/bin/redis-server --bind 127.0.0.1 --port 34164 --save '' --appendonly no --requirepass "$password" --dir "$run/redis") > "$run/evidence/redis.log" 2>&1 &
redis_pid=$!
/home/isp/apps/rabbitmq/sbin/rabbitmq-server > "$run/evidence/rabbit-launch.log" 2>&1 &
rabbit_pid=$!
for i in $(seq 1 60); do /home/isp/apps/rabbitmq/sbin/rabbitmqctl -n "$RABBITMQ_NODENAME" status > "$run/evidence/rabbit-status.log" 2>&1 && break; kill -0 "$rabbit_pid"; sleep 2; done
export CYF_RABBIT_HOST=127.0.0.1 CYF_RABBIT_PORT=34162 CYF_RABBIT_VHOST=aam_fixture CYF_RABBIT_USERNAME=aam_fixture CYF_RABBIT_PASSWORD="$password"
/home/isp/apps/rabbitmq/sbin/rabbitmqctl -n "$RABBITMQ_NODENAME" add_vhost "$CYF_RABBIT_VHOST" > "$run/evidence/rabbit-provision.log" 2>&1
/home/isp/apps/rabbitmq/sbin/rabbitmqctl -n "$RABBITMQ_NODENAME" add_user "$CYF_RABBIT_USERNAME" "$password" >> "$run/evidence/rabbit-provision.log" 2>&1
/home/isp/apps/rabbitmq/sbin/rabbitmqctl -n "$RABBITMQ_NODENAME" set_permissions -p "$CYF_RABBIT_VHOST" "$CYF_RABBIT_USERNAME" '.*' '.*' '.*' >> "$run/evidence/rabbit-provision.log" 2>&1
cp_value=$(paste -sd: "$CYF_RUNTIME_CLASSPATH_FILE")
java -Xmx512m -XX:MaxMetaspaceSize=256m -cp "$cp_value" cn.jia.fixture.archive.ArchiveRealRuntimeFixtureApplication > "$run/evidence/java.log" 2>&1 &
java_pid=$!
for i in $(seq 1 120); do [ -f "$run/io/ready.json" ] && break; kill -0 "$java_pid"; sleep 2; done
[ -f "$run/io/ready.json" ]
export CYF_CLIENT_ROOT="$base/isp-install" CYF_FIXTURE_RUN_ROOT="$run" CYF_CLIENT_WS_URL=ws://127.0.0.1:18121/ws/agent/channel
sh "$base/root/api/scripts/archive-real-runtime/run-client.sh" > "$run/evidence/client-runtime.log" 2>&1 &
client_pid=$!
export CYF_FIXTURE_BINDING_VERSION="$(mysql --no-defaults --socket="$run/mysql.sock" -u root -N -B cyf_aam_runtime_resume_20261007 -e "SELECT id FROM agent_persona_binding WHERE persona_code='fixture-editor' AND status=1")"
python3 "$base/control/runtime-driver.py" "$run" "$CYF_FIXTURE_AGENT_ID" > "$run/evidence/http-driver.log" 2>&1
# Browser executes source-only control adaptation against real fixture HTTP; no fetch or websocket doubles.
cd "$base/root/web"
export VITE_API_BASE_URL=http://127.0.0.1:18121 VITE_APP_ENV=test
node -e "import('vite').then(async({createServer})=>{const s=await createServer({root:process.cwd(),server:{host:'127.0.0.1',port:18124,https:false,strictPort:true}});await s.listen()})" > "$run/evidence/web-runtime.log" 2>&1 &
web_pid=$!
for i in $(seq 1 60); do curl -fsS http://127.0.0.1:18124/juyiting >/dev/null && break; kill -0 "$web_pid"; sleep 1; done
export CYF_WEB_ORIGIN=http://127.0.0.1:18124 CYF_FIXTURE_API_ORIGIN=http://127.0.0.1:18121 CYF_WEB_ROOT="$base/root/web" CYF_BROWSER_RESULT_FILE="$run/evidence/browser-result.json"
export CYF_FIXTURE_JOB_ID="$(python3 -c "import json;print(json.load(open('$run/io/driver-state.json'))['manual']['job']['jobId'])")"
export CYF_FIXTURE_WORK_ID="$(python3 -c "import json;print(json.load(open('$run/io/driver-state.json'))['manual']['job']['workId'])")"
export CYF_FIXTURE_EDITION_ID="$(python3 -c "import json;print(json.load(open('$run/io/driver-state.json'))['manual']['publication']['editionId'])")"
export CYF_PLAYWRIGHT_ENTRY="$base/control/browser/node_modules/playwright/index.mjs"
node "$base/control/run-browser-server.mjs" > "$run/evidence/browser.log" 2>&1
printf 'REAL_RUNTIME_HTTP_CLIENT_BROWSER_FINISHED %s\n' "$(date -Iseconds)"
