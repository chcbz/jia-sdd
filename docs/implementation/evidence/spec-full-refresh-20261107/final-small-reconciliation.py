from pathlib import Path
R=Path('/home/isp/wsps/cyf'); E=R/'docs/implementation/evidence/spec-full-refresh-20261107'
def edit(n,a,b):
 p=R/n; old=p.read_text(); assert a in old,n
 o=E/'originals'/(n+'.txt');o.parent.mkdir(parents=True,exist_ok=True)
 if not o.exists():o.write_text(old)
 p.write_text(old.replace(a,b))
edit('specs/api-performance-3s-slo/acceptance.md','预算耗尽、依赖断开、连接池耗尽、慢 SQL 和客户端取消不会产生重复写或未知事务；若不可避免则返回可查询 operation ID。','性能目标耗尽不触发取消；真实依赖断开、连接池耗尽、慢SQL和客户端取消按既有事务/幂等处理，不引入重复写。提交结果未知沿已有权威状态查询恢复，不仅为优化新建operation框架。')
edit('specs/api-performance-3s-slo/acceptance.md','缓存键和失效策略使用无歧义编码覆盖 tenant/jiacn、client_id、task/资源 scope、owner/principal、subject、ACL-policy/data version，全部 byte-exact；无跨租户、client、task、owner 或用户数据泄漏。','缓存键/失效覆盖该缓存实际依赖的租户、主体、资源及权限/数据版本，使用无歧义编码，不机械给公共定义缓存复制全部scope。由所属边界验证无越权泄漏，不逐帧重新鉴权或完整hash历史。')
edit('specs/api-performance-3s-slo/design.md','权限相关数据 -> 使用无歧义编码的 tenant/jiacn + client_id + task/资源 scope + owner/principal + subject + ACL-policy/data version，全维度 byte-exact。','权限相关数据 -> 按真实访问范围与失效来源选择租户/主体/资源/权限或数据版本，无歧义编码；公共定义不机械套所有scope，同一可信边界不重复校验。')
edit('ops/orchestration/README.md','**既有实现差异待修正**：旧说明中的构建单元`RuntimeMaxSec`按剩余预算终止构建与根规则冲突，不是当前规范授权；本轮仅整理文档，未修正或实测该工具。','**已只读核实的实现差异（2026-11-07，待修正）**：`ops/orchestration/local_release.py`的`remaining()`及`run(build=True)`会将600秒剩余预算用于阶段拒绝和`RuntimeMaxSec`构建终止，与根规则冲突，不是当前规范授权；本轮仅整理文档，未修正或执行该工具。')
(E/'final-small-reconciliation.py').write_text(Path(__file__).read_text())
