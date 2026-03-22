"""vmware-storage CLI — Datastore, iSCSI, and vSAN management."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from vmware_storage.config import load_config
from vmware_storage.connection import ConnectionManager

app = typer.Typer(
    name="vmware-storage",
    help="VMware vSphere storage management: datastores, iSCSI, vSAN.",
    no_args_is_help=True,
)

console = Console()


# ---------------------------------------------------------------------------
# Shared options
# ---------------------------------------------------------------------------


def _get_connection(target: str | None, config_path: str | None = None):
    config = load_config(Path(config_path) if config_path else None)
    conn_mgr = ConnectionManager(config)
    return conn_mgr.connect(target)


def _print_json(data) -> None:
    console.print_json(json.dumps(data, default=str, ensure_ascii=False))


# ---------------------------------------------------------------------------
# Datastore commands
# ---------------------------------------------------------------------------

ds_app = typer.Typer(help="Datastore browsing and image discovery.")
app.add_typer(ds_app, name="datastore")


@ds_app.command("list")
def ds_list(
    target: str | None = typer.Option(None, help="Target name"),
    config: str | None = typer.Option(None, "--config", help="Config file path"),
) -> None:
    """List all datastores with capacity info."""
    from vmware_storage.ops.inventory import list_datastores
    si = _get_connection(target, config)
    result = list_datastores(si)
    table = Table(title="Datastores")
    table.add_column("Name", style="bold")
    table.add_column("Type")
    table.add_column("Total GB", justify="right")
    table.add_column("Free GB", justify="right")
    table.add_column("Usage %", justify="right")
    table.add_column("VMs", justify="right")
    for ds in result:
        usage_style = "red" if ds["usage_pct"] > 85 else ""
        table.add_row(
            ds["name"], ds["type"],
            str(ds["total_gb"]), str(ds["free_gb"]),
            f"[{usage_style}]{ds['usage_pct']}%[/]",
            str(ds["vm_count"]),
        )
    console.print(table)


@ds_app.command("browse")
def ds_browse(
    ds_name: str = typer.Argument(help="Datastore name"),
    path: str = typer.Option("", help="Subdirectory path"),
    pattern: str = typer.Option("*", help="Glob pattern"),
    target: str | None = typer.Option(None, help="Target name"),
    config: str | None = typer.Option(None, "--config", help="Config file path"),
) -> None:
    """Browse files in a datastore."""
    from vmware_storage.ops.datastore_browser import browse_datastore
    si = _get_connection(target, config)
    result = browse_datastore(si, ds_name, path=path, pattern=pattern)
    _print_json(result)


@ds_app.command("scan-images")
def ds_scan_images(
    ds_name: str = typer.Argument(help="Datastore name"),
    target: str | None = typer.Option(None, help="Target name"),
    config: str | None = typer.Option(None, "--config", help="Config file path"),
) -> None:
    """Scan a datastore for deployable images (OVA/ISO/OVF/VMDK)."""
    from vmware_storage.ops.datastore_browser import scan_images
    si = _get_connection(target, config)
    result = scan_images(si, ds_name)
    _print_json(result)


# ---------------------------------------------------------------------------
# iSCSI commands
# ---------------------------------------------------------------------------

iscsi_app = typer.Typer(help="iSCSI adapter and target management.")
app.add_typer(iscsi_app, name="iscsi")


@iscsi_app.command("enable")
def iscsi_enable(
    host_name: str = typer.Argument(help="ESXi host name"),
    target: str | None = typer.Option(None, help="Target name"),
    config: str | None = typer.Option(None, "--config", help="Config file path"),
) -> None:
    """Enable software iSCSI adapter on a host."""
    from vmware_storage.ops.iscsi_config import enable_software_iscsi
    si = _get_connection(target, config)
    console.print(enable_software_iscsi(si, host_name))


@iscsi_app.command("status")
def iscsi_status(
    host_name: str = typer.Argument(help="ESXi host name"),
    target: str | None = typer.Option(None, help="Target name"),
    config: str | None = typer.Option(None, "--config", help="Config file path"),
) -> None:
    """Show iSCSI adapter status and targets."""
    from vmware_storage.ops.iscsi_config import get_iscsi_status
    si = _get_connection(target, config)
    _print_json(get_iscsi_status(si, host_name))


@iscsi_app.command("add-target")
def iscsi_add_target(
    host_name: str = typer.Argument(help="ESXi host name"),
    address: str = typer.Argument(help="iSCSI target IP address"),
    port: int = typer.Option(3260, help="iSCSI target port"),
    target: str | None = typer.Option(None, help="Target name"),
    config: str | None = typer.Option(None, "--config", help="Config file path"),
) -> None:
    """Add an iSCSI send target."""
    from vmware_storage.ops.iscsi_config import add_iscsi_target
    si = _get_connection(target, config)
    console.print(add_iscsi_target(si, host_name, address, port))


@iscsi_app.command("remove-target")
def iscsi_remove_target(
    host_name: str = typer.Argument(help="ESXi host name"),
    address: str = typer.Argument(help="iSCSI target IP address"),
    port: int = typer.Option(3260, help="iSCSI target port"),
    target: str | None = typer.Option(None, help="Target name"),
    config: str | None = typer.Option(None, "--config", help="Config file path"),
) -> None:
    """Remove an iSCSI send target."""
    from vmware_storage.ops.iscsi_config import remove_iscsi_target
    si = _get_connection(target, config)
    console.print(remove_iscsi_target(si, host_name, address, port))


@iscsi_app.command("rescan")
def iscsi_rescan(
    host_name: str = typer.Argument(help="ESXi host name"),
    target: str | None = typer.Option(None, help="Target name"),
    config: str | None = typer.Option(None, "--config", help="Config file path"),
) -> None:
    """Rescan all HBAs and VMFS volumes."""
    from vmware_storage.ops.iscsi_config import rescan_storage
    si = _get_connection(target, config)
    console.print(rescan_storage(si, host_name))


# ---------------------------------------------------------------------------
# vSAN commands
# ---------------------------------------------------------------------------

vsan_app = typer.Typer(help="vSAN health and capacity monitoring.")
app.add_typer(vsan_app, name="vsan")


@vsan_app.command("health")
def vsan_health_cmd(
    cluster_name: str = typer.Argument(help="Cluster name"),
    target: str | None = typer.Option(None, help="Target name"),
    config: str | None = typer.Option(None, "--config", help="Config file path"),
) -> None:
    """Get vSAN cluster health summary."""
    from vmware_storage.ops.vsan import get_vsan_health
    si = _get_connection(target, config)
    _print_json(get_vsan_health(si, cluster_name))


@vsan_app.command("capacity")
def vsan_capacity_cmd(
    cluster_name: str = typer.Argument(help="Cluster name"),
    target: str | None = typer.Option(None, help="Target name"),
    config: str | None = typer.Option(None, "--config", help="Config file path"),
) -> None:
    """Get vSAN capacity overview."""
    from vmware_storage.ops.vsan import get_vsan_capacity
    si = _get_connection(target, config)
    _print_json(get_vsan_capacity(si, cluster_name))


# ---------------------------------------------------------------------------
# Doctor
# ---------------------------------------------------------------------------


@app.command()
def doctor(
    skip_auth: bool = typer.Option(False, "--skip-auth", help="Skip auth check"),
) -> None:
    """Run environment diagnostics."""
    from vmware_storage.doctor import run_doctor
    sys.exit(run_doctor(skip_auth=skip_auth))
