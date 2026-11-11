from pathlib import Path
import hashlib,json
R=Path('/home/isp/wsps/cyf');E=R/'docs/implementation/evidence/local-release-closure-20261107';B=E/'directory-layout-before'
section='''## 2026-11-07：本地构建与开发目录职责归位

- `apps`放工具链：构建JDK为`/home/isp/apps/dragonwell-21.0.11.0.11+10-GA`，生产Temurin不变。
- `pkgs`放安装包归档：API当前/回退及Web当前镜像已移至`/home/isp/pkgs/cyf/cyf-local-archive-20261107-{api-current,api-rollback,web-current}/package/`。不把包或备份放入开发目录。
- `state`放构建状态及缓存：`/home/isp/state/cyf-local-build/gradle-home`；后续临时构建任务使用`/home/isp/state/cyf-local-build/tasks/cyf-BATCH`，最终归档放pkgs，不将构建目录当永久备份。
- `baks`放历史维护备份及证据：旧`/home/isp/wsps/private-maintenance`剩余13个历史任务已原子迁至`/home/isp/baks/private-maintenance`；2094项原文件/目录的字节、权限、所有者及inode完整核对，无载荷复制、删除或服务重启。旧wsps入口不留软链接。
- `wsps`只放项目源码和开发工作副本。后续新增工作树按所属项目放在`<项目>/.worktrees/`，不再创建共享的顶层`worktrees`、`cyf-worktrees`或用于运维归档的`private-maintenance`。工作树用于隔离分支、不是独立服务，也不需要两个不同名称的顶层目录。
- `/home/isp/wsps/cyf-worktrees`为空且无占用、挂载，已删除。`/home/isp/wsps/worktrees`仍有15个任务目录（12个Git工作树，另3个任务目录），涉及CYF根/API/Web及isp-install，不属于同一个仓库。现有任务未移动、删除或重登记；后续由各Owner确认任务状态后通过Git机制逐项收口，不以目录年龄批量清理。旧共享路径仅保留兼容，禁止继续扩张。
- 完成包登记的3条镜像路径已迁到pkgs，保留原完成时间、源码、摘要和inode；原4条台账记录数不变。现有清理器增加精确pkgs/build-task bases并移除旧private-maintenance base；当前/回退、最近两批、24h、锁和进程使用保护不变。baks下的维护档案不进入最终包清理范围。
- 历史安装record与历史archive.json路径原文保留，不伪造重绑定；原当前/回退内存盘包仍保留。迁移映射、摘要与验证见`/home/isp/wsps/cyf/docs/implementation/evidence/local-release-closure-20261107/directory-layout-migration.json`。不把目录整理当成新的构建或发布。

'''
p=Path('/home/isp/docs/SERVER_ARCHITECTURE.md');before=p.read_bytes();(B/'SERVER_ARCHITECTURE.md').write_bytes(before);(B/'SERVER_ARCHITECTURE.md').chmod(0o600);s=before.decode();head,rest=s.split('\n',1);p.write_text(head+'\n\n'+section+rest.lstrip('\n'))
(R/'ops/maintenance/HOST_DIRECTORY_LAYOUT.md').write_text('# 主机目录职责与本地发布目录（2026-11-07）\n\n主机权威说明：`/home/isp/docs/SERVER_ARCHITECTURE.md`。以下同步当前本任务目录整理事实；历史证据不做路径字符串回写。\n\n'+section)
p=R/'docs/aliyun-flow-cicd-strategy.md';s=p.read_text();a=s.index('### 已验证范围及持久化/清理状态');b=s.index('\n操作参数见',a);chunk=s[a:b].replace('/home/isp/wsps/private-maintenance/','/home/isp/pkgs/cyf/');s=s[:a]+chunk+s[b:];s+='\n### 主机目录职责归位（2026-11-07后续更新）\n\n安装包镜像现位于`/home/isp/pkgs/cyf`；本地构建任务/缓存归`/home/isp/state/cyf-local-build`；旧维护档案归`/home/isp/baks/private-maintenance`，不再使用wsps存放运维归档。工作树按所属项目的`.worktrees`归属；空`cyf-worktrees`已删除，旧共享worktrees的15个任务目录保留待各Owner逐项收口。精确迁移与保留边界见`ops/maintenance/HOST_DIRECTORY_LAYOUT.md`，不将历史安装记录字符串重写成新执行证据。\n';p.write_text(s)
p=R/'ops/orchestration/README.md';s=p.read_text().replace('/home/isp/wsps/private-maintenance/cyf-NEW_BATCH','/home/isp/state/cyf-local-build/tasks/cyf-NEW_BATCH');s+='\n主机目录职责：构建任务及缓存归state、最终包归档归`/home/isp/pkgs/cyf`、历史维护备份归baks，源码/worktree归各项目。当前三个镜像已迁至pkgs，旧wsps/private-maintenance和空cyf-worktrees入口已移除；不通过搬动未完成工作树整理目录。见`ops/maintenance/HOST_DIRECTORY_LAYOUT.md`。\n';p.write_text(s)
p=R/'ops/maintenance/LOCAL_ARTIFACT_RETENTION.md';s=p.read_text();s+='\n## 2026-11-07目录归位更新\n\n完成包显式基目录增加`/home/isp/pkgs/cyf`、`/home/isp/state/cyf-local-build/tasks`，移除`/home/isp/wsps/private-maintenance`；现有共享worktrees仅作历史兼容，不作为新工作树默认根。三个镜像的登记路径已随原子迁移更新，完成时间/摘要/身份不变。baks/private-maintenance是历史维护档案，不纳入最终包扫描。此为目录整理，不改变24h/最近两批/当前回退/进程/锁保护。详见`HOST_DIRECTORY_LAYOUT.md`。\n';p.write_text(s)
record={'hostArchitecturePath':'/home/isp/docs/SERVER_ARCHITECTURE.md','beforeSha256':hashlib.sha256(before).hexdigest(),'afterSha256':hashlib.sha256(Path('/home/isp/docs/SERVER_ARCHITECTURE.md').read_bytes()).hexdigest()};(E/'directory-layout-docs.json').write_text(json.dumps(record,indent=2)+'\n')
