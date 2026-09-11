#!/usr/bin/env python3
"""Install optional Chilean modules and load a safe localization demo company."""

import argparse
import sys
import xmlrpc.client
from datetime import date, datetime, time, timedelta
from pathlib import Path

from demo_proyecto_gdg import Odoo, database_from_url, load_env


COMPANY_NAME = "GDG Ingeniería Chile · DEMO"
OPTIONAL_MODULES = ("l10n_cl_edi_exports", "l10n_cl_edi_factoring")
PARTNERS = (
    ("Cliente Demo Chile Minería SpA", "76123456-0", "1", "CL", "Calama"),
    ("Cliente Demo Chile Energía Ltda.", "76234567-6", "1", "CL", "Antofagasta"),
    ("Proveedor Demo Chile Obras Civiles Ltda.", "76345678-1", "1", "CL", "Santiago"),
    ("Cliente Demo Exportación Perú SAC", False, "4", "PE", "Lima"),
)
DOCUMENTS = (
    ("DEMO-CL-FAC-33-001", "out_invoice", "Cliente Demo Chile Minería SpA", "33", 1850000, "sale"),
    ("DEMO-CL-FAC-34-002", "out_invoice", "Cliente Demo Chile Energía Ltda.", "34", 760000, "exempt"),
    ("DEMO-CL-FCP-46-003", "in_invoice", "Proveedor Demo Chile Obras Civiles Ltda.", "46", 980000, "purchase"),
    ("DEMO-CL-FAC-EXPORT-004", "out_invoice", "Cliente Demo Exportación Perú SAC", "110", 4200, "export"),
    ("DEMO-CL-NC-61-005", "out_refund", "Cliente Demo Chile Minería SpA", "61", 185000, "sale"),
)
EVENTS = (
    ("DEMO CL · Revisión tributaria mensual y F29", 2, 9, "Revisar IVA débito, IVA crédito, compras, ventas y borrador de F29."),
    ("DEMO CL · Visita técnica Cliente Minería", 4, 11, "Coordinar alcance técnico que continuará en cotización y proyecto."),
    ("DEMO CL · Comité de cierre, facturación y cobranza", 9, 16, "Revisar entregables, DTE pendiente, vencimientos y responsable de cobranza."),
)


def context(company_id):
    return {"allowed_company_ids": [company_id], "company_id": company_id, "force_company": company_id}


def ensure_modules(odoo):
    for name in OPTIONAL_MODULES:
        module_id = odoo.find("ir.module.module", [("name", "=", name)])
        if not module_id:
            raise RuntimeError(f"El módulo {name} no está disponible en esta edición")
        state = odoo.call("ir.module.module", "read", [[module_id]], {"fields": ["state"]})[0]["state"]
        if state == "installed":
            print(f"INSTALADO  ir.module.module       {name}")
        elif odoo.dry_run:
            print(f"INSTALARÍA ir.module.module       {name} · estado actual {state}")
        else:
            print(f"INSTALAR   ir.module.module       {name}")
            odoo.call("ir.module.module", "button_immediate_install", [[module_id]])


