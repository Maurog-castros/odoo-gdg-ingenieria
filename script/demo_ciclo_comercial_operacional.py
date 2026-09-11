#!/usr/bin/env python3
"""Load connected CRM, Sales, Inventory and Accounting demo data."""

import argparse
import sys
import xmlrpc.client
from datetime import date, datetime, time, timedelta
from pathlib import Path

from demo_proyecto_gdg import Odoo, database_from_url, load_env


CLIENTS = (
    ("Cliente Demo Energia Norte", "contacto.energia@example.com", "Antofagasta"),
    ("Cliente Demo Mineria Central", "abastecimiento.mineria@example.com", "Calama"),
    ("Cliente Demo Transmision Sur", "proyectos.transmision@example.com", "Concepción"),
    ("Cliente Demo Industria Andina", "mantenimiento.andina@example.com", "Santiago"),
)

CRM_STAGES = (
    ("1 · Prospecto calificado", 10, False, False),
    ("2 · Diagnóstico comercial", 20, False, False),
    ("3 · Oferta en preparación", 30, False, False),
    ("4 · Negociación y adjudicación", 40, False, False),
    ("5 · Ganado", 50, True, True),
    ("6 · No adjudicado", 60, False, True),
)

CRM_LEADS = (
    ("DEMO CRM · Mantención preventiva planta industrial", "Cliente Demo Industria Andina", "1 · Prospecto calificado", 9800000, 15, "1", -1, "Necesidad detectada para mantenimiento preventivo anual de celdas MT."),
    ("DEMO CRM · Diagnóstico transformador principal", "Cliente Demo Mineria Central", "2 · Diagnóstico comercial", 14500000, 30, "2", 3, "Coordinar visita, antecedentes y ventana operacional para diagnóstico."),
    ("DEMO CRM · Montaje ampliación de patio 110 kV", "Cliente Demo Energia Norte", "3 · Oferta en preparación", 68500000, 55, "3", 7, "Preparar cubicación, APU y estrategia de ejecución para ampliación."),
    ("DEMO CRM · Pruebas y puesta en servicio alimentador", "Cliente Demo Transmision Sur", "4 · Negociación y adjudicación", 22500000, 75, "3", 5, "Oferta emitida; cliente solicita ajuste de plazo y forma de pago."),
    ("DEMO CRM · Puesta en servicio Subestación Norte", "Cliente Demo Energia Norte", "5 · Ganado", 18500000, 100, "3", -15, "Servicio adjudicado y convertido en proyecto y pedido de venta."),
    ("DEMO CRM · Inspección termográfica anual", "Cliente Demo Mineria Central", "6 · No adjudicado", 6200000, 0, "0", -10, "Proceso cerrado: el cliente postergó la intervención al próximo presupuesto."),
)

PRODUCTS = (
    ("DEMO-SRV-DIAG", "Diagnóstico eléctrico en terreno", "service", False, 3500000),
    ("DEMO-SRV-MONTAJE", "Montaje electromecánico AT/MT", "service", False, 12000000),
    ("DEMO-SRV-PES", "Pruebas y puesta en servicio", "service", False, 5000000),
    ("DEMO-REP-FUSIBLE", "Fusible de control industrial 10 A", "consu", True, 45000),
)

SALE_ORDERS = (
    ("DEMO-COT-DIAGNOSTICO-201", "Cliente Demo Mineria Central", "draft", -1, 14, "DEMO CRM · Diagnóstico transformador principal", (("DEMO-SRV-DIAG", 1, 3500000, 0),)),
    ("DEMO-COT-MANTENCION-202", "Cliente Demo Transmision Sur", "sent", -12, -2, "DEMO CRM · Pruebas y puesta en servicio alimentador", (("DEMO-SRV-MONTAJE", 1, 9000000, 5), ("DEMO-SRV-PES", 1, 3750000, 0))),
    ("DEMO-PED-OBRA-203", "Cliente Demo Energia Norte", "sale", -20, 10, "DEMO CRM · Puesta en servicio Subestación Norte", (("DEMO-SRV-MONTAJE", 1, 12500000, 0), ("DEMO-SRV-PES", 1, 6000000, 0))),
    ("DEMO-COT-CANCELADA-204", "Cliente Demo Mineria Central", "cancel", -25, -15, "DEMO CRM · Inspección termográfica anual", (("DEMO-SRV-DIAG", 1, 6200000, 0),)),
)

