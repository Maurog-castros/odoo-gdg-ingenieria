#!/usr/bin/env python3
"""Create a four-stage, full-cycle construction project demo in Odoo."""

import argparse
import sys
import xmlrpc.client
from datetime import date, datetime, time, timedelta
from pathlib import Path

from demo_proyecto_gdg import Odoo, database_from_url, load_env


STAGES = (
    ("1 · Cotización", 10),
    ("2 · Diagnóstico en terreno", 20),
    ("3 · Ejecución de obra", 30),
    ("4 · Cierre / entrega de obra", 40),
)

TAGS = (
    ("💰 Cotización", 11), ("🚧 Terreno", 3), ("📐 Ingeniería", 4),
    ("🦺 Seguridad", 2), ("⚡ Crítica", 1), ("🧪 Pruebas", 6), ("📄 Entregable", 9),
)

MILESTONES = (
    ("M1 · Oferta adjudicada", -24, True),
    ("M2 · Diagnóstico aprobado", -10, True),
    ("M3 · Obra ejecutada", 10, False),
    ("M4 · Entrega aceptada", 22, False),
)

TASKS = (
    # 1 · Cotización
    {"code": "C1", "name": "C1 · Revisar bases, alcance y condiciones comerciales", "stage": "1 · Cotización", "start": -35, "end": -33, "hours": 12, "state": "1_done", "tags": ("💰 Cotización", "📐 Ingeniería"), "milestone": "M1 · Oferta adjudicada", "description": "<h3>Objetivo</h3><p>Comprender exactamente qué solicita el cliente y qué debe quedar fuera de la oferta.</p><h3>Actividades realizadas</h3><ul><li>Revisión de bases administrativas y técnicas</li><li>Identificación de entregables, multas, garantías y plazos</li><li>Registro de consultas y supuestos comerciales</li></ul><p><b>Resultado:</b> matriz de alcance y exclusiones aprobada por el equipo comercial.</p>"},
    {"code": "C2", "name": "C2 · Preparar cubicación y análisis de precios unitarios", "stage": "1 · Cotización", "start": -33, "end": -30, "hours": 28, "state": "1_done", "tags": ("💰 Cotización", "📐 Ingeniería"), "milestone": "M1 · Oferta adjudicada", "description": "<h3>Objetivo</h3><p>Construir el costo interno de la obra sin exponer el detalle sensible al cliente.</p><h3>Actividades realizadas</h3><ul><li>Cubicación de materiales y horas hombre</li><li>Costeo de equipos, movilización y maquinaria</li><li>Aplicación de contingencia y margen objetivo</li></ul><p><b>Resultado:</b> presupuesto interno trazable por partida.</p>"},
    {"code": "C3", "name": "C3 · Solicitar precios a proveedores críticos", "stage": "1 · Cotización", "start": -31, "end": -28, "hours": 14, "state": "1_done", "tags": ("💰 Cotización",), "milestone": "M1 · Oferta adjudicada", "description": "<h3>Objetivo</h3><p>Respaldar la oferta con precios y plazos vigentes de materiales y servicios críticos.</p><h3>Actividades realizadas</h3><ul><li>Solicitud de precios de cables y terminales</li><li>Cotización de grúa y transporte especial</li><li>Comparación de validez, moneda y plazo de entrega</li></ul><p><b>Resultado:</b> proveedores preferentes seleccionados para la propuesta.</p>"},
    {"code": "C4", "name": "C4 · Emitir oferta técnica y obtener adjudicación", "stage": "1 · Cotización", "start": -28, "end": -24, "hours": 18, "state": "1_done", "tags": ("💰 Cotización", "📄 Entregable"), "milestone": "M1 · Oferta adjudicada", "depends": ("C1", "C2", "C3"), "description": "<h3>Objetivo</h3><p>Entregar una propuesta clara para el cliente y conservar el detalle de costos internamente.</p><h3>Actividades realizadas</h3><ul><li>Revisión técnica y comercial</li><li>Emisión de oferta con alcance macro</li><li>Registro de aclaraciones y orden de compra del cliente</li></ul><p><b>Resultado:</b> oferta adjudicada y proyecto autorizado.</p>"},

    # 2 · Diagnóstico en terreno
    {"code": "D1", "name": "D1 · Coordinar visita, accesos y permisos de trabajo", "stage": "2 · Diagnóstico en terreno", "start": -23, "end": -21, "hours": 10, "state": "1_done", "tags": ("🚧 Terreno", "🦺 Seguridad"), "milestone": "M2 · Diagnóstico aprobado", "depends": ("C4",), "description": "<h3>Objetivo</h3><p>Asegurar que la inspección se ejecute con personal acreditado y sin interferir la operación.</p><ul><li>Coordinación de fecha y ventana operacional</li><li>Acreditación del equipo técnico</li><li>Permisos, EPP y charla de ingreso</li></ul><p><b>Resultado:</b> visita ejecutada sin incidentes.</p>"},
    {"code": "D2", "name": "D2 · Levantar instalaciones y condiciones existentes", "stage": "2 · Diagnóstico en terreno", "start": -21, "end": -18, "hours": 24, "state": "1_done", "tags": ("🚧 Terreno", "📐 Ingeniería"), "milestone": "M2 · Diagnóstico aprobado", "description": "<h3>Objetivo</h3><p>Contrastar planos y antecedentes con la configuración real de la instalación.</p><ul><li>Inspección de patios, tableros y canalizaciones</li><li>Registro fotográfico georreferenciado</li><li>Mediciones y planos marcados en terreno</li></ul><p><b>Resultado:</b> levantamiento conforme a obra disponible para diseño.</p>"},
    {"code": "D3", "name": "D3 · Diagnosticar equipos, protecciones y señales", "stage": "2 · Diagnóstico en terreno", "start": -18, "end": -14, "hours": 32, "state": "1_done", "tags": ("🚧 Terreno", "🧪 Pruebas", "⚡ Crítica"), "milestone": "M2 · Diagnóstico aprobado", "description": "<h3>Objetivo</h3><p>Determinar el estado técnico y las brechas que condicionan la intervención.</p><ul><li>Inspección de equipos AT/MT</li><li>Revisión de ajustes de protecciones</li><li>Validación de señales de control y SCADA</li></ul><p><b>Resultado:</b> hallazgos clasificados por criticidad.</p>"},
    {"code": "D4", "name": "D4 · Emitir diagnóstico y plan definitivo de intervención", "stage": "2 · Diagnóstico en terreno", "start": -14, "end": -10, "hours": 20, "state": "1_done", "tags": ("📐 Ingeniería", "📄 Entregable"), "milestone": "M2 · Diagnóstico aprobado", "depends": ("D2", "D3"), "description": "<h3>Objetivo</h3><p>Convertir los hallazgos de terreno en un plan ejecutable y aprobado.</p><ul><li>Informe de condición y recomendaciones</li><li>Secuencia, recursos y restricciones</li><li>Revisión del plan con cliente y Operaciones</li></ul><p><b>Resultado:</b> diagnóstico aprobado y frente liberado.</p>"},

    # 3 · Ejecución de obra
    {"code": "E1", "name": "E1 · Movilizar personal, equipos y materiales", "stage": "3 · Ejecución de obra", "start": -9, "end": -6, "hours": 24, "state": "1_done", "tags": ("🚧 Terreno", "🦺 Seguridad"), "milestone": "M3 · Obra ejecutada", "depends": ("D4",), "description": "<h3>Objetivo</h3><p>Instalar el frente de trabajo con recursos completos y trazables.</p><ul><li>Ingreso de cuadrilla y equipos de prueba</li><li>Recepción y control de materiales</li><li>Segregación, señalización y charla diaria</li></ul><p><b>Resultado:</b> frente habilitado para ejecutar.</p>"},
    {"code": "E2", "name": "E2 · Ejecutar adecuaciones civiles y soportes", "stage": "3 · Ejecución de obra", "start": -5, "end": 2, "hours": 64, "state": "01_in_progress", "tags": ("🚧 Terreno", "🦺 Seguridad"), "milestone": "M3 · Obra ejecutada", "description": "<h3>Objetivo</h3><p>Preparar fundaciones, canalizaciones y estructuras necesarias para el montaje.</p><ul><li>Replanteo y excavaciones controladas</li><li>Hormigonado y montaje de soportes</li><li>Inspecciones de calidad y liberación</li></ul><p><b>Estado:</b> soportes principales terminados; quedan remates.</p>"},
    {"code": "E3", "name": "E3 · Montar equipos y completar conexionado eléctrico", "stage": "3 · Ejecución de obra", "start": -2, "end": 7, "hours": 96, "state": "01_in_progress", "tags": ("🚧 Terreno", "⚡ Crítica"), "milestone": "M3 · Obra ejecutada", "description": "<h3>Objetivo</h3><p>Instalar equipos AT/MT y dejar completos los circuitos de fuerza, control y protección.</p><ul><li>Izaje, nivelación y torque</li><li>Tendido y terminación de cables</li><li>Conexionado de control y señales</li></ul><p><b>Estado:</b> montaje mecánico en curso.</p>"},
    {"code": "E4", "name": "E4 · Realizar control de calidad y pruebas internas", "stage": "3 · Ejecución de obra", "start": 7, "end": 10, "hours": 30, "state": "04_waiting_normal", "tags": ("🧪 Pruebas", "⚡ Crítica"), "milestone": "M3 · Obra ejecutada", "depends": ("E2", "E3"), "description": "<h3>Objetivo</h3><p>Liberar la obra antes de convocar al cliente a las pruebas de aceptación.</p><ul><li>Inspección visual y torque final</li><li>Continuidad, aislamiento y pruebas funcionales</li><li>Cierre de observaciones de calidad</li></ul><p><b>Estado:</b> en espera del término de montaje y obras civiles.</p>"},

    # 4 · Cierre / entrega
    {"code": "F1", "name": "F1 · Ejecutar pruebas de aceptación con el cliente", "stage": "4 · Cierre / entrega de obra", "start": 11, "end": 14, "hours": 28, "state": "01_in_progress", "tags": ("🧪 Pruebas", "📄 Entregable"), "milestone": "M4 · Entrega aceptada", "depends": ("E4",), "description": "<h3>Objetivo</h3><p>Demostrar que equipos, protecciones y controles cumplen los criterios acordados.</p><ul><li>Pruebas SAT y simulación de señales</li><li>Registro conjunto de resultados</li><li>Lista de pendientes de entrega</li></ul><p><b>Entregable:</b> protocolos firmados por ambas partes.</p>"},
    {"code": "F2", "name": "F2 · Consolidar dossier y planos conforme a obra", "stage": "4 · Cierre / entrega de obra", "start": 14, "end": 18, "hours": 26, "state": "01_in_progress", "tags": ("📐 Ingeniería", "📄 Entregable"), "milestone": "M4 · Entrega aceptada", "depends": ("F1",), "description": "<h3>Objetivo</h3><p>Entregar toda la evidencia técnica necesaria para operar y mantener la instalación.</p><ul><li>Planos as-built</li><li>Protocolos y certificados</li><li>Fotografías, manuales y respaldos de configuración</li></ul><p><b>Entregable:</b> dossier digital indexado.</p>"},
    {"code": "F3", "name": "F3 · Capacitar operación y realizar entrega formal", "stage": "4 · Cierre / entrega de obra", "start": 16, "end": 20, "hours": 16, "state": "01_in_progress", "tags": ("📄 Entregable", "🦺 Seguridad"), "milestone": "M4 · Entrega aceptada", "depends": ("F1",), "description": "<h3>Objetivo</h3><p>Transferir al cliente el conocimiento operativo y las restricciones de seguridad.</p><ul><li>Capacitación a operadores y mantenedores</li><li>Entrega de manuales y contactos de soporte</li><li>Firma del acta de entrega</li></ul><p><b>Entregable:</b> registro de asistencia y acta firmada.</p>"},
    {"code": "F4", "name": "F4 · Cerrar contrato, facturación y lecciones aprendidas", "stage": "4 · Cierre / entrega de obra", "start": 20, "end": 22, "hours": 12, "state": "01_in_progress", "tags": ("💰 Cotización", "📄 Entregable"), "milestone": "M4 · Entrega aceptada", "depends": ("F2", "F3"), "description": "<h3>Objetivo</h3><p>Completar el cierre contractual, económico y organizacional del proyecto.</p><ul><li>Conformidad y liberación del último cobro</li><li>Revisión de costos, margen y pendientes</li><li>Lecciones aprendidas y archivo final</li></ul><p><b>Resultado esperado:</b> proyecto cerrado sin documentos ni cobros pendientes.</p>"},
)


