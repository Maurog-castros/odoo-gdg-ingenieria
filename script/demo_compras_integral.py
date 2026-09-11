#!/usr/bin/env python3
"""Create an idempotent, end-to-end Purchase demo for GDG Ingeniería."""

import argparse
import sys
import xmlrpc.client
from datetime import date, datetime, time, timedelta
from pathlib import Path

from demo_proyecto_gdg import Odoo, PROJECT_NAME, database_from_url, load_env


CATEGORIES = (
    ("DEMO · Materiales de obra", None),
    ("DEMO · Material eléctrico AT/MT", "DEMO · Materiales de obra"),
    ("DEMO · Ferretería y montaje", "DEMO · Materiales de obra"),
    ("DEMO · Obras civiles", "DEMO · Materiales de obra"),
    ("DEMO · Equipos de prueba", None),
    ("DEMO · EPP y seguridad", None),
    ("DEMO · Servicios y arriendos", None),
)

VENDORS = (
    ("Proveedor Demo Equipos Eléctricos", "ventas.equipos@example.com", "Santiago", 7),
    ("Proveedor Demo Ferretería Industrial", "cotizaciones.ferreteria@example.com", "Antofagasta", 3),
    ("Proveedor Demo Hormigones Norte", "despacho.hormigon@example.com", "Antofagasta", 2),
    ("Proveedor Demo Maquinaria y Transporte", "operaciones.maquinaria@example.com", "Calama", 5),
    ("Proveedor Demo Seguridad Industrial", "ventas.seguridad@example.com", "Santiago", 4),
)

PRODUCTS = (
    ("DEMO-CAB-CTRL", "Cable de control 12 x 2,5 mm²", "DEMO · Material eléctrico AT/MT", "consu", True, 5850, "m", 7),
    ("DEMO-TERM-MT", "Kit de terminales MT 23 kV", "DEMO · Material eléctrico AT/MT", "consu", True, 395000, "kit", 10),
    ("DEMO-PERNO-M20", "Perno galvanizado M20 x 80", "DEMO · Ferretería y montaje", "consu", True, 4850, "un", 3),
    ("DEMO-HORM-H30", "Hormigón premezclado H30", "DEMO · Obras civiles", "consu", True, 118000, "m³", 2),
    ("DEMO-EPP-ARCO", "Kit EPP categoría arco eléctrico", "DEMO · EPP y seguridad", "consu", True, 285000, "kit", 4),
    ("DEMO-REL-TEST", "Equipo secundario de prueba de relés", "DEMO · Equipos de prueba", "consu", True, 8900000, "un", 14),
    ("DEMO-ARR-GRUA", "Arriendo grúa 80 toneladas", "DEMO · Servicios y arriendos", "service", False, 1250000, "día", 5),
    ("DEMO-TRANS-CARGA", "Transporte especial de equipos", "DEMO · Servicios y arriendos", "service", False, 780000, "servicio", 4),
)