INVOICES = (
    ("DEMO-FAC-BORRADOR-301", "out_invoice", "Cliente Demo Mineria Central", "draft", -1, 14, (("DEMO-SRV-DIAG", 1, 3500000),)),
    ("DEMO-FAC-PENDIENTE-302", "out_invoice", "Cliente Demo Energia Norte", "posted", -10, 10, (("DEMO-SRV-MONTAJE", 0.5, 12000000),)),
    ("DEMO-FAC-VENCIDA-303", "out_invoice", "Cliente Demo Transmision Sur", "posted", -35, -5, (("DEMO-SRV-PES", 0.8, 5000000),)),
    ("DEMO-FAC-PAGADA-304", "out_invoice", "Cliente Demo Industria Andina", "paid", -25, -5, (("DEMO-SRV-DIAG", 1, 2500000),)),
    ("DEMO-FCP-BORRADOR-305", "in_invoice", "Proveedor Demo Maquinaria y Transporte", "draft", -3, 12, (("DEMO-SRV-MONTAJE", 0.1, 12000000),)),
)


def dt(offset, hour=10):
    return datetime.combine(date.today() + timedelta(days=offset), time(hour, 0)).strftime("%Y-%m-%d %H:%M:%S")


def ensure_partner(odoo, name, email=None, city=None, supplier=False):
    values = {"name": name, "company_type": "company", "email": email, "city": city}
    if supplier:
        values["supplier_rank"] = 1
    else:
        values["customer_rank"] = 1
    return odoo.upsert("res.partner", [("name", "=", name)], values, name)


def ensure_product(odoo, code, name, product_type, storable, price):
    template_id = odoo.upsert("product.template", [("default_code", "=", code)], {
        "name": name, "default_code": code, "type": product_type, "is_storable": storable,
        "sale_ok": True, "purchase_ok": True, "list_price": price, "standard_price": price * 0.6,
        "description_sale": f"Servicio o producto ficticio {code} para demostración.",
    }, f"{code} · {name}")
    variant_id = odoo.find("product.product", [("product_tmpl_id", "=", template_id)]) if template_id else None
    return template_id, variant_id


def create_crm(odoo, partners, salesperson_id):
    stages = {}
    for name, sequence, won, fold in CRM_STAGES:
        stages[name] = odoo.upsert("crm.stage", [("name", "=", name)], {"name": name, "sequence": sequence, "is_won": won, "fold": fold}, name)
    tag_ids = []
    for name, color in (("DEMO · Energía", 4), ("DEMO · Minería", 2), ("DEMO · Alta prioridad", 1)):
        tag_id = odoo.upsert("crm.tag", [("name", "=", name)], {"name": name, "color": color}, name)
        if tag_id:
            tag_ids.append(tag_id)
    leads = {}
    for name, partner_name, stage_name, revenue, probability, priority, deadline, description in CRM_LEADS:
        leads[name] = odoo.upsert("crm.lead", [("name", "=", name)], {
            "name": name, "type": "opportunity", "partner_id": partners.get(partner_name),
            "user_id": salesperson_id, "stage_id": stages.get(stage_name), "priority": priority,
            "expected_revenue": revenue, "probability": probability,
            "date_deadline": (date.today() + timedelta(days=deadline)).isoformat(),
            "tag_ids": [(6, 0, tag_ids[:2] if "Mineria" not in partner_name else tag_ids[1:])],
            "description": f"<h3>Contexto comercial</h3><p>{description}</p><p><b>Próxima decisión:</b> avanzar según la etapa y actividad programada.</p>",
        }, name)
    return leads


