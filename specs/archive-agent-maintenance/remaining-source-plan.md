# 剩余源码交付路线

执行顺序以 `delivery-order.md` 为准，保持原 D2 范围。历史逐包证据见 `completion-audit.md`，当前事实见 `integration.yaml`。本文件不把待开发或待测试项标记为已完成。

| 包 | 原要求 | 当前状态 | 交付要点 |
| --- | --- | --- | --- |
| RECOVERY-13 | 同输入同根因第二次失败阻断，真实修复后新 attempt | 三项修复与最终窄复审接受；74 API / 41 Web 定向 PASS、build PASS；已本地提交，未 push | 真实 Runtime/安装/source 修复事实，retryable 不改变根因，scope 按授权语义计算；实库新 selector 待服务端 |
| 分页 | design §7.2、§7.4 | 69 API / 128 Web PASS、build PASS，独立窄审接受；已本地提交，未 push | 任职当前/历史、jobs state/cursor、管理 works、Reader works 的有界连续页；SQL 稳定 keyset；每页重新授权；Web 能继续读后续页且清身份/筛选后旧请求不得回填 |
| 章节断点 | design §9.3、§10.1 | 77 API / 80 Client 定向 PASS，独立窄审接受；已本地提交，未 push | Client 本 run 持久章节 digest/checkpoint；重启先读取服务端事实；服务端不可变章节对象引用/digest；复用共享存储，不建第三套文件系统 |
| 发布恢复 | design §10.2 | 唯一 critical Writer 正在实现 | SEALED → STAGING 分批写入，每批持久断点；崩溃重启可恢复；读回后 READY；最终 publication/active 在短事务授权和 CAS 后原子切换；旧版持续可读 |
| 存储生命周期 | design §18.3、来源对象边界 | 待开发 | 安装副本配额、基于真实引用的受控回收；source orphan/stale PENDING 恢复与清理；只处理本功能 namespace，不扫描推导资格或删除其他任务对象 |
| 文档与交付 | 用户交付指令 | 待收口 | 更新接口/配置/迁移/恢复/运维文档，按原要求源码收口；组件提交普通 push 并核远程 SHA 后 Root 更新 pins/gitlinks 再 push |
| 服务端全面验证 | 用户交付指令 | 完整源码 push 后执行 | 任务独占 checkout/隔离设施；保留服务端其他 dirty 工作区与生产服务/DB；共享 Gradle 锁；逐项保留 PASS、既有失败与新增失败 |

## 包级约束

- 唯一源码 Writer 串行实现，冻结后 Main 必要定向编译/自检，再独立只读窄复审；Reviewer 不修源码。
- 不重复把全面本地回归或 Runtime/browser 验证设为首次完整源码 push 的前置条件。
- 未完整开发前不以推送部分源码代替“开发完成”。不合并 master/develop，不 force-push。
- 已批准技能包字节不变；API/Web/Client 是独立仓库，Root 不提前 pin 未推送提交。
- 84 项生产业务验收、生产部署/迁移、真实典籍上架/任职/激活与付费调用不在本次开发验证的授权内。

## 用户硬截止（2026-10-04）

本次剩余开发从北京时间12:31:39起最多两小时，14:31:39若完整源码、文档和远程提交未完成则停止所有开发、测试与推送，保留现有工作并报告未完成项。不得在截止后自行继续。
