#!/bin/bash
set -euo pipefail
cd /home/isp/wsps/cyf/.worktrees/juyiting-multimedia-deliberation-20260928/api-primary-v3-admission
E=/var/tmp/cyf-mmd-reference-integrity-main-20261003
N=${1:?attempt}
export JAVA_HOME=/home/isp/apps/jdk21 PATH=/home/isp/apps/jdk21/bin:$PATH
export MMD_U1_REFERENCE_MYSQL_URL='jdbc:mysql://127.0.0.1:33793/mysql?useSSL=false&allowPublicKeyRetrieval=true'
export MMD_U1_REFERENCE_MYSQL_USER=root MMD_U1_REFERENCE_MYSQL_PASSWORD='' MMD_U1_REFERENCE_MYSQL_ISOLATED_FIXTURE=true MMD_U1_REFERENCE_MYSQL_DATABASE_PREFIX=mmd_refjson
TREE=$(git rev-parse HEAD^{tree}); SHA=$(git rev-parse HEAD)
python3 /home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py transition MMD-U4-BROWSER-BASELINE-SERVICE-READINESS --gate targeted_verification --agent main_01a0dde8_reference_read --profile critical_worker --mode writer --commit-sha "$SHA" --tree-sha "$TREE" --clear-blocker --next-action 'Reproduce and fix actual MySQL JSON whitespace/key-order normalization in assignment read; preserve exact semantic schema/authority/ACL/hash; task419 no replay, no Provider or production DML.'
python3 /home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py gradle --cwd "$PWD" --tree-sha "$TREE" --selector 'assignment-operation-reference:mysql-json-normalization' --fixture-digest "mysql8.0.21-refjson-port33793-init$(sha256sum "$E/verification.init.gradle" | cut -c1-16)" --artifact "$E/$N.log" MMD-U4-BROWSER-BASELINE-SERVICE-READINESS -- ./gradlew :agent:jia-agent-service:mmdU1BootstrapOutbox --tests '*AgentTaskBountyBootstrapOutboxServiceImplTest*' :agent:jia-agent-service:mmdControlledImageBridge --tests '*ControlledImageBridgeMySqlTest*' --continue --no-daemon --offline --configure-on-demand --max-workers=1 --console=plain -I "$E/verification.init.gradle" '-Dorg.gradle.jvmargs=-Xmx384m -XX:+UseSerialGC -XX:ActiveProcessorCount=2 -XX:MaxMetaspaceSize=256m -Dfile.encoding=UTF-8' > "$E/$N.log" 2>&1
