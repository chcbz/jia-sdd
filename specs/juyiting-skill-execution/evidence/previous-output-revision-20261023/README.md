# 上一版图片作为后续修改输入：局部验证

核对日期：2026-10-23。API commit `041548f601385a3463fbba06b929991371d93d9c`，tree `1bc5ae21325d9763e8325f31f4cc88a53317a5f3`。

- Flow5260799/248为CI-only SUCCESS；2921项通过、126项跳过、0失败/错误，共3047项。跳过清单见verification.json，不声称全量测试均执行。
- 新来源测试8项、admission测试2项及真实MySQL8授权查询1项全部实际执行通过。MySQL所属套件34项均通过，未使用可选外部数据库套件的skip代替验证。
- 原测试集、validateLayering及fresh bootJar均保留；同Run制品SHA及内含JAR摘要已核对。
- Runtime1.2.8真实上下文消费者轻量检查2项通过，不表示模型或生产流程验证通过。
- 临时流水线配置已恢复前值并回读一致，无部署作业，无API/Web/Runtime安装。

原始日志、XML和制品留在 `/var/tmp/cyf-previous-output-revision-20261023/`；本目录保存紧凑脱敏证据，不复制大型制品。Run247属于前一源码，仅保留历史，不作本次通过证据。

## 尚未完成

需获本次API版本发布授权后，按同Run测试/制品/部署契约上线，再以ziyue/吴用和带可辨识细节的图片验证自然连续修改：第二次inputReceipt SHA必须等于第一次成果SHA，并完成预览和最终验收。不能仅以变色、请求成功或可验收代替来源正确。PDF、精确尺寸及517历史状态不在本轮。

详见[本轮handoff](../../../../docs/implementation/handoffs/PREVIOUS-OUTPUT-REVISION-20261023.md)。