def ensure_sale_order(odoo, name, partner_id, target, order_date, validity, lead_id, lines, products, salesperson_id):
    order_id = odoo.find("sale.order", [("name", "=", name)])
    if not order_id:
        print(f"{'CREARÍA' if odoo.dry_run else 'CREAR':10} sale.order             {name}")
        if odoo.dry_run:
            return None
        commands = []
        for code, quantity, price, discount in lines:
            product_id = products[code][1]
            commands.append((0, 0, {"product_id": product_id, "product_uom_qty": quantity, "price_unit": price, "discount": discount, "name": products[code][2]}))
        values = {"name": name, "partner_id": partner_id, "user_id": salesperson_id, "date_order": dt(order_date), "validity_date": (date.today() + timedelta(days=validity)).isoformat(), "client_order_ref": f"REF-{name[-3:]}", "origin": "DEMO CRM", "opportunity_id": lead_id or False, "note": "<p>Documento ficticio para demostración del ciclo comercial.</p>", "order_line": commands}
        order_id = odoo.call("sale.order", "create", [odoo.clean("sale.order", values)])
        odoo.created += 1
    else:
        print(f"{'REVISAR' if odoo.dry_run else 'EXISTE':10} sale.order             {name}")
    if not order_id:
        return None
    state = odoo.call("sale.order", "read", [[order_id]], {"fields": ["state"]})[0]["state"]
    if odoo.dry_run:
        print(f"REVISAR    sale.workflow          {name} · {state}")
    elif target == "sent" and state == "draft":
        odoo.call("sale.order", "write", [[order_id], {"state": "sent"}])
    elif target == "sale" and state in ("draft", "sent"):
        odoo.call("sale.order", "action_confirm", [[order_id]])
    elif target == "cancel" and state != "cancel":
        odoo.call("sale.order", "write", [[order_id], {"state": "cancel"}])
    return order_id


def ensure_picking(odoo, origin, picking_type_id, source_id, destination_id, product_id, quantity, target):
    picking_id = odoo.find("stock.picking", [("origin", "=", origin)])
    if not picking_id:
        print(f"{'CREARÍA' if odoo.dry_run else 'CREAR':10} stock.picking          {origin}")
        if odoo.dry_run:
            return None
        product = odoo.call("product.product", "read", [[product_id]], {"fields": ["display_name", "uom_id"]})[0]
        move_values = {
            "product_id": product_id,
            "product_uom": product["uom_id"][0],
            "product_uom_qty": quantity,
            "location_id": source_id,
            "location_dest_id": destination_id,
        }
        # Odoo 19 calcula la descripción desde el producto y ya no expone el
        # campo heredado `name` en stock.move.
        values = {"picking_type_id": picking_type_id, "location_id": source_id, "location_dest_id": destination_id, "scheduled_date": dt(0), "origin": origin, "move_ids": [(0, 0, move_values)]}
        picking_id = odoo.call("stock.picking", "create", [odoo.clean("stock.picking", values)])
        odoo.created += 1
    else:
        print(f"{'REVISAR' if odoo.dry_run else 'EXISTE':10} stock.picking          {origin}")
    if not picking_id:
        return picking_id
    picking = odoo.call("stock.picking", "read", [[picking_id]], {"fields": ["state", "move_ids"]})[0]
    if odoo.dry_run:
        print(f"REVISAR    stock.workflow         {origin} · {picking['state']}")
        return picking_id
    if picking["state"] == "draft":
        odoo.call("stock.picking", "action_confirm", [[picking_id]])
    if target == "done" and picking["state"] != "done":
        odoo.call("stock.picking", "action_assign", [[picking_id]])
        for move_id in picking["move_ids"]:
            move = odoo.call("stock.move", "read", [[move_id]], {"fields": ["product_uom_qty"]})[0]
            odoo.call("stock.move", "write", [[move_id], {"quantity": move["product_uom_qty"], "picked": True}])
        odoo.call("stock.picking", "button_validate", [[picking_id]])
    elif target == "ready":
        odoo.call("stock.picking", "action_assign", [[picking_id]])
    return picking_id


