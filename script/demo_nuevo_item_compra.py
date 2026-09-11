#!/usr/bin/env python3
"""Demonstrate creating a new purchase item and reusing it in a later order."""

import argparse
import json
import sys
import urllib.request
import xmlrpc.client
from pathlib import Path


PRODUCT_NAME = "Demo - Kit de pruebas de aislamiento 23 kV"
PRODUCT_CODE = "DEMO-KIT-23KV"
FIRST_ORDER = "DEMO-OC-NUEVO-ITEM-001"
SECOND_ORDER = "DEMO-OC-NUEVO-ITEM-002"
VENDOR_NAME = "Proveedor Demo Equipos Electricos"


def load_env(path):
    values = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip("\"'")
    return values


def call(url, database, uid, password, model, method, args, kwargs=None):
    proxy = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
    return proxy.execute_kw(database, uid, password, model, method, args, kwargs or {})


def database_from_url(url):
    with urllib.request.urlopen(f"{url}/web/database/list", timeout=20) as response:
        databases = json.loads(response.read().decode("utf-8")).get("result", [])
    if len(databases) != 1:
        raise RuntimeError("Define ODOO_DB en .env cuando Odoo tenga cero o varias bases")
    return databases[0]


def find_id(url, database, uid, password, model, domain):
    ids = call(url, database, uid, password, model, "search", [domain], {"limit": 1})
    return ids[0] if ids else None


def get_or_create_product(url, database, uid, password, dry_run):
    product_id = find_id(url, database, uid, password, "product.template", [("default_code", "=", PRODUCT_CODE)])
    if product_id:
        print(f"EXISTE  product.template  {PRODUCT_CODE} - {PRODUCT_NAME}")
        return product_id
    print(f"CREAR   product.template  {PRODUCT_CODE} - {PRODUCT_NAME}")
    if dry_run:
        return None
    return call(
        url,
        database,
        uid,
        password,
        "product.template",
        "create",
        [{
            "name": PRODUCT_NAME,
            "default_code": PRODUCT_CODE,
            "type": "consu",
            "purchase_ok": True,
            "sale_ok": False,
            "list_price": 850000,
            "standard_price": 650000,
            "description_purchase": "Kit ficticio para demostrar la creacion de un item desde Compras.",
        }],
    )


def get_or_create_order(url, database, uid, password, name, vendor_id, product_id, dry_run):
    order_id = find_id(url, database, uid, password, "purchase.order", [("name", "=", name)])
    if order_id:
        print(f"EXISTE  purchase.order    {name}")
        return order_id
    print(f"CREAR   purchase.order    {name}")
    if dry_run:
        return None
    product_variant = call(
        url,
        database,
        uid,
        password,
        "product.product",
        "search",
        [[("product_tmpl_id", "=", product_id)]],
        {"limit": 1},
    )
    if not product_variant:
        raise RuntimeError("El producto no tiene una variante disponible")
    return call(
        url,
        database,
        uid,
        password,
        "purchase.order",
        "create",
        [{
            "name": name,
            "partner_id": vendor_id,
            "order_line": [(0, 0, {
                "product_id": product_variant[0],
                "product_qty": 2,
                "price_unit": 650000,
                "name": PRODUCT_NAME,
            })],
        }],
    )


def main():
    parser = argparse.ArgumentParser(description="Demuestra un item nuevo reutilizado en dos ordenes de compra.")
    parser.add_argument("--env", default="script/creacion-usuarios/.env")
    parser.add_argument("--dry-run", action="store_true", help="Muestra los cambios sin crear registros")
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
    if not uid:
        raise RuntimeError("No se pudo autenticar el usuario administrador")

    vendor_id = find_id(url, database, uid, password, "res.partner", [("name", "=", VENDOR_NAME)])
    if not vendor_id:
        raise RuntimeError(f"No existe el proveedor demo: {VENDOR_NAME}. Ejecuta primero seed_demo_data.py")

    product_id = get_or_create_product(url, database, uid, password, args.dry_run)
    if product_id or args.dry_run:
        get_or_create_order(url, database, uid, password, FIRST_ORDER, vendor_id, product_id, args.dry_run)
        get_or_create_order(url, database, uid, password, SECOND_ORDER, vendor_id, product_id, args.dry_run)

    print("Simulacion completada." if args.dry_run else "Demo de item nuevo completada.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, xmlrpc.client.Fault, xmlrpc.client.ProtocolError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)