#!/usr/bin/env python3
"""Create the GDG Engineering project demo in Odoo."""

import argparse
import json
import sys
import urllib.request
import xmlrpc.client
from pathlib import Path


PROJECT_NAME = "Demo - Puesta en servicio Subestacion Energia Norte"
PARTNER_NAME = "Cliente Demo Energia Norte"
TASKS = [
    ("01 - Levantamiento tecnico", "Revisar alcance, planos, permisos y condiciones de la subestacion."),
    ("02 - Planificacion de montaje", "Definir recursos, equipos, secuencia de montaje y controles de seguridad."),
    ("03 - Montaje de equipos AT/MT", "Registrar el montaje de transformador, interruptores y equipos asociados."),
    ("04 - Pruebas electricas PES", "Ejecutar pruebas de puesta en servicio, protecciones y control."),
    ("05 - Informe y cierre", "Consolidar protocolos, observaciones, evidencias y acta de cierre."),
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


def find_one(url, database, uid, password, model, domain):
    ids = call(url, database, uid, password, model, "search", [domain], {"limit": 1})
    return ids[0] if ids else None


def get_or_create(url, database, uid, password, model, domain, values, label, dry_run):
    record_id = find_one(url, database, uid, password, model, domain)
    if record_id:
        print(f"EXISTE  {model:16} {label}")
        return record_id
    print(f"CREAR   {model:16} {label}")
    if dry_run:
        return None
    return call(url, database, uid, password, model, "create", [values])


def main():
    parser = argparse.ArgumentParser(description="Carga el demo funcional de Proyectos para GDG Ingenieria.")
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

    project_model = find_one(url, database, uid, password, "ir.model", [("model", "=", "project.project")])
    task_model = find_one(url, database, uid, password, "ir.model", [("model", "=", "project.task")])
    if not project_model or not task_model:
        raise RuntimeError("Los modulos y modelos de Proyectos no estan disponibles")

    partner_id = find_one(url, database, uid, password, "res.partner", [("name", "=", PARTNER_NAME)])
    if not partner_id:
        raise RuntimeError(f"No existe el contacto demo: {PARTNER_NAME}. Ejecuta primero seed_demo_data.py")

    project_id = get_or_create(
        url, database, uid, password, "project.project", [("name", "=", PROJECT_NAME)],
        {"name": PROJECT_NAME, "partner_id": partner_id}, PROJECT_NAME, args.dry_run,
    )
    for task_name, description in TASKS:
        values = {"name": task_name, "description": description}
        if project_id:
            values["project_id"] = project_id
        get_or_create(
            url, database, uid, password, "project.task",
            [("name", "=", task_name)], values, task_name, args.dry_run,
        )

    print("Simulacion completada." if args.dry_run else "Demo de Proyectos procesada correctamente.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, xmlrpc.client.Fault, xmlrpc.client.ProtocolError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)