def ensure_company(odoo, uid):
    company_id = odoo.find("res.company", [("name", "=", COMPANY_NAME)])
    country_id = odoo.find("res.country", [("code", "=", "CL")])
    currency_ids = odoo.call("res.currency", "search", [[("name", "=", "CLP")]], {
        "limit": 1, "context": {"active_test": False},
    })
    currency_id = currency_ids[0] if currency_ids else False
    if not country_id or not currency_id:
        raise RuntimeError("No se encontraron Chile y CLP en los datos maestros de Odoo")
    if not odoo.dry_run:
        odoo.call("res.currency", "write", [[currency_id], {"active": True}])
    state_id = odoo.find("res.country.state", [("country_id", "=", country_id), ("name", "ilike", "Metropolitana")])
    activity_ids = odoo.call("l10n_cl.company.activities", "search", [[("code", "in", ["432100", "711002"])]])
    values = {
        "name": COMPANY_NAME,
        "country_id": country_id,
        "currency_id": currency_id,
        "chart_template": "cl",
        "vat": "76123456-0",
        "street": "Av. Proyecto Demo 1234",
        "city": "Santiago",
        "state_id": state_id or False,
        "zip": "7500000",
        "phone": "+56 2 2000 0000",
        "email": "contabilidad.demo@example.com",
        "l10n_cl_activity_description": "Servicios de ingeniería eléctrica y montaje industrial · DEMO",
        "l10n_cl_company_activity_ids": [(6, 0, activity_ids)],
        "l10n_cl_sii_regional_office": "ur_SaC",
        "l10n_cl_dte_service_provider": "SIIDEMO",
        "l10n_cl_dte_resolution_date": date.today().isoformat(),
        "l10n_cl_dte_resolution_number": "0-DEMO",
    }
    values = {name: (False if value is None else value) for name, value in values.items()}
    if not company_id:
        print(f"{'CREARÍA' if odoo.dry_run else 'CREAR':10} res.company            {COMPANY_NAME}")
        if odoo.dry_run:
            return None
        company_id = odoo.call("res.company", "create", [odoo.clean("res.company", values)])
        odoo.created += 1
    else:
        print(f"{'REVISAR' if odoo.dry_run else 'ACTUALIZAR':10} res.company            {COMPANY_NAME}")
        if not odoo.dry_run:
            odoo.call("res.company", "write", [[company_id], odoo.clean("res.company", values)])
    if company_id and not odoo.dry_run:
        user = odoo.call("res.users", "read", [[uid]], {"fields": ["company_ids"]})[0]
        if company_id not in user["company_ids"]:
            odoo.call("res.users", "write", [[uid], {"company_ids": [(4, company_id)]}])
    return company_id


def ensure_partner(odoo, company_id, name, vat, taxpayer_type, country_code, city):
    partner_id = odoo.find("res.partner", [("name", "=", name), ("company_id", "=", company_id)])
    country_id = odoo.find("res.country", [("code", "=", country_code)])
    identification_id = odoo.find("l10n_latam.identification.type", [
        ("name", "=", "RUT"), ("country_id.code", "=", "CL")
    ]) if country_code == "CL" else False
    values = {
        "name": name,
        "company_type": "company",
        "company_id": company_id,
        "country_id": country_id,
        "city": city,
        "vat": vat,
        "email": f"{name.lower().replace(' ', '.')}@example.com",
        "customer_rank": 1 if not name.startswith("Proveedor") else 0,
        "supplier_rank": 1 if name.startswith("Proveedor") else 0,
        "l10n_cl_sii_taxpayer_type": taxpayer_type,
        "l10n_latam_identification_type_id": identification_id,
    }
    label = name
    if not partner_id:
        print(f"{'CREARÍA' if odoo.dry_run else 'CREAR':10} res.partner           {label}")
        if odoo.dry_run:
            return None
        partner_id = odoo.call("res.partner", "create", [odoo.clean("res.partner", values)], {"context": context(company_id)})
        odoo.created += 1
    else:
        print(f"{'REVISAR' if odoo.dry_run else 'ACTUALIZAR':10} res.partner           {label}")
        if not odoo.dry_run:
            odoo.call("res.partner", "write", [[partner_id], odoo.clean("res.partner", values)], {"context": context(company_id)})
    return partner_id