def stamp(offset):
    return datetime.combine(date.today() + timedelta(days=offset), time(18, 0)).strftime("%Y-%m-%d %H:%M:%S")


def main():
    parser = argparse.ArgumentParser(description="Carga una demo de proyecto desde cotización hasta entrega.")
    parser.add_argument("--env", default="script/creacion-usuarios/.env")
    parser.add_argument("--project-id", type=int, default=3)
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
        raise RuntimeError("No se pudo autenticar el usuario administrador")
    odoo = Odoo(url, database, uid, password, args.dry_run)
    project_rows = odoo.call("project.project", "read", [[args.project_id]], {"fields": ["name"]})
    if not project_rows:
        raise RuntimeError(f"No existe el proyecto {args.project_id}")
    project_name = project_rows[0]["name"]
    manager_id = odoo.find("res.users", [("login", "=", "project.user")]) or uid
    existing_tasks = odoo.call("project.task", "search_count", [[("project_id", "=", args.project_id), ("active", "=", True)]])
    print(f"Proyecto {args.project_id}: {project_name} · {existing_tasks} tareas activas antes de la carga")

    tags = {}
    for name, color in TAGS:
        tags[name] = odoo.upsert("project.tags", [("name", "=", name)], {"name": name, "color": color}, name)

    odoo.upsert("project.project", [("id", "=", args.project_id)], {
        "name": project_name, "user_id": manager_id,
        "date_start": (date.today() - timedelta(days=35)).isoformat(), "date": (date.today() + timedelta(days=22)).isoformat(),
        "allow_milestones": True, "allow_task_dependencies": True, "allow_recurring_tasks": True,
        "description": "<h2>Ciclo integral de una obra</h2><p>Demo desde la evaluación comercial hasta la entrega técnica, contractual y económica.</p><p><b>Avance:</b> cotización y diagnóstico terminados; ejecución en curso; cierre planificado.</p>",
    }, project_name)

    stages = {}
    for name, sequence in STAGES:
        stages[name] = odoo.upsert("project.task.type", [("name", "=", name)], {
            "name": name, "sequence": sequence, "fold": False, "project_ids": [(4, args.project_id)],
        }, name)

    milestones = {}
    for name, offset, reached in MILESTONES:
        milestones[name] = odoo.upsert("project.milestone", [("name", "=", name), ("project_id", "=", args.project_id)], {
            "name": name, "project_id": args.project_id, "deadline": (date.today() + timedelta(days=offset)).isoformat(), "is_reached": reached,
        }, name)

    task_ids = {}
    for task in TASKS:
        values = {
            "name": task["name"], "project_id": args.project_id, "stage_id": stages.get(task["stage"]),
            "planned_date_begin": stamp(task["start"]), "date_deadline": stamp(task["end"]),
            "allocated_hours": task["hours"], "state": task["state"], "priority": "2" if "⚡ Crítica" in task["tags"] else "1",
            "user_ids": [(6, 0, [manager_id])], "tag_ids": [(6, 0, [tags[name] for name in task["tags"] if tags.get(name)])],
            "milestone_id": milestones.get(task["milestone"]), "description": task["description"],
        }
        task_ids[task["code"]] = odoo.upsert("project.task", [("name", "=", task["name"]), ("project_id", "=", args.project_id)], values, task["name"])

    for task in TASKS:
        dependencies = [task_ids[code] for code in task.get("depends", ()) if task_ids.get(code)]
        task_id = task_ids.get(task["code"])
        if task_id and dependencies and not args.dry_run:
            odoo.call("project.task", "write", [[task_id], {"depend_on_ids": [(6, 0, dependencies)]}])

    if not args.dry_run:
        active = odoo.call("project.task", "search_count", [[("project_id", "=", args.project_id), ("active", "=", True)]])
        done = odoo.call("project.task", "search_count", [[("project_id", "=", args.project_id), ("active", "=", True), ("state", "=", "1_done")]])
        print(f"Demo lista: {active} tareas activas · {done} terminadas · 4 etapas · 4 hitos.")
    else:
        print("Simulación completa: no se modificó Odoo.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, xmlrpc.client.Fault, xmlrpc.client.ProtocolError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