def create_inventory(odoo, products):
    warehouses = odoo.call("stock.warehouse", "search_read", [[]], {"fields": ["lot_stock_id", "in_type_id", "int_type_id"], "limit": 1})
    if not warehouses:
        odoo.omit("Inventario", "no existe una bodega configurada")
        return
    warehouse = warehouses[0]
    stock_id = warehouse["lot_stock_id"][0]
    supplier_id = odoo.find("stock.location", [("usage", "=", "supplier")])
    obra_id = odoo.upsert("stock.location", [("name", "=", "DEMO · Obra Proyecto 3")], {"name": "DEMO · Obra Proyecto 3", "location_id": stock_id, "usage": "internal", "barcode": "DEMO-OBRA-003"}, "DEMO · Obra Proyecto 3")
    calibration_id = odoo.upsert("stock.location", [("name", "=", "DEMO · Equipos en calibración")], {"name": "DEMO · Equipos en calibración", "location_id": stock_id, "usage": "internal", "barcode": "DEMO-CALIBRACION"}, "DEMO · Equipos en calibración")
    product_id = products["DEMO-REP-FUSIBLE"][1]
    if product_id and obra_id:
        ensure_picking(odoo, "DEMO-STOCK-INICIAL-401", warehouse["in_type_id"][0], supplier_id, stock_id, product_id, 30, "done")
        ensure_picking(odoo, "DEMO-TRANSFERENCIA-OBRA-402", warehouse["int_type_id"][0], stock_id, obra_id, product_id, 12, "done")
        ensure_picking(odoo, "DEMO-REPOSICION-OBRA-403", warehouse["int_type_id"][0], stock_id, obra_id, product_id, 8, "ready")
        ensure_picking(odoo, "DEMO-RETORNO-CALIBRACION-404", warehouse["int_type_id"][0], obra_id, calibration_id, product_id, 2, "ready")


def ensure_invoice(odoo, ref, move_type, partner_id, target, invoice_date, due_date, lines, products):
    move_id = odoo.find("account.move", [("ref", "=", ref), ("move_type", "=", move_type)])
    if not move_id:
        print(f"{'CREARÍA' if odoo.dry_run else 'CREAR':10} account.move           {ref}")
        if odoo.dry_run:
            return None
        commands = []
        for code, quantity, price in lines:
            commands.append((0, 0, {"product_id": products[code][1], "name": products[code][2], "quantity": quantity, "price_unit": price}))
        move_id = odoo.call("account.move", "create", [{"move_type": move_type, "partner_id": partner_id, "invoice_date": (date.today() + timedelta(days=invoice_date)).isoformat(), "invoice_date_due": (date.today() + timedelta(days=due_date)).isoformat(), "ref": ref, "invoice_line_ids": commands}])
        odoo.created += 1
    else:
        print(f"{'REVISAR' if odoo.dry_run else 'EXISTE':10} account.move           {ref}")
    if not move_id:
        return None
    move = odoo.call("account.move", "read", [[move_id]], {"fields": ["state", "payment_state", "amount_residual", "amount_total"]})[0]
    if odoo.dry_run:
        print(f"REVISAR    account.workflow       {ref} · {move['state']} · {move['payment_state']}")
        return move_id
    if target in ("posted", "paid") and move["state"] == "draft":
        odoo.call("account.move", "action_post", [[move_id]])
    if target == "paid":
        move = odoo.call("account.move", "read", [[move_id]], {"fields": ["payment_state", "amount_residual"]})[0]
        if move["payment_state"] != "paid" and move["amount_residual"]:
            journals = odoo.call("account.journal", "search_read", [[("type", "in", ["bank", "cash"])]], {"fields": ["id"], "limit": 1})
            if journals:
                context = {"active_model": "account.move", "active_ids": [move_id], "active_id": move_id}
                wizard_id = odoo.call("account.payment.register", "create", [{"payment_date": date.today().isoformat(), "amount": move["amount_residual"], "journal_id": journals[0]["id"]}], {"context": context})
                odoo.call("account.payment.register", "action_create_payments", [[wizard_id]], {"context": context})
            else:
                odoo.omit(f"Pago {ref}", "no existe diario de banco o caja")
    return move_id