ORDER_SCENARIOS = (
    {
        "name": "DEMO-RFQ-CABLES-101", "vendor": "Proveedor Demo Equipos Eléctricos",
        "target": "draft", "date": -1, "planned": 8,
        "lines": (("DEMO-CAB-CTRL", 500, 5850, 3), ("DEMO-TERM-MT", 4, 395000, 0)),
        "note": "Solicitud nueva para comparar precio, plazo y disponibilidad de materiales eléctricos.",
    },
    {
        "name": "DEMO-RFQ-EPP-102", "vendor": "Proveedor Demo Seguridad Industrial",
        "target": "sent", "date": -8, "planned": -2,
        "lines": (("DEMO-EPP-ARCO", 8, 285000, 5),),
        "note": "Cotización enviada y vencida: permite demostrar seguimiento de proveedores y actividades atrasadas.",
    },
    {
        "name": "DEMO-APR-HORMIGON-103", "vendor": "Proveedor Demo Hormigones Norte",
        "target": "to approve", "date": -2, "planned": 3,
        "lines": (("DEMO-HORM-H30", 80, 118000, 2),),
        "note": "Compra de alto monto a la espera de aprobación del responsable de Compras.",
    },
    {
        "name": "DEMO-PO-MONTAJE-104", "vendor": "Proveedor Demo Ferretería Industrial",
        "target": "purchase", "date": -5, "planned": 4,
        "lines": (("DEMO-PERNO-M20", 240, 4850, 0), ("DEMO-CAB-CTRL", 300, 5700, 2)),
        "note": "Orden confirmada con recepción futura para mostrar cantidades pendientes y trazabilidad logística.",
    },
    {
        "name": "DEMO-PO-ATRASADA-105", "vendor": "Proveedor Demo Equipos Eléctricos",
        "target": "purchase", "date": -12, "planned": -3,
        "lines": (("DEMO-TERM-MT", 6, 382000, 4),),
        "note": "Recepción atrasada ficticia que exige seguimiento inmediato al proveedor.",
    },
    {
        "name": "DEMO-PO-RECIBIDA-106", "vendor": "Proveedor Demo Maquinaria y Transporte",
        "target": "received", "date": -14, "planned": -7,
        "lines": (("DEMO-ARR-GRUA", 2, 1250000, 0), ("DEMO-TRANS-CARGA", 1, 780000, 0)),
        "note": "Servicio recibido completamente y dentro del plazo para comparar desempeño del proveedor.",
    },
    {
        "name": "DEMO-RFQ-PRUEBAS-107", "vendor": "Proveedor Demo Equipos Eléctricos",
        "target": "cancel", "date": -18, "planned": -10,
        "lines": (("DEMO-REL-TEST", 1, 8900000, 0),),
        "note": "Solicitud cancelada por decisión de arrendar el equipo; conserva la trazabilidad de la decisión.",
    },
)

ACTIVITIES = (
    ("DEMO-RFQ-EPP-102", "Comparar oferta y solicitar vigencia", -1, "La cotización venció; confirmar precio y fecha de entrega."),
    ("DEMO-APR-HORMIGON-103", "Aprobar compra de hormigón H30", 0, "Revisar monto, plazo y partida del proyecto antes de aprobar."),
    ("DEMO-PO-ATRASADA-105", "Gestionar recepción atrasada", 0, "Contactar al proveedor y registrar nueva fecha comprometida."),
)


def dt(offset):
    return datetime.combine(date.today() + timedelta(days=offset), time(10, 0)).strftime("%Y-%m-%d %H:%M:%S")


def ensure_category(odoo, name, parent_id):
    return odoo.upsert("product.category", [("name", "=", name)], {"name": name, "parent_id": parent_id or False}, name)


def ensure_product(odoo, code, name, category_id, product_type, storable, cost):
    values = {
        "name": name, "default_code": code, "categ_id": category_id, "type": product_type,
        "is_storable": storable, "purchase_ok": True, "sale_ok": False,
        "standard_price": cost, "purchase_method": "receive",
        "description_purchase": f"Producto ficticio {code} para la demostración integral de Compras.",
    }
    template_id = odoo.upsert("product.template", [("default_code", "=", code)], values, f"{code} · {name}")
    if not template_id:
        return None, None
    variant_id = odoo.find("product.product", [("product_tmpl_id", "=", template_id)])
    return template_id, variant_id


def ensure_supplier_price(odoo, vendor_id, template_id, code, price, delay):
    if not vendor_id or not template_id:
        return
    domain = [("partner_id", "=", vendor_id), ("product_tmpl_id", "=", template_id)]
    odoo.upsert(
        "product.supplierinfo", domain,
        {"partner_id": vendor_id, "product_tmpl_id": template_id, "min_qty": 1, "price": price, "delay": delay},
        f"Tarifa proveedor · {code}",
    )


