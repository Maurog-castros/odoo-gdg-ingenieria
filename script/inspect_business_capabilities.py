#!/usr/bin/env python3
"""Inspect CRM, Sales, Inventory and Accounting fields without modifying Odoo."""

import argparse
import sys
import xmlrpc.client
from pathlib import Path

from demo_proyecto_gdg import database_from_url, load_env


MODELS = {
    "crm.lead": ("name", "type", "partner_id", "contact_name", "email_from", "phone", "user_id", "team_id", "stage_id", "priority", "expected_revenue", "probability", "date_deadline", "description", "tag_ids", "active", "lost_reason_id"),
    "crm.stage": ("name", "sequence", "is_won", "fold", "team_id"),
    "crm.tag": ("name", "color"),
    "sale.order": ("name", "partner_id", "state", "date_order", "validity_date", "commitment_date", "client_order_ref", "origin", "user_id", "team_id", "order_line", "note", "invoice_status", "delivery_status"),
    "sale.order.line": ("order_id", "product_id", "name", "product_uom_qty", "price_unit", "discount", "qty_delivered", "qty_invoiced", "tax_id"),
    "stock.location": ("name", "location_id", "usage", "active", "barcode"),
    "stock.picking": ("name", "picking_type_id", "location_id", "location_dest_id", "partner_id", "scheduled_date", "state", "origin", "move_ids"),
    "stock.move": ("name", "product_id", "product_uom", "product_uom_qty", "quantity", "picked", "location_id", "location_dest_id", "picking_id", "state"),
    "stock.quant": ("product_id", "location_id", "quantity", "inventory_quantity", "inventory_quantity_set", "inventory_diff_quantity"),
    "stock.lot": ("name", "product_id", "company_id"),
    "account.move": ("name", "move_type", "state", "partner_id", "invoice_date", "invoice_date_due", "invoice_payment_term_id", "invoice_line_ids", "invoice_origin", "payment_state", "amount_total", "ref", "journal_id"),
    "account.move.line": ("move_id", "product_id", "name", "quantity", "price_unit", "discount", "tax_ids", "analytic_distribution", "account_id"),
    "account.payment": ("name", "payment_type", "partner_type", "partner_id", "amount", "date", "journal_id", "payment_method_line_id", "state", "ref"),
    "account.payment.register": ("payment_date", "amount", "journal_id", "payment_method_line_id", "communication"),
}


def rpc(url, database, uid, password, model, method, args, kwargs=None):
    proxy = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
    return proxy.execute_kw(database, uid, password, model, method, args, kwargs or {})


def main():
    parser = argparse.ArgumentParser(description="Inspecciona capacidades empresariales de Odoo.")
    parser.add_argument("--env", default="script/creacion-usuarios/.env")
    args = parser.parse_args()
    config = load_env(Path(args.env))
    url = config.get("URLODOO", "").rstrip("/")
    admin, password = config.get("ADMIN-USER", ""), config.get("PASS", "")
    database = config.get("ODOO_DB") or database_from_url(url)
    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(database, admin, password, {})
    if not uid:
        raise RuntimeError("No se pudo autenticar")
    installed_rows = rpc(url, database, uid, password, "ir.model", "search_read", [[("model", "in", list(MODELS))]], {"fields": ["model"]})
    installed = {row["model"] for row in installed_rows}
    print(f"Odoo {common.version().get('server_version', 'desconocida')}")
    for model, names in MODELS.items():
        if model not in installed:
            print(f"NO  {model}")
            continue
        fields = rpc(url, database, uid, password, model, "fields_get", [], {"attributes": ["type", "readonly", "required", "selection"]})
        details = []
        for name in names:
            meta = fields.get(name)
            if not meta:
                continue
            flags = ("*" if meta.get("required") else "") + ("[ro]" if meta.get("readonly") else "")
            selection = meta.get("selection")
            choices = f"={','.join(v for v, _ in selection)}" if isinstance(selection, list) else ""
            details.append(f"{name}:{meta.get('type')}{flags}{choices}")
        print(f"SI  {model}: {', '.join(details)}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, xmlrpc.client.Fault, xmlrpc.client.ProtocolError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
