#!/usr/bin/env python3
"""Inspect Odoo Purchase capabilities without modifying business data."""

import argparse
import json
import sys
import urllib.request
import xmlrpc.client
from pathlib import Path


MODELS = {
    "purchase.order": ("name", "partner_id", "user_id", "state", "date_order", "date_approve", "date_calendar_start", "receipt_status", "partner_ref", "origin", "notes", "order_line", "picking_ids"),
    "purchase.order.line": ("order_id", "product_id", "name", "product_qty", "qty_received", "qty_invoiced", "price_unit", "discount", "date_planned", "analytic_distribution", "taxes_id"),
    "product.template": ("name", "default_code", "categ_id", "type", "purchase_ok", "sale_ok", "standard_price", "purchase_method", "seller_ids"),
    "product.category": ("name", "parent_id"),
    "product.supplierinfo": ("partner_id", "product_tmpl_id", "min_qty", "price", "delay", "currency_id"),
    "stock.picking": ("name", "partner_id", "scheduled_date", "date_deadline", "state", "origin", "move_ids"),
    "stock.move": ("product_id", "product_uom_qty", "quantity", "picked", "state", "date_deadline", "picking_id"),
    "purchase.requisition": ("name", "vendor_id", "state", "date_end", "ordering_date", "line_ids", "type_id"),
    "purchase.requisition.line": ("requisition_id", "product_id", "product_qty", "price_unit", "schedule_date"),
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
    parser = argparse.ArgumentParser(description="Inspecciona funciones disponibles de Compras sin modificar Odoo.")
    parser.add_argument("--env", default="script/creacion-usuarios/.env")
    args = parser.parse_args()
    config = load_env(Path(args.env))
    url = config.get("URLODOO", "").rstrip("/")
    admin, password = config.get("ADMIN-USER", ""), config.get("PASS", "")
    database = config.get("ODOO_DB") or database_from_url(url)
    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(database, admin, password, {})
    if not uid:
        raise RuntimeError("No se pudo autenticar el usuario administrador")
    installed_rows = rpc(url, database, uid, password, "ir.model", "search_read", [[("model", "in", list(MODELS))]], {"fields": ["model"]})
    installed = {row["model"] for row in installed_rows}
    print(f"Odoo {common.version().get('server_version', 'desconocida')} · Compras")
    for model, requested in MODELS.items():
        if model not in installed:
            print(f"NO  {model}")
            continue
        fields = rpc(url, database, uid, password, model, "fields_get", [], {"attributes": ["type", "readonly", "required", "selection"]})
        details = []
        for name in requested:
            meta = fields.get(name)
            if not meta:
                continue
            flags = ("*" if meta.get("required") else "") + ("[solo lectura]" if meta.get("readonly") else "")
            selection = meta.get("selection")
            choices = f"={','.join(value for value, _label in selection)}" if isinstance(selection, list) else ""
            details.append(f"{name}:{meta.get('type')}{flags}{choices}")
        print(f"SI  {model}: {', '.join(details)}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, xmlrpc.client.Fault, xmlrpc.client.ProtocolError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