def ensure_order(odoo, scenario, vendor_id, products, buyer_id):
    order_id = odoo.find("purchase.order", [("name", "=", scenario["name"])])
    if order_id:
        print(f"{'REVISAR' if odoo.dry_run else 'EXISTE':10} purchase.order        {scenario['name']}")
        return order_id
    lines = []
    for code, quantity, price, discount in scenario["lines"]:
        product_id = products[code][1]
        if not product_id and not odoo.dry_run:
            raise RuntimeError(f"No se encontró variante para {code}")
        lines.append((0, 0, {
            "product_id": product_id, "product_qty": quantity, "price_unit": price,
            "discount": discount, "date_planned": dt(scenario["planned"]),
            "name": f"[{code}] {products[code][2]}",
        }))
    print(f"{'CREARÍA' if odoo.dry_run else 'CREAR':10} purchase.order        {scenario['name']}")
    if odoo.dry_run:
        return None
    order_values = {
        "name": scenario["name"], "partner_id": vendor_id, "user_id": buyer_id,
        "date_order": dt(scenario["date"]), "origin": PROJECT_NAME,
        "partner_ref": f"OFERTA-{scenario['name'][-3:]}",
        "notes": f"<p><b>DEMO GDG</b></p><p>{scenario['note']}</p>",
        "note": f"<p><b>DEMO GDG</b></p><p>{scenario['note']}</p>",
        "order_line": lines,
    }
    order_id = odoo.call("purchase.order", "create", [odoo.clean("purchase.order", order_values)])
    odoo.created += 1
    return order_id


def transition_order(odoo, order_id, scenario):
    if not order_id:
        return
    order_status = odoo.call("purchase.order", "read", [[order_id]], {"fields": ["state", "receipt_status"]})[0]
    state = order_status["state"]
    target = scenario["target"]
    if odoo.dry_run:
        print(f"REVISAR    purchase.workflow     {scenario['name']} · estado={state} · recepción={order_status.get('receipt_status')}")
        return
    if target == "sent" and state == "draft":
        odoo.call("purchase.order", "write", [[order_id], {"state": "sent"}])
    elif target == "to approve" and state in ("draft", "sent"):
        odoo.call("purchase.order", "write", [[order_id], {"state": "to approve"}])
    elif target in ("purchase", "received") and state in ("draft", "sent"):
        odoo.call("purchase.order", "button_confirm", [[order_id]])
    elif target in ("purchase", "received") and state == "to approve":
        odoo.call("purchase.order", "button_approve", [[order_id]])
    elif target == "cancel" and state != "cancel":
        odoo.call("purchase.order", "write", [[order_id], {"state": "cancel"}])

    if target not in ("purchase", "received"):
        return
    picking_ids = odoo.call("purchase.order", "read", [[order_id]], {"fields": ["picking_ids"]})[0]["picking_ids"]
    if target == "received" and not picking_ids:
        line_ids = odoo.call("purchase.order", "read", [[order_id]], {"fields": ["order_line"]})[0]["order_line"]
        for line_id in line_ids:
            line = odoo.call("purchase.order.line", "read", [[line_id]], {"fields": ["product_qty"]})[0]
            odoo.call("purchase.order.line", "write", [[line_id], {"qty_received": line["product_qty"]}])
    for picking_id in picking_ids:
        picking = odoo.call("stock.picking", "read", [[picking_id]], {"fields": ["state", "move_ids"]})[0]
        if picking["state"] == "done":
            continue
        odoo.call("stock.picking", "write", [[picking_id], {"scheduled_date": dt(scenario["planned"])}])
        if target == "received":
            for move_id in picking["move_ids"]:
                move = odoo.call("stock.move", "read", [[move_id]], {"fields": ["product_uom_qty"]})[0]
                odoo.call("stock.move", "write", [[move_id], {"quantity": move["product_uom_qty"], "picked": True}])
            odoo.call("stock.picking", "button_validate", [[picking_id]])