def ensure_product(odoo, company_id, sale_tax_id, purchase_tax_id):
    code = "DEMO-CL-SRV-ING"
    template_id = odoo.find("product.template", [("default_code", "=", code), ("company_id", "=", company_id)])
    values = {
        "name": "Servicio de ingeniería eléctrica nacional · DEMO Chile",
        "default_code": code,
        "type": "service",
        "sale_ok": True,
        "purchase_ok": True,
        "company_id": company_id,
        "list_price": 1850000,
        "standard_price": 980000,
        "taxes_id": [(6, 0, [sale_tax_id] if sale_tax_id else [])],
        "supplier_taxes_id": [(6, 0, [purchase_tax_id] if purchase_tax_id else [])],
        "description_sale": "Servicio ficticio afecto a IVA para la demostración de localización chilena.",
    }
    if not template_id:
        print(f"{'CREARÍA' if odoo.dry_run else 'CREAR':10} product.template      {code}")
        if odoo.dry_run:
            return None
        template_id = odoo.call("product.template", "create", [odoo.clean("product.template", values)], {"context": context(company_id)})
        odoo.created += 1
    else:
        print(f"{'REVISAR' if odoo.dry_run else 'ACTUALIZAR':10} product.template      {code}")
        if not odoo.dry_run:
            odoo.call("product.template", "write", [[template_id], odoo.clean("product.template", values)], {"context": context(company_id)})
    return odoo.find("product.product", [("product_tmpl_id", "=", template_id)]) if template_id else None


def ensure_document(odoo, company_id, product_id, partners, ref, move_type, partner_name, code, amount, tax_mode):
    move_id = odoo.find("account.move", [("company_id", "=", company_id), ("ref", "=", ref)])
    if move_id:
        move = odoo.call("account.move", "read", [[move_id]], {"fields": ["state", "payment_state"]})[0]
        print(f"{'REVISAR' if odoo.dry_run else 'EXISTE':10} account.move           {ref} · {move['state']} · {move['payment_state']}")
        return move_id
    print(f"{'CREARÍA' if odoo.dry_run else 'CREAR':10} account.move           {ref} · DTE {code}")
    if odoo.dry_run:
        return None
    journal_type = "purchase" if move_type == "in_invoice" else "sale"
    journal_id = odoo.find("account.journal", [("company_id", "=", company_id), ("type", "=", journal_type)])
    document_type_id = odoo.find("l10n_latam.document.type", [("country_id.code", "=", "CL"), ("code", "=", code)])
    tax_domain = [("company_id", "=", company_id), ("active", "=", True)]
    if tax_mode == "sale":
        tax_domain += [("type_tax_use", "=", "sale"), ("amount", "=", 19.0)]
    elif tax_mode == "purchase":
        tax_domain += [("type_tax_use", "=", "purchase"), ("amount", "=", 19.0)]
    else:
        tax_domain += [("type_tax_use", "=", "sale"), ("amount", "=", 0.0)]
    tax_id = odoo.find("account.tax", tax_domain)
    account_types = ["expense", "expense_direct_cost"] if move_type == "in_invoice" else ["income", "income_other"]
    account_ids = odoo.call("account.account", "search", [[
        ("company_ids", "in", [company_id]), ("account_type", "in", account_types)
    ]], {"limit": 1, "context": context(company_id)})
    if not account_ids:
        raise RuntimeError(f"No existe una cuenta contable compatible para {ref}")
    values = {
        "company_id": company_id,
        "journal_id": journal_id,
        "move_type": move_type,
        "partner_id": partners[partner_name],
        "invoice_date": date.today().isoformat(),
        "invoice_date_due": (date.today() + timedelta(days=30)).isoformat(),
        "ref": ref,
        "l10n_latam_document_type_id": document_type_id,
        "invoice_line_ids": [(0, 0, {
            "product_id": product_id,
            "account_id": account_ids[0],
            "name": f"{ref} · Documento tributario ficticio para demostración",
            "quantity": 1,
            "price_unit": amount,
            "tax_ids": [(6, 0, [tax_id] if tax_id and tax_mode not in ("exempt", "export") else [])],
        })],
    }
    if tax_mode == "export":
        usd_id = odoo.find("res.currency", [("name", "=", "USD")])
        values["currency_id"] = usd_id
    move_id = odoo.call("account.move", "create", [odoo.clean("account.move", values)], {"context": context(company_id)})
    odoo.created += 1
    return move_id


