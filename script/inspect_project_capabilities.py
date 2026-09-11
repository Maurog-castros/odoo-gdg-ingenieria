#!/usr/bin/env python3
"""Inspect read-only Odoo Project capabilities for demo preparation."""

import argparse
import json
import sys
import urllib.request
import xmlrpc.client
from pathlib import Path


MODELS = (
    "project.project",
    "project.task",
    "project.task.type",
    "project.tags",
    "project.milestone",
    "project.update",
    "account.analytic.line",
    "ir.attachment",
)

INTERESTING_FIELDS = {
    "project.project": ("name", "partner_id", "user_id", "date_start", "date", "tag_ids", "description", "privacy_visibility", "allow_milestones", "allow_task_dependencies", "allow_recurring_tasks", "allow_billable", "allow_timesheets", "sale_order_id", "sale_line_id", "analytic_account_id"),
    "project.task": ("name", "partner_id", "user_ids", "planned_date_begin", "date_deadline", "stage_id", "tag_ids", "priority", "allocated_hours", "parent_id", "depend_on_ids", "milestone_id", "description", "project_id", "sale_order_id", "sale_line_id", "analytic_account_id", "state", "recurring_task", "repeat_interval", "repeat_unit", "repeat_type", "repeat_number", "recurrence_id"),
    "project.task.type": ("name", "sequence", "fold", "project_ids"),
    "project.tags": ("name", "color"),
    "project.milestone": ("name", "deadline", "is_reached", "project_id"),
    "project.update": ("name", "user_id", "date", "progress", "status", "description", "project_id"),
    "account.analytic.line": ("name", "partner_id", "user_id", "employee_id", "date", "unit_amount", "project_id", "task_id"),
    "ir.attachment": ("name", "res_model", "res_id", "mimetype", "type", "description", "datas"),
}


def load_env(path):
    values = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip("\"'")
    return values


def rpc(url, database, uid, password, model, method, args, kwargs=None):
    proxy = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
    return proxy.execute_kw(database, uid, password, model, method, args, kwargs or {})


def database_from_url(url):
    with urllib.request.urlopen(f"{url}/web/database/list", timeout=20) as response:
        databases = json.loads(response.read().decode("utf-8")).get("result", [])
    if len(databases) != 1:
        raise RuntimeError("Define ODOO_DB cuando Odoo tenga cero o varias bases")
    return databases[0]


def main():
    parser = argparse.ArgumentParser(description="Inspecciona funciones disponibles de Proyectos sin modificar Odoo.")
    parser.add_argument("--env", default="script/creacion-usuarios/.env")
    args = parser.parse_args()

    config = load_env(Path(args.env))
    url = config.get("URLODOO", "").rstrip("/")
    admin = config.get("ADMIN-USER", "")
    password = config.get("PASS", "")
    database = config.get("ODOO_DB") or database_from_url(url)
    if not url or not admin or not password:
        raise RuntimeError(".env debe contener URLODOO, ADMIN-USER y PASS")

    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(database, admin, password, {})
    version = common.version().get("server_version", "desconocida")
    if not uid:
        raise RuntimeError("No se pudo autenticar el usuario administrador")

    installed = rpc(url, database, uid, password, "ir.model", "search_read", [[("model", "in", list(MODELS))]], {"fields": ["model"]})
    installed_names = {row["model"] for row in installed}
    print(f"Odoo {version} · base {database}")
    for model in MODELS:
        if model not in installed_names:
            print(f"NO       {model}")
            continue
        fields = rpc(url, database, uid, password, model, "fields_get", [], {"attributes": ["type", "readonly", "required", "selection"]})
        details = []
        for name in INTERESTING_FIELDS[model]:
            meta = fields.get(name)
            if not meta:
                continue
            suffix = "*" if meta.get("required") else ""
            readonly = "[solo lectura]" if meta.get("readonly") else ""
            selection = meta.get("selection")
            choices = f"={','.join(value for value, _label in selection)}" if isinstance(selection, list) else ""
            details.append(f"{name}:{meta.get('type')}{suffix}{choices}{readonly}")
        print(f"SI       {model}: {', '.join(details)}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, xmlrpc.client.Fault, xmlrpc.client.ProtocolError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
