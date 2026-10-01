# 本机隔离机制可行性探查（非引擎验收）

2026-10-02 主控实测；没有Provider调用、没有启用profile、没有应用源码改动或服务配置修改。

- 当前主机 `bwrap 0.4.0` 能建立最小 mount/user/network 等 namespace；命令见记录。
- v1 在执行 Python 前失败：`/usr/bin/python3` 经 `/etc/alternatives/python3` 指向未挂载目录。保留 exit=1 原始记录，不计测试成功。
- v2 改用实测解析后的 `/usr/libexec/platform-python3.6`，不扩大挂载范围，exit=0。实际输入可读、写入返回 EROFS、主机工作空间及本探针外部canary不可见。
- `network_interfaces=not_mounted` 仅指 `/sys` 未挂载，**不是网络连通性负向验证**。没有测试Provider出站代理或工具网络。
- 此探查只排除“本机根本无法建立这种隔离”的阻碍。未证明真实native Agent启动、工具目录、资料理解、恶意输入隔离、恢复或server/local双模式通过。不得据此广告 `STRICT_NO_TOOLS` 或 `MANIFEST_READ_ONLY` 就绪。

下一步：高风险Client Owner在真实引擎profile实现中绑定必要运行资源、最小资料视图和Provider连接边界，再进行原生启动/负向/四种载体验证。避免为解决某个程序的符号链接直接挂载整个主机根或秘密目录。