def ensure_activity(odoo, order_id, summary, offset, note, user_id):
    if not order_id or not odoo.supports("mail.activity"):
        return
    model_id = odoo.find("ir.model", [("model", "=", "purchase.order")])
    activity_type = odoo.find("mail.activity.type", [("name", "ilike", "Por hacer")]) or odoo.find("mail.activity.type", [])
    domain = [("res_model_id", "=", model_id), ("res_id", "=", order_id), ("summary", "=", summary)]
    odoo.upsert("mail.activity", domain, {
        "res_model_id": model_id, "res_id": order_id, "activity_type_id": activity_type,
        "summary": summary, "note": f"<p>{note}</p>", "date_deadline": (date.today() + timedelta(days=offset)).isoformat(),
        "user_id": user_id,
    }, summary)


def main():
    parser = argparse.ArgumentParser(description="Prepara una demo integral del módulo Compras para GDG Ingeniería.")
    parser.add_argument("--env", default="script/creacion-usuarios/.env")
    parser.add_argument("--dry-run", action="store_true", help="Muestra cambios sin modificar Odoo")
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
        raise RuntimeError("No se pudo autenticar el usuario administrador")
    odoo = Odoo(url, database, uid, password, args.dry_run)
    if not odoo.supports("purchase.order") or not odoo.supports("stock.picking"):
        raise RuntimeError("Compras e Inventario deben estar instalados")

    buyer_id = odoo.find("res.users", [("login", "=", "purchase.user")]) or uid
    categories = {}
    for name, parent_name in CATEGORIES:
        categories[name] = ensure_category(odoo, name, categories.get(parent_name))

    vendors = {}
    for name, email, city, _delay in VENDORS:
        vendors[name] = odoo.upsert("res.partner", [("name", "=", name)], {
            "name": name, "company_type": "company", "supplier_rank": 1,
            "email": email, "city": city, "comment": "Proveedor ficticio para la demostración integral de Compras.",
        }, name)

    products = {}
    for code, name, category, product_type, storable, cost, _unit, delay in PRODUCTS:
        template_id, variant_id = ensure_product(odoo, code, name, categories.get(category), product_type, storable, cost)
        products[code] = (template_id, variant_id, name)
        vendor_index = 0 if category in ("DEMO · Material eléctrico AT/MT", "DEMO · Equipos de prueba") else 1
        if category == "DEMO · Obras civiles":
            vendor_index = 2
        elif category == "DEMO · Servicios y arriendos":
            vendor_index = 3
        elif category == "DEMO · EPP y seguridad":
            vendor_index = 4
        vendor_name = VENDORS[vendor_index][0]
        ensure_supplier_price(odoo, vendors.get(vendor_name), template_id, code, cost, delay)

    orders = {}
    for scenario in ORDER_SCENARIOS:
        order_id = ensure_order(odoo, scenario, vendors.get(scenario["vendor"]), products, buyer_id)
        orders[scenario["name"]] = order_id
        transition_order(odoo, order_id, scenario)

    for order_name, summary, offset, note in ACTIVITIES:
        ensure_activity(odoo, orders.get(order_name), summary, offset, note, buyer_id)

    if not odoo.supports("purchase.requisition"):
        odoo.omit("Acuerdos de compra", "el módulo purchase_requisition no está instalado")

    print("\nResumen")
    if args.dry_run:
        print("Simulación completa: no se modificó Odoo.")
    else:
        demo_orders = odoo.call("purchase.order", "search_count", [[("name", "like", "DEMO-%")]])
        demo_products = odoo.call("product.template", "search_count", [[("default_code", "like", "DEMO-%")]])
        print(f"Demo lista: {odoo.created} registros creados y {odoo.updated} actualizados.")
        print(f"Control en Odoo: {demo_orders} documentos de compra demo · {demo_products} productos demo.")
    print("Cobertura: categorías, productos, proveedores, tarifas, RFQ, envío, atraso, aprobación, orden confirmada, recepción pendiente, recepción atrasada, recepción completa, cancelación y actividades.")
    for feature, reason in odoo.skipped:
        print(f"Pendiente por configuración: {feature} — {reason}.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, xmlrpc.client.Fault, xmlrpc.client.ProtocolError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
