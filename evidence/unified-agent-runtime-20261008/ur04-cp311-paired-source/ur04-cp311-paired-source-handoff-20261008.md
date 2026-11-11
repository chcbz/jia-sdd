# UR04 paired SOURCE 同步源码阶段交接（2026-10-08）

## 独立输入/候选
- WT: /home/isp/wsps/worktrees/ur04-cp311-paired-source-20261008
- branch: codex/ur04-cp311-paired-source-20261008
- base: 64d445a6a76fbe4a7f527fe914bdce6b5c6105da/treec0e486cb63f7293682a4400bfd41fa39bf363bee
- candidate commit: b125d70c79471be0fc9f306cc0f2e9cd85890ee4
- candidate tree: 4b875b456573f65865096fb34be7b25544897e46
- remote readback: b125d70c79471be0fc9f306cc0f2e9cd85890ee4	refs/heads/codex/ur04-cp311-paired-source-20261008
- WT clean，源码写入结束。旧UR02 WT未修改，主控session65727未操作/取消/等待/预测结果。没有push develop/部署。

## 精确owned四路径
- /home/isp/wsps/worktrees/ur04-cp311-paired-source-20261008/agent/jia-agent-service/src/ur04E05Http/resources/ur04/e05-runtime-http-client.mjs
- /home/isp/wsps/worktrees/ur04-cp311-paired-source-20261008/agent/jia-agent-service/src/ur04E05Http/java/cn/jia/agent/acceptance/ur04/Ur04E05HttpDbAcceptanceTest.java
- /home/isp/wsps/worktrees/ur04-cp311-paired-source-20261008/agent/jia-agent-service/src/ur06EnrollMysql/resources/ur06/enroll-mysql-client.mjs
- /home/isp/wsps/worktrees/ur04-cp311-paired-source-20261008/agent/jia-agent-service/src/ur06EnrollMysql/java/cn/jia/agent/acceptance/ur06/Ur06EnrollMysqlAcceptanceTest.java

## 仅固定来源字面量变化
- payload A commit d91ebbf436911eac20ffb70cb92192a65c742e11
- A tree b2e3f17ff57e21e2482c0fc54e71dbf4b92dbd82
- A files/count 285（常量不变）
- A raw git archive bytes 3624960
- A archive SHA256 3c826b9e78db3bc4ca5a9eef1e9026ebeb0e34626e214a6b1b2d8bd532169b36
- 两Node SOURCE四字段、两Java CLIENT及UR04 tree expectation替换，最终4files/9lines changed。未改变任何业务逻辑、permissions/auth/ACK/fence、sourcefailclosed、完整成员/模式/hash/tree/制品来源断言或private清理。
- 每个文件仅四来源literal forward/reverse替换与base完整字节对比成立；两Java全部63+73=136个method/constructor body只归一化来源literal后逐字节一致。UR04原6 E05与UR06原7 enroll/MySQL selector同名同序，全部断言保留，无skip。
- 旧7594/0827/f4dcd/3594240在此四文件全部去除，原严格SOURCE等值判定不变，未加双来源兼容。
- B 2533381cc79e79d124d8c8630914790f48d3619e/tree739f25ca5e7759ab427a7694d9cc55dc51d46732仅主控harness身份；四文件不绑定B作payload。没有改harness/init/DDL/生产源码/其他fixture文件。

## source proof 精确读取与低成本核对
1. /var/tmp/ur01-python-wheel-fix-source-20261008/payload-A-source-proof.json
   SHA256 c4f7b8a631378524c7c82eb123b15790c3d63766b8d8174485e30848267873d3
2. /home/isp/wsps/cyf/evidence/unified-agent-runtime-20261008/ur01-cp311-source-readback/independent-source-readback.json
   SHA256 4d56262eed67bdfb3397419500e7e463f675b7a8369273061bc7d6bdcdb4c767

两proof commit/tree/count/tarSHA/bytes/PAX一致；只读payload-A.tar全部285 regular files+73directories/358members，验证文件SHA/Gitblob/executablemode与proof、重建完整Git tree=b2e3、archive hash和PAX=A，不extract/安装/运行payload。
node v20.20.2对两原mjs执行node --check，均exit0；两Java tree-sitter grammar OK；diff --check/精确4paths/normalized whole-file及method body比较OK。**只代表syntax/static来源一致，不是Java compile或真实跨端测试PASS。**
- static report: /var/tmp/ur04-cp311-paired-source-static-20261008.json
- static report SHA256: 4409399a56f2407fb2b7da97c5e93877731eb63da1a1fecb704217c1aed33df9
- static script: /var/tmp/ur04-cp311-paired-source-static-20261008.py

## 实际未验收状态 / 接续
- 未执行Gradle/安装/npm/pip/MySQL/Provider/Flow/任何生产操作；未消费完整installedartifact，archive不是安装制品。
- 新A四C、UR04六E05、UR06七enroll/MySQL在此candidate均NOT_RUN。本slice无M4实现/结果，Curie readonly计划继续由主控接续，不能以来源同步关闭M4/Goal。
- UR02session65727属主控正式verifier，Owner没有终态证据，未报PASS。
- 交主控固定b125d70c79471be0fc9f306cc0f2e9cd85890ee4/4b875b456573f65865096fb34be7b25544897e46，同新A/B批次经orchestrator正式编译/pairedsource消费；callback仅在实际新四C全PASS及完整proof readback后消费同canonical artifact。原所有selector及失败边界继续保留。source阶段候选结束，不需要Reviewer。
