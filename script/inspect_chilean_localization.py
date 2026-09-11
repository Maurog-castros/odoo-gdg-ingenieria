#!/usr/bin/env python3
"""Inspect available Chilean localization modules and company configuration."""

import argparse
import sys
import xmlrpc.client
from pathlib import Path

from demo_proyecto_gdg import database_from_url, load_env


def rpc(proxy, database, uid, password, model, method, args, kwargs=None):
    return proxy.execute_kw(database, uid, password, model, method, args, kwargs or {})


def available_fields(proxy, database, uid, password, model, requested):
    fields = rpc(proxy, database, uid, password, model, "fields_get", [], {
        "attributes": ["type", "readonly", "required", "selection"],
    })
    return {name: fields[name] for name in requested if name in fields}


def main():
    parser = argparse.ArgumentParser(description="Inspecciona la localización chilena disponible en Odoo.")
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
    proxy = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

    print(f"Odoo {common.version().get('server_version', 'desconocida')}")
    modules = rpc(proxy, database, uid, password, "ir.module.module", "search_read", [
        ["|", "|", ("name", "ilike", "l10n_cl"), ("name", "ilike", "account"), ("name", "ilike", "localization")]
    ], {"fields": ["name", "shortdesc", "state", "application"], "order": "name"})
    print("\nMódulos contables y chilenos disponibles")
    for module in modules:
        if module["name"].startswith("l10n_cl") or module.get("application"):
            print(f"{module['state']:14} {module['name']:35} {module['shortdesc']}")

    companies = rpc(proxy, database, uid, password, "res.company", "search_read", [[]], {
        "fields": ["name", "country_id", "currency_id", "vat", "chart_template"], "limit": 5,
    })
    print("\nCompañías")
    for company in companies:
        print(company)

    probes = {
        "res.company": (
            "country_id", "currency_id", "vat", "chart_template", "street", "city", "state_id",
            "l10n_cl_activity_description", "l10n_cl_company_activity_ids", "l10n_cl_sii_regional_office",
            "l10n_cl_dte_service_provider", "l10n_cl_dte_resolution_date", "l10n_cl_dte_resolution_number",
        ),
        "res.partner": ("l10n_latam_identification_type_id", "l10n_cl_sii_taxpayer_type", "vat"),
        "account.journal": ("l10n_latam_use_documents", "l10n_cl_point_of_sale_type", "l10n_cl_sequence_ids"),
        "account.move": (
            "l10n_latam_document_type_id", "l10n_latam_document_number", "l10n_cl_dte_status",
            "l10n_cl_sii_send_ident", "l10n_cl_claim", "l10n_cl_payment_policy",
        ),
        "l10n_cl.company.activities": ("name", "code", "tax_category"),
        "l10n_latam.document.type": ("name", "code", "country_id", "internal_type"),
        "l10n_latam.identification.type": ("name", "l10n_cl_code", "country_id"),
    }
    print("\nCampos de localización disponibles")
    known_models = {row["model"] for row in rpc(proxy, database, uid, password, "ir.model", "search_read", [
        [("model", "in", list(probes))]
    ], {"fields": ["model"]})}
    for model, requested in probes.items():
        if model not in known_models:
            print(f"NO  {model}")
            continue
        print(f"SI  {model}: {available_fields(proxy, database, uid, password, model, requested)}")

    move_counts = rpc(proxy, database, uid, password, "account.move", "read_group", [
        [], ["company_id", "state"], ["company_id", "state"]
    ], {"lazy": False})
    print("\nMovimientos contables por compañía y estado")
    for row in move_counts:
        print(row)

    installed_models = rpc(proxy, database, uid, password, "ir.model", "search_read", [
        [("model", "ilike", "l10n_cl")]
    ], {"fields": ["model", "name"], "order": "model"})
    print("\nModelos chilenos instalados")
    for model in installed_models:
        print(f"{model['model']:45} {model['name']}")

    for model, fields, domain in (
        ("l10n_cl.company.activities", ["name", "code", "tax_category"], []),
        ("l10n_latam.document.type", ["name", "code", "internal_type"], [("country_id.code", "=", "CL")]),
        ("l10n_latam.identification.type", ["name"], [("country_id.code", "=", "CL")]),
    ):
        print(f"\nMuestra {model}")
        rows = rpc(proxy, database, uid, password, model, "search_read", [domain], {
            "fields": fields, "limit": 30, "order": "code" if "code" in fields else "name",
        })
        for row in rows:
            print(row)

    apps = rpc(proxy, database, uid, password, "ir.module.module", "search_read", [
        [("state", "=", "installed"), ("application", "=", True)]
    ], {"fields": ["name", "shortdesc"], "order": "name"})
    print("\nAplicaciones instaladas")
    for app in apps:
        print(f"{app['name']:35} {app['shortdesc']}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, xmlrpc.client.Fault, xmlrpc.client.ProtocolError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
