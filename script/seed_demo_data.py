#!/usr/bin/env python3
"""Load functional demo data inspired by GDG Ingenieria's public services."""

import argparse
import json
import sys
import urllib.request
import xmlrpc.client
from pathlib import Path


PARTNERS = [
    ("Cliente Demo Energia Norte", "cliente.energia.norte@example.com", "Antofagasta", "Chile"),
    ("Cliente Demo Mineria Central", "cliente.mineria.central@example.com", "Santiago", "Chile"),
    ("Cliente Demo Transmision Sur", "cliente.transmision.sur@example.com", "Concepcion", "Chile"),
    ("Proveedor Demo Equipos Electricos", "proveedor.equipos@example.com", "Santiago", "Chile"),
]

SERVICES = [
    ("Demo - Montaje de equipos AT/MT", "Construccion y montaje de equipos de alta y media tension."),
    ("Demo - Pruebas electricas y puesta en servicio", "Pruebas de equipos de poder, control y protecciones."),
    ("Demo - Mantencion e inspeccion tecnica", "Mantenimiento preventivo, correctivo e inspeccion tecnica."),
    ("Demo - Tratamiento de aceite de transformador", "Tratamiento y desgasificado de aceite de transformadores."),
]

OPPORTUNITIES = [
    ("Demo - PES subestacion Energia Norte", "Cliente Demo Energia Norte", 18500000, "Pruebas electricas y puesta en servicio de subestacion."),
    ("Demo - Montaje transformador Mineria Central", "Cliente Demo Mineria Central", 42000000, "Montaje y pruebas de transformador de poder."),
    ("Demo - Plan de mantencion Transmision Sur", "Cliente Demo Transmision Sur", 12750000, "Plan de mantenimiento e inspeccion de equipos."),
]


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


def find_one(url, database, uid, password, model, field, value):
    ids = call(url, database, uid, password, model, "search", [[(field, "=", value)]], {"limit": 1})
    return ids[0] if ids else None


def available_models(url, database, uid, password):
    rows = call(
        url,
        database,
        uid,
        password,
        "ir.model",
        "search_read",
        [[("model", "in", ["product.template", "crm.lead", "sale.order", "purchase.order", "project.project", "project.task"])]],
        {"fields": ["model"], "limit": 50},
    )
    return {row["model"] for row in rows}


def get_or_create(url, database, uid, password, model, field, value, values, dry_run):
    record_id = find_one(url, database, uid, password, model, field, value)
    if record_id:
        print(f"EXISTE  {model:18} {value}")
        return record_id
    print(f"CREAR   {model:18} {value}")
    if dry_run:
        return None
    return call(url, database, uid, password, model, "create", [values])


def main():
    parser = argparse.ArgumentParser(description="Carga datos funcionales ficticios para probar Odoo.")
    parser.add_argument("--env", default="script/creacion-usuarios/.env")
    parser.add_argument("--dry-run", action="store_true", help="Muestra cambios sin crear registros")
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
    models = available_models(url, database, uid, password)
    for optional_model, label in (("sale.order", "Ventas"), ("project.project", "Proyectos")):
        if optional_model not in models:
            print(f"AVISO   Modulo de {label} no instalado; se omite esa parte de la demo.")

    partner_ids = {}
    for name, email, city, country in PARTNERS:
        partner_ids[name] = get_or_create(
            url, database, uid, password, "res.partner", "name", name,
            {"name": name, "email": email, "city": city, "country_id": False, "comment": "Registro ficticio para pruebas funcionales."}, args.dry_run,
        )

    service_ids = {}
    for name, description in SERVICES:
        service_ids[name] = get_or_create(
            url, database, uid, password, "product.template", "name", name,
            {"name": name, "type": "service", "sale_ok": True, "purchase_ok": True, "list_price": 1000000, "description_sale": description}, args.dry_run,
        )

    for name, partner_name, revenue, description in OPPORTUNITIES:
        get_or_create(
            url, database, uid, password, "crm.lead", "name", name,
            {"name": name, "type": "opportunity", "partner_id": partner_ids.get(partner_name), "expected_revenue": revenue, "description": description}, args.dry_run,
        )

    if not args.dry_run and "purchase.order" in models:
        sale_partner = partner_ids["Cliente Demo Energia Norte"]
        purchase_partner = partner_ids["Proveedor Demo Equipos Electricos"]
        sale_product = service_ids["Demo - Pruebas electricas y puesta en servicio"]
        purchase_product = service_ids["Demo - Montaje de equipos AT/MT"]
        if "sale.order" in models and sale_partner and sale_product:
            variant = call(url, database, uid, password, "product.product", "search", [[("product_tmpl_id", "=", sale_product)]], {"limit": 1})
            if variant:
                get_or_create(url, database, uid, password, "sale.order", "name", "DEMO-COT-ENERGIA-NORTE", {"name": "DEMO-COT-ENERGIA-NORTE", "partner_id": sale_partner, "order_line": [(0, 0, {"product_id": variant[0], "product_uom_qty": 1, "price_unit": 18500000})]}, args.dry_run)
        if purchase_partner and purchase_product:
            variant = call(url, database, uid, password, "product.product", "search", [[("product_tmpl_id", "=", purchase_product)]], {"limit": 1})
            if variant:
                get_or_create(url, database, uid, password, "purchase.order", "name", "DEMO-OC-EQUIPOS", {"name": "DEMO-OC-EQUIPOS", "partner_id": purchase_partner, "order_line": [(0, 0, {"product_id": variant[0], "product_qty": 1, "price_unit": 9000000})]}, args.dry_run)

        project_id = None
        if "project.project" in models:
            project_id = get_or_create(url, database, uid, password, "project.project", "name", "Demo - Puesta en servicio Energia Norte", {"name": "Demo - Puesta en servicio Energia Norte", "partner_id": sale_partner}, args.dry_run)
        if project_id and "project.task" in models:
            for task_name in ("Levantamiento tecnico", "Pruebas de equipos", "Informe y cierre"):
                get_or_create(url, database, uid, password, "project.task", "name", task_name, {"name": task_name, "project_id": project_id}, args.dry_run)

    print("Simulacion completada." if args.dry_run else "Datos demo procesados correctamente.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, xmlrpc.client.Fault, xmlrpc.client.ProtocolError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)