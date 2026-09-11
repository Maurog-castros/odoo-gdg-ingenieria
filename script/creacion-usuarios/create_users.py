#!/usr/bin/env python3
"""Create the functional test users used by the Odoo project."""

import argparse
import json
import os
import sys
import urllib.request
import xmlrpc.client
from pathlib import Path


USERS = [
    ("crm.user", "Usuario CRM", "crm.user@example.com", ("crm.group_crm_user",)),
    ("sales.user", "Usuario Ventas", "sales.user@example.com", ("sales_team.group_sale_salesman",)),
    ("sales.manager", "Responsable Ventas", "sales.manager@example.com", ("sales_team.group_sale_manager",)),
    ("purchase.user", "Usuario Compras", "purchase.user@example.com", ("purchase.group_purchase_user",)),
    ("purchase.manager", "Responsable Compras", "purchase.manager@example.com", ("purchase.group_purchase_manager",)),
    ("inventory.user", "Usuario Inventario", "inventory.user@example.com", ("stock.group_stock_user",)),
    ("inventory.manager", "Responsable Inventario", "inventory.manager@example.com", ("stock.group_stock_manager",)),
    ("invoicing.user", "Usuario Facturacion", "invoicing.user@example.com", ("account.group_account_invoice",)),
    ("accounting.user", "Usuario Contabilidad", "accounting.user@example.com", ("account.group_account_user",)),
    ("project.user", "Usuario Proyectos", "project.user@example.com", ("project.group_project_user",)),
]


def load_env(path):
    values = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip("\"'")
    return values


def rpc_call(url, database, uid, password, model, method, args, kwargs=None):
    proxy = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
    return proxy.execute_kw(database, uid, password, model, method, args, kwargs or {})


def find_group_id(url, database, uid, password, xmlid):
    module, name = xmlid.split(".", 1)
    records = rpc_call(
        url,
        database,
        uid,
        password,
        "ir.model.data",
        "search_read",
        [[("module", "=", module), ("name", "=", name), ("model", "=", "res.groups")]],
        {"fields": ["res_id"], "limit": 1},
    )
    if not records:
        raise RuntimeError(f"No se encontro el grupo Odoo {xmlid}")
    return records[0]["res_id"]


def discover_database(url):
    with urllib.request.urlopen(f"{url}/web/database/list", timeout=20) as response:
        payload = json.loads(response.read().decode("utf-8"))
    databases = payload.get("result", [])
    if not databases:
        raise RuntimeError("Odoo no ha devuelto ninguna base de datos")
    if len(databases) > 1:
        raise RuntimeError("Hay varias bases de datos; define ODOO_DB en .env")
    return databases[0]


def main():
    parser = argparse.ArgumentParser(description="Crea los 10 usuarios funcionales de Odoo.")
    parser.add_argument("--env", default=".env", help="Ruta al archivo .env (por defecto: .env)")
    parser.add_argument("--dry-run", action="store_true", help="Comprueba grupos y usuarios sin crear cambios")
    args = parser.parse_args()

    env_path = Path(args.env)
    if not env_path.exists():
        raise RuntimeError(f"No existe el archivo de entorno: {env_path}")

    config = load_env(env_path)
    url = config.get("URLODOO", "").rstrip("/")
    admin_login = config.get("ADMIN-USER", "")
    admin_password = config.get("PASS", "")
    user_password = config.get("USER_PASSWORD") or os.environ.get("USER_PASSWORD")
    database = config.get("ODOO_DB", "")

    if not url or not admin_login or not admin_password:
        raise RuntimeError(".env debe contener URLODOO, ADMIN-USER y PASS")
    if not user_password and not args.dry_run:
        raise RuntimeError("Define USER_PASSWORD en .env o en el entorno antes de crear usuarios")

    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    if not database:
        database = discover_database(url)

    uid = common.authenticate(database, admin_login, admin_password, {})
    if not uid:
        raise RuntimeError("No se pudo autenticar el usuario administrador")

    group_ids = {}
    for _, _, _, group_xmlids in USERS:
        for group_xmlid in group_xmlids:
            group_ids[group_xmlid] = find_group_id(url, database, uid, admin_password, group_xmlid)

    existing = rpc_call(
        url,
        database,
        uid,
        admin_password,
        "res.users",
        "search_read",
        [[("login", "in", [user[0] for user in USERS])]],
        {"fields": ["login", "name"], "limit": len(USERS)},
    )
    existing_logins = {user["login"] for user in existing}

    for login, name, email, group_xmlids in USERS:
        if login in existing_logins:
            print(f"EXISTE  {login:18} {name}")
            continue
        print(f"CREAR   {login:18} {name}")
        if not args.dry_run:
            rpc_call(
                url,
                database,
                uid,
                admin_password,
                "res.users",
                "create",
                [{
                    "name": name,
                    "login": login,
                    "email": email,
                    "password": user_password,
                    "groups_id": [(6, 0, [group_ids[group] for group in group_xmlids])],
                }],
            )

    print("Simulacion completada." if args.dry_run else "Usuarios procesados correctamente.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, xmlrpc.client.Fault, xmlrpc.client.ProtocolError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)