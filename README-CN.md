<!-- mcp-name: io.github.zw008/vmware-storage -->
# VMware Storage

[English](README.md) | [中文](README-CN.md)

面向领域的 VMware vSphere 存储管理 MCP Skill：数据存储、iSCSI、vSAN。

> **VMware MCP Skills 家族：**
>
> | Skill | 范围 | 工具数 |
> |-------|------|:-----:|
> | **vmware-monitor**（只读） | 清单、健康、告警、事件 | 8 |
> | **vmware-aiops**（完整运维） | VM 生命周期、部署、Guest Ops、计划模式 | 33 |
> | **vmware-storage**（本 Skill） | 数据存储、iSCSI、vSAN | 11 |

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 快速安装

```bash
# 通过 PyPI
uv tool install vmware-storage

# 或 pip
pip install vmware-storage
```

## 配置

```bash
mkdir -p ~/.vmware-storage
cp config.example.yaml ~/.vmware-storage/config.yaml
# 编辑 config.yaml，填入 vCenter/ESXi 地址和用户名

echo "VMWARE_MY_VCENTER_PASSWORD=your_password" > ~/.vmware-storage/.env
chmod 600 ~/.vmware-storage/.env

# 验证环境
vmware-storage doctor
```

### config.yaml 示例

```yaml
default_target: vcenter1
targets:
  vcenter1:
    host: 192.168.1.10       # vCenter IP
    user: administrator@vsphere.local
    password_env: VMWARE_VCENTER1_PASSWORD
  esxi-prod:
    host: 192.168.1.20       # 直连 ESXi
    user: root
    password_env: VMWARE_ESXIPROD_PASSWORD
```

## MCP 工具（11 个）

| 类别 | 工具 | 类型 |
|------|------|------|
| 数据存储 | `list_all_datastores`、`browse_datastore`、`scan_datastore_images`、`list_cached_images` | 只读 |
| iSCSI | `storage_iscsi_enable`、`storage_iscsi_status`、`storage_iscsi_add_target`、`storage_iscsi_remove_target`、`storage_rescan` | 读/写 |
| vSAN | `vsan_health`、`vsan_capacity` | 只读 |

### 工具说明

**数据存储**
- `list_all_datastores` — 列出所有数据存储，含容量、使用率、可达性
- `browse_datastore` — 浏览数据存储目录下的文件（支持 glob 过滤）
- `scan_datastore_images` — 扫描可部署镜像（OVA、ISO、OVF、VMDK）
- `list_cached_images` — 查询本地镜像注册表（支持按类型/数据存储过滤）

**iSCSI**
- `storage_iscsi_enable` — 在 ESXi 主机上启用软件 iSCSI 适配器
- `storage_iscsi_status` — 查看 iSCSI 适配器状态和已配置的发送目标
- `storage_iscsi_add_target` — 添加 iSCSI 发送目标并自动重扫
- `storage_iscsi_remove_target` — 移除 iSCSI 发送目标并自动重扫
- `storage_rescan` — 强制重扫所有 HBA 和 VMFS 卷

**vSAN**
- `vsan_health` — 获取 vSAN 集群健康摘要和磁盘组详情
- `vsan_capacity` — 获取 vSAN 容量概览（总量/已用/空闲）

## CLI

```bash
# 数据存储
vmware-storage datastore list
vmware-storage datastore browse datastore01
vmware-storage datastore scan-images datastore01

# iSCSI（破坏性操作有双重确认 + --dry-run 预览）
vmware-storage iscsi status esxi-01
vmware-storage iscsi enable esxi-01 --dry-run
vmware-storage iscsi enable esxi-01
vmware-storage iscsi add-target esxi-01 192.168.1.100 --dry-run
vmware-storage iscsi add-target esxi-01 192.168.1.100
vmware-storage iscsi remove-target esxi-01 192.168.1.100
vmware-storage iscsi rescan esxi-01

# vSAN
vmware-storage vsan health Cluster-Prod
vmware-storage vsan capacity Cluster-Prod

# 环境诊断
vmware-storage doctor
```

## MCP Server

```bash
# 直接运行
python -m mcp_server

# 或通过 Docker
docker compose up -d
```

### Agent 配置

将以下内容添加到 AI Agent 的 MCP 配置文件：

```json
{
  "mcpServers": {
    "vmware-storage": {
      "command": "vmware-storage-mcp",
      "env": {
        "VMWARE_STORAGE_CONFIG": "~/.vmware-storage/config.yaml"
      }
    }
  }
}
```

更多 Agent 配置模板（Claude Code、Cursor、Goose、Continue 等）见 [examples/mcp-configs/](examples/mcp-configs/)。

## 为什么独立成一个 Skill？

`vmware-aiops` 有 33 个 MCP 工具——对本地小模型（7B-14B）来说上下文占用太重。独立拆分后：

- **11 个工具** — 完全适合小模型上下文窗口
- **领域专注** — 存储管理员只看到需要的工具
- **最小权限** — 可以配置只有存储只读权限的 vCenter 服务账号
- **可组合** — 可与 vmware-monitor 或 vmware-aiops 同时运行

## 版本兼容性

| vSphere | 支持 | 说明 |
|---------|------|------|
| 8.0 | 完整 | vSAN SDK 内置于 pyVmomi 8.0.3+ |
| 7.0 | 完整 | 所有存储 API 均可用 |
| 6.7 | 兼容 | iSCSI + 数据存储功能正常；vSAN 功能有限 |

## 安全

| 功能 | 说明 |
|------|------|
| 只读为主 | 11 个工具中 6 个只读 |
| 输入验证 | iSCSI 操作前验证 IP 地址和端口 |
| 审计日志 | 所有操作记录到 `~/.vmware-storage/audit.log`（JSON Lines） |
| 双重确认 | CLI iSCSI 写操作需两次确认 |
| --dry-run | CLI iSCSI 写操作支持预览模式 |
| 无 VM 操作 | 无法创建、删除或修改 VM |
| 凭据安全 | 密码只从环境变量读取，不存于配置文件 |
| Prompt 注入防护 | 来自 vSphere 的文件名和路径经过控制字符清理 |
| TLS 说明 | 默认对 ESXi 自签名证书禁用 TLS 验证；生产环境建议启用 |

## 许可证

[MIT](LICENSE)
