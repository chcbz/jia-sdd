# Runtime 原生 HTTP 网关

2026-10-11 核对 API `cf1402727466e1e51db0860200dc178eab2096c4` 的
`AgentRuntimeAuthenticationFilter.allowed`；本目录是网关配置源码，不是前后端应用发布。

- 将两个 `.conf` 固定摘要后安装到 `/home/isp/apps/nginx/conf/snippets/`。
- 仅在 `/home/isp/apps/nginx/conf/vhost/api.chaoyoufan.cn.conf` 的 server 块 include
  `/home/isp/apps/nginx/conf/snippets/cyf-runtime-native-locations.conf`。
- 保留既有 `/agent`、`/ws` 及默认拒绝路由；不代理整个 `/internal`。
- 只转发允许路径和方法；Authorization、五个 X-Agent 证明头、Origin 与重复头不改写。
  Runtime/session/channel/owner/task 的权限仍由后端核对。浏览器 CORS 不开放此 native 通道。
- 沿用现有 100m 主配置上传限制及代理超时；本变更不新增包大小/资源门禁。
- 生产变更在现有 coordinator→API release 锁内备份、核对前值、安装，`nginx -t` 后 reload；
  失败只恢复本次精确文件前值，不重启后端、Runtime或强杀旧worker。
- 定向静态测试：`python3 -B -m unittest discover -s ops/ci/aliyun-flow/tests -p test_runtime_native_nginx.py -v`。
  静态测试不代替实际公网鉴权与业务验收。后端白名单变化必须同步核对本配置。
- 已实测李逵公网轮询200、无凭据/伪凭据/普通用户JWT拒绝；通用文件交付尚未通过。
  具体范围与证据见 `docs/implementation/handoffs/LIKUI-SELFHOST-20261011.md`，不能将此当作全能力开通。