def ensure_events(odoo, uid, partners):
    attendee_ids = [partner_id for partner_id in partners.values() if partner_id]
    for name, day_offset, hour, description in EVENTS:
        event_id = odoo.find("calendar.event", [("name", "=", name)])
        start = datetime.combine(date.today() + timedelta(days=day_offset), time(hour, 0))
        values = {
            "name": name,
            "start": start.strftime("%Y-%m-%d %H:%M:%S"),
            "stop": (start + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": uid,
            "partner_ids": [(6, 0, attendee_ids)],
            "description": f"<p>{description}</p><p><b>Datos ficticios para demostración.</b></p>",
        }
        if event_id:
            print(f"{'REVISAR' if odoo.dry_run else 'ACTUALIZAR':10} calendar.event        {name}")
            if not odoo.dry_run:
                odoo.call("calendar.event", "write", [[event_id], odoo.clean("calendar.event", values)])
        else:
            print(f"{'CREARÍA' if odoo.dry_run else 'CREAR':10} calendar.event        {name}")
            if not odoo.dry_run:
                odoo.call("calendar.event", "create", [odoo.clean("calendar.event", values)])
                odoo.created += 1


def load_demo(odoo, uid):
    company_id = ensure_company(odoo, uid)
    if not company_id:
        print("La simulación se detiene antes de los datos dependientes de la compañía nueva.")
        return
    accounts = odoo.call("account.account", "search_count", [[("company_ids", "in", [company_id])]], {"context": context(company_id)})
    taxes = odoo.call("account.tax", "search_count", [[("company_id", "=", company_id)]], {"context": context(company_id)})
    journals = odoo.call("account.journal", "search_count", [[("company_id", "=", company_id)]], {"context": context(company_id)})
    if not accounts or not taxes or not journals:
        raise RuntimeError(f"La compañía no recibió el plan chileno completo: {accounts} cuentas, {taxes} impuestos, {journals} diarios")
    sale_tax_id = odoo.find("account.tax", [("company_id", "=", company_id), ("type_tax_use", "=", "sale"), ("amount", "=", 19.0)])
    purchase_tax_id = odoo.find("account.tax", [("company_id", "=", company_id), ("type_tax_use", "=", "purchase"), ("amount", "=", 19.0)])
    partners = {}
    for row in PARTNERS:
        partners[row[0]] = ensure_partner(odoo, company_id, *row)
    product_id = ensure_product(odoo, company_id, sale_tax_id, purchase_tax_id)
    for row in DOCUMENTS:
        ensure_document(odoo, company_id, product_id, partners, *row)
    ensure_events(odoo, uid, partners)
    print(f"Plan chileno: {accounts} cuentas · {taxes} impuestos · {journals} diarios.")


def main():
    parser = argparse.ArgumentParser(description="Activa extensiones y carga la demo de localización chilena.")
    parser.add_argument("--env", default="script/creacion-usuarios/.env")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    config = load_env(Path(args.env))
    url = config.get("URLODOO", "").rstrip("/")
    admin, password = config.get("ADMIN-USER", ""), config.get("PASS", "")
    database = config.get("ODOO_DB") or database_from_url(url)
    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(database, admin, password, {})
    if not uid:
        raise RuntimeError("No se pudo autenticar")
    odoo = Odoo(url, database, uid, password, args.dry_run)
    ensure_modules(odoo)
    load_demo(odoo, uid)
    print("\nResumen")
    if args.dry_run:
        print("Simulación completa: no se modificó Odoo.")
    else:
        company_id = odoo.find("res.company", [("name", "=", COMPANY_NAME)])
        document_count = odoo.call("account.move", "search_count", [[
            ("company_id", "=", company_id), ("ref", "in", [row[0] for row in DOCUMENTS])
        ]])
        print(f"Localización chilena lista · {document_count} documentos tributarios de demostración en borrador.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, xmlrpc.client.Fault, xmlrpc.client.ProtocolError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
