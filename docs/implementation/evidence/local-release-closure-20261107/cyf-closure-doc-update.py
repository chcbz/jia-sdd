from pathlib import Path
R=Path('/home/isp/wsps/cyf')
p=R/'docs/aliyun-flow-cicd-strategy.md';s=p.read_text();s=s.replace('当前默认快速路径、适用范围和未完成事项见下节','当前默认快速路径、适用范围和持久化/清理状态见下节').replace('### 已验证范围及未完成事项','### 已验证范围及持久化/清理状态')
a=s.index('- **仍待落地：持久存储与自动保留闭环。**');b=s.index('\n操作参数见',a)
s=s[:a]+'''- **2026-11-07持久化已完成并回读核验：** 构建JDK为`/opt/cyf/toolchains/dragonwell-21.0.11.0.11+10-GA`；已验证Gradle缓存为`/home/isp/state/cyf-local-build/gradle-home`。当前API、API回退和当前Web包的逐字节镜像位于`/home/isp/wsps/private-maintenance/cyf-local-archive-20261107-{api-current,api-rollback,web-current}/package/`；原历史安装记录未改写，仍绑定的内存盘原包继续保护。新批输出使用持久任务目录，不再依赖内存盘归档。
- **受控保留已实际启用：** 已安装现有维护工具的artifact登记及API LOCAL schema4/Web LOCAL schema2适配，4个完成任务已登记到原台账；原每30分钟cron继续消费，不新增任务。最新两批/组件、完成24小时、当前及回退绑定、进程/锁/未知状态均保护。只允许显式任务根或其`api/web/runtime`组件子根登记，不泛扫历史目录。
- 已清理明确过期/废弃的2个API备份、3个未发布构建中间JAR、2个Web历史载荷及1个孤儿stage，回收**1,591,824,384 allocated bytes（约1.48GiB）**；证据/日志和当前、必要回退保持。持久化同时占用磁盘，净余量约1GiB，仍低于自动清理5GiB触发值；实际cron入口退出3表示无合规候选但容量目标未达，不能强删数据库/Runtime/未知备份来凑8GiB。
- 维护工具253项隔离回归通过；真实自动入口已执行，末尾改为轻量`df`，不再以递归`du`长持锁。安装摘要、登记及清理证据见`docs/implementation/evidence/local-release-closure-20261107/`。版本化收口记录见同目录`version-control.json`（以实际生成及远端回读为准）；共享技能未修改，不声称已全局同步。
''' +s[b:];p.write_text(s)
p=R/'docs/DEPLOYMENT.md';s=p.read_text();s=s.replace('原临时源码已删除，内存盘JDK/包非持久归档，持久存储及清理器artifact登记尚未闭环。下一批先核对工具链、源码路径和备份峰值容量。','原临时源码已删除。JDK、Gradle缓存和当前/回退制品镜像已持久化；现有清理器已安装artifact登记及LOCAL记录适配，并由原cron消费。历史记录仍绑定的内存盘原包继续保留，不伪造重绑定。根盘仍约1GiB可用，下一批先核对工具链、源码路径和candidate+rollback峰值容量。');p.write_text(s)
p=R/'ops/orchestration/README.md';s=p.read_text().replace('--api-version VERSION --jdk /ABS/VERIFIED/JDK --cache-home /ABS/VERIFIED/CACHE \\\n  --output /ABS/NEW/OUTPUT','--api-version VERSION \\\n  --jdk /opt/cyf/toolchains/dragonwell-21.0.11.0.11+10-GA \\\n  --cache-home /home/isp/state/cyf-local-build/gradle-home \\\n  --output /home/isp/wsps/private-maintenance/cyf-NEW_BATCH')
s+='''
### 持久化与完成后保留（2026-11-07落地）

- 上述JDK和缓存已从临时路径迁入持久目录并核验；当前API/回退/Web包另有持久、摘要一致的镜像，历史安装record未改写。不要清理仍绑定的内存盘原件。干净源码须重新准备，历史计时worktree已删除。
- 完整批次结束并保存包外证据后，由Owner显式登记，不能仅凭构建成功推断任务结束；统一输出的组件子目录已受控支持：

```bash
/usr/bin/python3 -I -B /usr/local/libexec/cyf/rebuildable_cache_cleanup.py mark-complete \\
  --task-root /home/isp/wsps/private-maintenance/cyf-NEW_BATCH/api \\
  --artifact package/api.tgz --component api \\
  --source-commit FULL_API_COMMIT --source-tree FULL_API_TREE \\
  --payload-sha256 ACTUAL_APPLICATION_JAR_SHA256
# Web：使用同批 /web、package/web.tgz、component web及真实Web commit/tree，不传API payload参数。
```

- 最近两批/组件、24h及当前/回退引用均保护，沿用原30分钟cron和锁；重新使用任务目录前先mark-active。详见`ops/maintenance/LOCAL_ARTIFACT_RETENTION.md`。根盘约1GiB仍偏紧，不能据此保证冷构建/新增回归或后续任意批次达600秒。
''';p.write_text(s)
p=R/'ops/maintenance/LOCAL_ARTIFACT_RETENTION.md';s=p.read_text();a=s.index('> 当前状态：');b=s.index('\n\n',a);s=s[:a]+'> 当前状态（2026-11-07）：已安装并回读现有清理器、LOCAL记录适配及artifact登记；4个已完成任务已登记，原30分钟cron入口已真实消费。维护回归253项通过。实际入口退出3仅因根盘约1GiB仍低于5GiB，无可合法继续删除候选；未改写安装record或强删受保护数据。详细证据见 `docs/implementation/evidence/local-release-closure-20261107/`。'+s[b:];s=s.replace('及原显式 worktree bases；路径只能','及原显式 worktree bases，也支持同一显式base下`cyf-BATCH/{api,web,runtime}`的精确组件子根（逐级身份/挂载/.keep检查，不允许任意嵌套）；路径只能');s+='\n2026-11-07补记：现行API schema4 LOCAL由原coordinator原生校验器确认，Web schema2 LOCAL由原Web helper及私有备份descriptor确认；保留旧Flow支持，未知schema仍fail-closed。安装文件摘要、注册与真实入口记录已保存。上述“源码基线”是历史起点，不代表本轮工具字节已存在于该旧commit。\n';p.write_text(s)
note='''
## 历史清理与持久化闭环（2026-11-07）

按用户“先清理历史临时文件和备份文件，再完成闭环”执行。精确回收1,591,824,384 allocated bytes：2个过期API备份503,287,808、3个已废弃未发布构建中间JAR755,277,824、2个旧Web载荷及1个孤儿stage333,258,752。保留当前、回退、最新两份Web备份、数据库/Runtime/未知格式及包外证据；不是清空全部历史。

JDK已完整核验迁至`/opt/cyf/toolchains/dragonwell-21.0.11.0.11+10-GA`，缓存原子迁至`/home/isp/state/cyf-local-build/gradle-home`；当前API/回退/Web包字节一致镜像持久保存于`/home/isp/wsps/private-maintenance/cyf-local-archive-20261107-*`。历史安装record原路径不改写，仍绑定的内存盘原件保留。

现有维护工具已安装并回读，支持原生API schema4/Web schema2、完成包登记及组合输出组件子根；4个完成任务已进入原registry。维护隔离回归61+67+41+84=253项。原每30分钟cron实际入口已执行，清理末尾不再递归du长持锁；最终exit3准确表示容量仍低于5GiB、没有可删候选，非未知schema失败。持久化亦占用磁盘，当前仅约1GiB余量，下一批必须复核备份峰值，不能宣称磁盘问题完全消除。

当前策略、部署说明、工具README及保留规则已同步本轮状态。具体安装/清理/登记/验证见`docs/implementation/evidence/local-release-closure-20261107/`；版本化结果以`version-control.json`实际远端回读为准。本轮无新应用构建、部署、重启或Flow，不覆盖原435.314秒成绩，也不将它泛化为未来冷构建保证。
'''
for name in ['LOCAL-BUILD-TIMING-20261106.md','LOCAL-BUILD-RETENTION-10M-20261106.md']:
 p=R/'docs/implementation/handoffs'/name;p.write_text(p.read_text()+note)
