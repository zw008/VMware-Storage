---
name: vmware-storage
description: >
  VMware vSphere storage management: datastores, iSCSI, vSAN.
  Domain-focused skill split from vmware-aiops for lighter context and local model compatibility.
  11 MCP tools: datastore browsing, iSCSI adapter/target config, vSAN health/capacity monitoring.
installer:
  kind: uv
  package: vmware-storage
metadata: {"openclaw":{"requires":{"env":["VMWARE_STORAGE_CONFIG"],"bins":["vmware-storage"],"config":["~/.vmware-storage/config.yaml","~/.vmware-storage/.env"]},"primaryEnv":"VMWARE_STORAGE_CONFIG","homepage":"https://github.com/zw008/VMware-Storage","emoji":"🗄️","os":["macos","linux"]}}
---

# VMware Storage

VMware vSphere storage management — 11 MCP tools for datastores, iSCSI, and vSAN. Lightweight and local-model friendly (split from vmware-aiops for focused use).

## What This Skill Does

| Category | Tools | Type |
|----------|-------|------|
| **Datastore** | list all datastores, browse files, scan for OVA/ISO/VMDK images, list cached images | Read-only |
| **iSCSI** | enable adapter, show status, add target, remove target, rescan HBAs | Read + Write |
| **vSAN** | cluster health summary, capacity overview (total/used/free) | Read-only |

## Quick Install

```bash
uv tool install vmware-storage
vmware-storage doctor
```

## When to Use

- Datastore capacity, free space, file browsing
- Finding OVA/ISO/VMDK images on datastores
- iSCSI adapter setup, target management, or storage rescanning
- vSAN cluster health or capacity

## Related Skills — Skill Routing

> Need VM operations or monitoring? Use the right skill:

| User Intent | Recommended Skill | Install |
|-------------|------------------|---------|
| Datastores, iSCSI, vSAN ← | **vmware-storage** (this skill) | — |
| Read-only monitoring, alarms, events | **vmware-monitor** | `uv tool install vmware-monitor` |
| Power on/off VM, create, delete, deploy OVA | **vmware-aiops** | `uv tool install vmware-aiops` |
| Run commands inside VM, upload files | **vmware-aiops** | `uv tool install vmware-aiops` |

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
