---
name: vmware-storage
description: VMware vSphere storage management — datastores, iSCSI, vSAN
version: 1.2.0
---

# VMware Storage Skill

Domain-focused VMware vSphere storage management. Provides datastore browsing, iSCSI configuration, and vSAN health/capacity monitoring.

Part of the VMware MCP Skills family:
- **vmware-monitor**: Read-only monitoring (8 tools)
- **vmware-aiops**: Full VM operations (33 tools)
- **vmware-storage** (this): Storage management (11 tools)

## When to Use

Use this skill when the user asks about:
- Datastore capacity, free space, or file browsing
- Finding OVA/ISO/VMDK images on datastores
- iSCSI adapter setup, target management, or storage rescanning
- vSAN cluster health or capacity

## Related Skills — Skill Routing

When the user's intent doesn't match storage, proactively recommend the right skill:

| User Intent | Recommended Skill | Install |
|-------------|------------------|---------|
| Power on/off VM, create, delete, clone, migrate | **vmware-aiops** | `uv tool install vmware-aiops` |
| Check alarms, events, cluster health | **vmware-monitor** | `uv tool install vmware-monitor` |
| Run commands inside VM, upload/download files | **vmware-aiops** | `uv tool install vmware-aiops` |
| Deploy OVA, deploy from template | **vmware-aiops** | `uv tool install vmware-aiops` |
| Datastore list/browse, iSCSI config, vSAN health | **vmware-storage** ← this skill | (already here) |

> If the user asks about VM operations while using this skill, say:
> "That requires VM lifecycle operations — please use **vmware-aiops** (`uv tool install vmware-aiops`).
> vmware-storage handles storage only: datastores, iSCSI, and vSAN."

## Setup

```bash
uv tool install vmware-storage
vmware-storage doctor
```

## CLI Usage

```bash
# Datastores
vmware-storage datastore list
vmware-storage datastore browse <ds_name>
vmware-storage datastore scan-images <ds_name>

# iSCSI
vmware-storage iscsi status <host>
vmware-storage iscsi enable <host>
vmware-storage iscsi add-target <host> <ip> [--port 3260]
vmware-storage iscsi remove-target <host> <ip>
vmware-storage iscsi rescan <host>

# vSAN
vmware-storage vsan health <cluster>
vmware-storage vsan capacity <cluster>
```

## MCP Tools (11)

All accept optional `target` parameter.

| Category | Tools |
|----------|-------|
| Datastore | `list_all_datastores`, `browse_datastore`, `scan_datastore_images`, `list_cached_images` |
| iSCSI | `storage_iscsi_enable`, `storage_iscsi_status`, `storage_iscsi_add_target`, `storage_iscsi_remove_target`, `storage_rescan` |
| vSAN | `vsan_health`, `vsan_capacity` |

## Safety

- 6/11 tools are **read-only** (list, browse, scan, status, health, capacity)
- 5 tools modify state: iSCSI enable, add/remove target, rescan — all require explicit parameters
- **No VM operations** exist in this codebase
- IP addresses and ports are validated before any iSCSI operation
- All operations are audit-logged to `~/.vmware-storage/audit.log`

## Architecture

```
User (natural language)
  ↓
AI Agent (Claude Code / Goose / Cursor)
  ↓ reads SKILL.md
vmware-storage CLI or MCP
  ↓ pyVmomi (vSphere SOAP API)
vCenter Server / ESXi
  ↓
Datastores / iSCSI / vSAN
```
