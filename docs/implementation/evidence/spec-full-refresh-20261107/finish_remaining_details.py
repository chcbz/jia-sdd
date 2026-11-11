from pathlib import Path
import json, hashlib, re, sys
from urllib.parse import urlsplit,unquote
R=Path('/home/isp/wsps/cyf'); E=R/'docs/implementation/evidence/spec-full-refresh-20261107'
def edit(n,a,b):
 p=R/n; old=p.read_text(); assert a in old,n
 o=E/'originals'/(n+'.txt'); o.parent.mkdir(parents=True,exist_ok=True)
 if not o.exists():o.write_text(old)
 p.write_text(old.replace(a,b))
p='specs/juyiting-skill-execution/management-mvp.md'
a='| 开工后 | 工作 | 到点应拿到什么 |\n| --- | --- | --- |\n> 以下四小时排程与其Flow资源条件是原任务历史计划，不是当前执行前置条件；现行实施按下节本地验证和实际候选安排，不重启历史排程。\n\n'
b='> 以下四小时排程与其Flow资源条件是原任务历史计划，不是当前执行前置条件；现行实施按下节本地验证和实际候选安排，不重启历史排程。\n\n| 开工后 | 工作 | 到点应拿到什么 |\n| --- | --- | --- |\n'
edit(p,a,b)
edit('specs/juyiting-external-commission-mvp/tasks.md','正式构建/部署统一Flow，develop不自动部署。','正式测试/构建/打包默认本地固定干净源码与独立输出，发布沿实际授权和既有受控入口；develop不自动部署。')
edit('specs/juyiting-agent-skill-display/acceptance.md','正式测试和生产构建必须Flow4403172，绑定同run制品，不回退本机生产打包。','正式测试和生产构建默认在本地固定干净源码/独立输出执行，绑定真实批次、完整commit/tree、测试及制品SHA-256；安装、健康、业务验收分别记录。')
edit('specs/api-performance-3s-slo/tasks.md','SSE/AI 首帧、异步 ACK、文件 TTFB 使用专用门禁并有异常场景。','SSE/AI首帧、异步ACK、文件TTFB按各自观测口径记录，并验证真实错误/取消场景；不因性能目标拒绝或截流。')
edit('specs/api-performance-3s-slo/spec.md','这些接口承诺的是 ACK、响应头或首个应用数据帧在 3 秒内到达。','这些接口以ACK、响应头或首个应用帧3秒内到达为观测目标，不作为强制超时承诺。')
