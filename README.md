<!-- mcp-name: io.github.zw008/vmware-storage -->
# VMware Storage

[English](README.md) | [中文](README-CN.md)

Domain-focused VMware vSphere storage management: datastores, iSCSI, vSAN.

> **Part of the VMware MCP Skills family:**
>
> | Skill | Scope | Tools |
> |-------|-------|:-----:|
> | **vmware-monitor** (read-only) | Inventory, health, alarms, events | 8 |
> | **vmware-aiops** (full ops) | VM lifecycle, deployment, guest ops, plans | 33 |
> | **vmware-storage** (this) | Datastores, iSCSI, vSAN | 11 |

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Quick Install

```bash
# Via PyPI
uv tool install vmware-storage

# Or pip
pip install vmware-storage
```

## Configuration

```bash
mkdir -p ~/.vmware-storage
cp config.example.yaml ~/.vmware-storage/config.yaml
# Edit with your vCenter/ESXi credentials

echo "VMWARE_MY_VCENTER_PASSWORD=your_password" > ~/.vmware-storage/.env
chmod 600 ~/.vmware-storage/.env

# Verify
vmware-storage doctor
```

## MCP Tools (11)

| Category | Tools | Type |
|----------|-------|------|
| Datastore | `list_all_datastores`, `browse_datastore`, `scan_datastore_images`, `list_cached_images` | Read |
| iSCSI | `storage_iscsi_enable`, `storage_iscsi_status`, `storage_iscsi_add_target`, `storage_iscsi_remove_target`, `storage_rescan` | Read/Write |
| vSAN | `vsan_health`, `vsan_capacity` | Read |

## CLI

```bash
# Datastore
vmware-storage datastore list
vmware-storage datastore browse datastore01
vmware-storage datastore scan-images datastore01

# iSCSI
vmware-storage iscsi status esxi-01
vmware-storage iscsi enable esxi-01
vmware-storage iscsi add-target esxi-01 192.168.1.100
vmware-storage iscsi remove-target esxi-01 192.168.1.100
vmware-storage iscsi rescan esxi-01

# vSAN
vmware-storage vsan health Cluster-Prod
vmware-storage vsan capacity Cluster-Prod

# Diagnostics
vmware-storage doctor
```

## MCP Server

```bash
# Run directly
python -m mcp_server

# Or via Docker
docker compose up -d
```

### Agent Configuration

Add to your AI agent's MCP config:

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

## Why a Separate Skill?

`vmware-aiops` has 33 MCP tools — too heavy for local LLMs (7B-14B). By splitting storage into its own skill:

- **11 tools** — fits comfortably in small model context windows
- **Domain-focused** — storage admins get only what they need
- **Composable** — use alongside vmware-monitor or vmware-aiops as needed

## Version Compatibility

| vSphere | Support | Notes |
|---------|---------|-------|
| 8.0 | Full | vSAN SDK built into pyVmomi 8.0.3+ |
| 7.0 | Full | All storage APIs work |
| 6.7 | Compatible | iSCSI + datastore features work; vSAN limited |

## Safety

| Feature | Description |
|---------|-------------|
| Read-heavy | 6/11 tools are read-only |
| Input validation | IP addresses and ports validated before iSCSI operations |
| Audit logging | All operations logged to `~/.vmware-storage/audit.log` |
| No VM operations | Cannot create, delete, or modify VMs |
| Credential safety | Passwords only from environment variables, never config files |

## License

[MIT](LICENSE)