def main():
    parser = argparse.ArgumentParser(description="Carga demos conectadas de CRM, Ventas, Inventario y Contabilidad.")
    parser.add_argument("--env", default="script/creacion-usuarios/.env")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    config = load_env(Path(args.env))
    url = config.get("URLODOO", "").rstrip("/")
    admin, password = config.get("ADMIN-USER", ""), config.get("PASS", "")
    if not url or not admin or not password:
        raise RuntimeError(".env debe contener URLODOO, ADMIN-USER y PASS")
    database = config.get("ODOO_DB") or database_from_url(url)
    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(database, admin, password, {})
    if not uid:
        raise RuntimeError("No se pudo autenticar")
    odoo = Odoo(url, database, uid, password, args.dry_run)
    required = ("crm.lead", "sale.order", "stock.picking", "account.move")
    missing = [model for model in required if not odoo.supports(model)]
    if missing:
        raise RuntimeError(f"Faltan módulos requeridos: {', '.join(missing)}")

    partners = {name: ensure_partner(odoo, name, email, city) for name, email, city in CLIENTS}
    supplier_name = "Proveedor Demo Maquinaria y Transporte"
    partners[supplier_name] = ensure_partner(odoo, supplier_name, "operaciones.maquinaria@example.com", "Calama", supplier=True)
    salesperson_id = odoo.find("res.users", [("login", "=", "sales.user")]) or uid
    leads = create_crm(odoo, partners, salesperson_id)

    products = {}
    for code, name, product_type, storable, price in PRODUCTS:
        template_id, variant_id = ensure_product(odoo, code, name, product_type, storable, price)
        products[code] = (template_id, variant_id, name)

    for name, partner_name, target, order_date, validity, lead_name, lines in SALE_ORDERS:
        ensure_sale_order(odoo, name, partners.get(partner_name), target, order_date, validity, leads.get(lead_name), lines, products, salesperson_id)

    create_inventory(odoo, products)

    for ref, move_type, partner_name, target, invoice_date, due_date, lines in INVOICES:
        ensure_invoice(odoo, ref, move_type, partners.get(partner_name), target, invoice_date, due_date, lines, products)

    print("\nResumen")
    if args.dry_run:
        print("Simulación completa: no se modificó Odoo.")
    else:
        lead_count = odoo.call("crm.lead", "search_count", [[("name", "in", [item[0] for item in CRM_LEADS])]])
        sale_count = odoo.call("sale.order", "search_count", [[("name", "in", [item[0] for item in SALE_ORDERS])]])
        picking_count = odoo.call("stock.picking", "search_count", [[("origin", "in", [
            "DEMO-STOCK-INICIAL-401", "DEMO-TRANSFERENCIA-OBRA-402",
            "DEMO-REPOSICION-OBRA-403", "DEMO-RETORNO-CALIBRACION-404",
        ])]])
        invoice_count = odoo.call("account.move", "search_count", [[("ref", "in", [item[0] for item in INVOICES])]])
        print(f"Control: {lead_count} oportunidades · {sale_count} documentos de venta · {picking_count} movimientos · {invoice_count} facturas demo.")
    for feature, reason in odoo.skipped:
        print(f"Pendiente por configuración: {feature} — {reason}.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, xmlrpc.client.Fault, xmlrpc.client.ProtocolError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
