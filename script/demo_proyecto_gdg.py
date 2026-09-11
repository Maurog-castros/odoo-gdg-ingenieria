#!/usr/bin/env python3
"""Create an attractive, idempotent GDG Project demo in Odoo."""

import argparse
import base64
import json
import sys
import urllib.request
import xmlrpc.client
from datetime import date, datetime, time, timedelta
from pathlib import Path


PROJECT_NAME = "Demo - Puesta en servicio Subestacion Energia Norte"
PARTNER_NAME = "Cliente Demo Energia Norte"
DEMO_MARKER = "[DEMO-GDG-PROYECTO]"

STAGES = (
    ("📐 Ingeniería y permisos", 10, False, "📥 Por iniciar"),
    ("📦 Compras y logística de obra", 20, False, "🔎 En revisión"),
    ("🏗️ Montaje electromecánico", 30, False, "⚙️ En ejecución"),
    ("⚡ Pruebas y energización", 40, False, "⛔ Bloqueada"),
    ("📄 Entrega documental y cierre", 50, False, "✅ Terminado"),
)

TAGS = (
    ("⚡ Crítica", 1), ("🦺 Seguridad", 2), ("📐 Ingeniería", 4),
    ("📦 Materiales", 3), ("🧪 Pruebas", 6), ("📄 Entregable", 9),
)

MILESTONES = (
    ("H1 · Ingeniería aprobada", -4, True),
    ("H2 · Montaje completado", 8, False),
    ("H3 · Energización autorizada", 15, False),
    ("H4 · Dossier y cierre", 22, False),
)

TASKS = (
    {"name": "A1 · Recepción de antecedentes y alcance contractual", "stage": "📐 Ingeniería y permisos", "deadline": -13, "hours": 5, "priority": "2", "state": "1_done", "users": ("project.user",), "tags": ("📐 Ingeniería", "📄 Entregable"), "milestone": "H1 · Ingeniería aprobada", "description": "<h3>Antecedentes contractuales revisados</h3><p>Se recibieron bases técnicas, planos unilineales, listado de equipos, protocolos exigidos y condiciones de acceso.</p><ul><li>Alcance y exclusiones contrastados con la oferta</li><li>Entregables y responsables identificados</li><li>Consultas técnicas cerradas con el cliente</li></ul><p><b>Resultado:</b> carpeta de inicio liberada para planificación.</p>"},
    {"name": "A2 · Plan HSE y acreditación del equipo", "stage": "📐 Ingeniería y permisos", "deadline": -12, "hours": 8, "priority": "3", "state": "1_done", "users": ("project.user",), "tags": ("🦺 Seguridad", "📄 Entregable"), "milestone": "H1 · Ingeniería aprobada", "description": "<h3>Personal habilitado para ingreso</h3><p>Se verificaron contratos, exámenes ocupacionales, certificaciones eléctricas, EPP y charla de inducción.</p><ul><li>Matriz de riesgos aprobada</li><li>Permisos de trabajo emitidos</li><li>Contactos de emergencia comunicados</li></ul><p><b>Resultado:</b> cuadrilla acreditada sin observaciones pendientes.</p>"},
    {"name": "01 · Reunión de inicio y permisos de trabajo", "stage": "📐 Ingeniería y permisos", "deadline": -12, "hours": 6, "priority": "1", "state": "1_done", "users": ("project.user",), "tags": ("🦺 Seguridad", "📄 Entregable"), "milestone": "H1 · Ingeniería aprobada", "description": "<h3>Inicio formal de la obra</h3><p>Se acordaron alcance, canales de comunicación, restricciones operacionales y ventanas de intervención.</p><ul><li>Acta de inicio firmada</li><li>Matriz de comunicaciones publicada</li><li>Reunión diaria fijada a las 08:00</li></ul><p><b>Resultado:</b> proyecto autorizado para comenzar.</p>"},
    {"name": "02 · Levantamiento técnico en subestación", "stage": "📐 Ingeniería y permisos", "deadline": -9, "hours": 18, "priority": "2", "state": "1_done", "users": ("project.user",), "tags": ("📐 Ingeniería", "🦺 Seguridad"), "milestone": "H1 · Ingeniería aprobada", "description": "<h3>Condiciones reales verificadas</h3><p>Se inspeccionaron patios AT/MT, tableros, protecciones, canalizaciones, señales y puntos de conexión.</p><ul><li>Registro fotográfico clasificado</li><li>Planos marcados conforme a terreno</li><li>Interferencias y restricciones documentadas</li></ul><p><b>Resultado:</b> levantamiento aceptado por Ingeniería.</p>"},
    {"name": "03 · Ingeniería y plan de maniobras", "stage": "📐 Ingeniería y permisos", "deadline": -4, "hours": 24, "priority": "2", "state": "1_done", "users": ("project.user",), "tags": ("📐 Ingeniería", "⚡ Crítica"), "milestone": "H1 · Ingeniería aprobada", "description": "<h3>Ingeniería aprobada</h3><p>Se definieron secuencia de montaje, bloqueos, pruebas previas, plan de maniobras y criterios de aceptación.</p><ul><li>Procedimiento de trabajo aprobado</li><li>Matriz de riesgos actualizada</li><li>Plan de maniobras validado por Operaciones</li></ul><p><b>Resultado:</b> hito H1 completado.</p>"},
    {"name": "04 · Materiales y equipos de prueba en obra", "stage": "📦 Compras y logística de obra", "deadline": -1, "hours": 12, "priority": "1", "users": ("inventory.user", "project.user"), "tags": ("📦 Materiales", "🧪 Pruebas"), "milestone": "H2 · Montaje completado", "description": "<h3>Control logístico</h3><p>Confirmar recepción de cables, pernos, EPP y equipos de prueba. Revisar series y calibraciones.</p>"},
    {"name": "05 · Montaje de equipos AT/MT", "stage": "🏗️ Montaje electromecánico", "deadline": 5, "hours": 72, "priority": "3", "users": ("project.user",), "tags": ("⚡ Crítica", "🦺 Seguridad"), "milestone": "H2 · Montaje completado", "description": "<h3>Montaje principal</h3><p>Montar equipos de alta y media tensión con controles diarios de calidad y seguridad.</p><p><b>Avance narrativo:</b> montaje mecánico completado; quedan terminaciones y torque final.</p>"},
    {"name": "06 · Integración SCADA y señales de control", "stage": "⚡ Pruebas y energización", "deadline": -2, "hours": 30, "priority": "3", "state": "04_waiting_normal", "users": ("project.user",), "tags": ("⚡ Crítica", "📐 Ingeniería"), "milestone": "H3 · Energización autorizada", "description": "<h3>Bloqueo visible</h3><p><b>Bloqueada:</b> falta matriz de señales revisada por el cliente.</p><p><b>Acción:</b> responsable de proyecto coordina aprobación en comité diario.</p>"},
    {"name": "07 · Pruebas de protecciones y control", "stage": "⚡ Pruebas y energización", "deadline": 10, "hours": 40, "priority": "3", "users": ("project.user",), "tags": ("🧪 Pruebas", "⚡ Crítica"), "milestone": "H3 · Energización autorizada", "description": "<h3>Pruebas eléctricas</h3><p>Ejecutar inyección secundaria, lógicas de protección, disparos y verificación de señales.</p>", "depends": ("06 · Integración SCADA y señales de control",)},
    {"name": "08 · Energización y puesta en servicio", "stage": "⚡ Pruebas y energización", "deadline": 15, "hours": 16, "priority": "3", "users": ("project.user",), "tags": ("🧪 Pruebas", "🦺 Seguridad", "⚡ Crítica"), "milestone": "H3 · Energización autorizada", "description": "<h3>Hito operacional</h3><p>Energizar con autorización del cliente, monitorear variables y registrar resultados.</p>", "depends": ("07 · Pruebas de protecciones y control",)},
    {"name": "09 · Protocolos e informe técnico", "stage": "📄 Entrega documental y cierre", "deadline": 19, "hours": 20, "priority": "2", "users": ("project.user",), "tags": ("📄 Entregable", "🧪 Pruebas"), "milestone": "H4 · Dossier y cierre", "description": "<h3>Dossier de calidad</h3><p>Consolidar protocolos firmados, resultados, fotografías, planos conforme a obra y observaciones.</p>", "depends": ("08 · Energización y puesta en servicio",)},
    {"name": "10 · Aprobación cliente, facturación y cierre", "stage": "📄 Entrega documental y cierre", "deadline": 22, "hours": 10, "priority": "2", "users": ("project.user", "invoicing.user"), "tags": ("📄 Entregable",), "milestone": "H4 · Dossier y cierre", "description": "<h3>Cierre comercial</h3><p>Obtener conformidad, liberar el hito de facturación y registrar lecciones aprendidas.</p>", "depends": ("09 · Protocolos e informe técnico",)},
    {"name": "♻️ Inspección semanal de seguridad", "stage": "🏗️ Montaje electromecánico", "deadline": 1, "hours": 2, "priority": "2", "users": ("project.user",), "tags": ("🦺 Seguridad",), "milestone": "H2 · Montaje completado", "description": "<h3>Rutina semanal</h3><p>Revisar EPP, permisos, orden del frente de trabajo y observaciones preventivas.</p>", "recurring": True},
)

SUBTASKS = (
    ("05.1 · Torque y registro de apriete", "05 · Montaje de equipos AT/MT", "🏗️ Montaje electromecánico", 2, 12, ("🦺 Seguridad",)),
    ("05.2 · Conexionado de control", "05 · Montaje de equipos AT/MT", "🏗️ Montaje electromecánico", 4, 18, ("📐 Ingeniería",)),
    ("07.1 · Inyección secundaria de relés", "07 · Pruebas de protecciones y control", "⚡ Pruebas y energización", 8, 16, ("🧪 Pruebas",)),
)

UPDATES = (
    ("Semana 1 · Ingeniería liberada", -7, 30, "done", "<p>Levantamiento e ingeniería completados. Sin accidentes ni desviaciones de calidad.</p>"),
    ("Semana 2 · Montaje en curso", -2, 58, "on_track", "<p>Equipos principales montados y materiales recibidos. Se mantiene fecha objetivo.</p>"),
    ("Comité actual · Atención requerida", 0, 68, "at_risk", "<p><b>Riesgo:</b> la matriz de señales SCADA espera aprobación del cliente. El equipo puede continuar terminaciones mecánicas.</p>"),
)

ATTACHMENTS = (
    ("02 · Levantamiento técnico en subestación", "DEMO - registro_levantamiento.txt", "Registro ficticio de levantamiento\n- Planos revisados\n- Fotografías referenciadas\n- Sin hallazgos críticos\n"),
    ("05 · Montaje de equipos AT/MT", "DEMO - control_calidad_montaje.txt", "Control ficticio de montaje\n- Torque parcial verificado\n- Conexionado en ejecución\n- Evidencias cargadas en la tarea\n"),
    ("07 · Pruebas de protecciones y control", "DEMO - protocolo_pruebas_PES.txt", "Protocolo ficticio de pruebas\n- Inyección secundaria\n- Lógicas de disparo\n- Señales SCADA\n- Firma cliente pendiente\n"),
)

LEGACY_TASK_NAMES = (
    "01 - Levantamiento tecnico", "02 - Planificacion de montaje",
    "03 - Montaje de equipos AT/MT", "04 - Pruebas electricas PES", "05 - Informe y cierre",
)


class Odoo:
    def __init__(self, url, database, uid, password, dry_run=False):
        self.url, self.database, self.uid, self.password = url, database, uid, password
        self.dry_run = dry_run
        self._fields, self._models = {}, None
        self.created, self.updated, self.skipped = 0, 0, []

    def call(self, model, method, args, kwargs=None):
        proxy = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/object")
        return proxy.execute_kw(self.database, self.uid, self.password, model, method, args, kwargs or {})

    def models(self):
        if self._models is None:
            rows = self.call("ir.model", "search_read", [[]], {"fields": ["model"], "limit": 10000})
            self._models = {row["model"] for row in rows}
        return self._models

    def supports(self, model):
        return model in self.models()

    def fields(self, model):
        if model not in self._fields:
            self._fields[model] = self.call(model, "fields_get", [], {"attributes": ["readonly"]})
        return self._fields[model]

    def clean(self, model, values):
        fields = self.fields(model)
        return {name: value for name, value in values.items() if name in fields and not fields[name].get("readonly")}

    def find(self, model, domain):
        ids = self.call(model, "search", [domain], {"limit": 1})
        return ids[0] if ids else None

    def upsert(self, model, domain, values, label):
        record_id = self.find(model, domain)
        clean_values = self.clean(model, values)
        if record_id:
            print(f"{'REVISAR' if self.dry_run else 'ACTUALIZAR':10} {model:21} {label}")
            if not self.dry_run and clean_values:
                self.call(model, "write", [[record_id], clean_values])
                self.updated += 1
            return record_id
        print(f"{'CREARÍA' if self.dry_run else 'CREAR':10} {model:21} {label}")
        if self.dry_run:
            return None
        record_id = self.call(model, "create", [clean_values])
        self.created += 1
        return record_id

    def omit(self, feature, reason):
        self.skipped.append((feature, reason))
        print(f"OMITIR     {feature}: {reason}")


def load_env(path):
    values = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip("\"'")
    return values


def database_from_url(url):
    with urllib.request.urlopen(f"{url}/web/database/list", timeout=20) as response:
        databases = json.loads(response.read().decode("utf-8")).get("result", [])
    if len(databases) != 1:
        raise RuntimeError("Define ODOO_DB en .env cuando Odoo tenga cero o varias bases")
    return databases[0]


def day(anchor, offset):
    return (anchor + timedelta(days=offset)).isoformat()


def deadline(anchor, offset):
    value = datetime.combine(anchor + timedelta(days=offset), time(18, 0))
    return value.strftime("%Y-%m-%d %H:%M:%S")


def user_ids(odoo, logins, fallback):
    result = []
    for login in logins:
        user_id = odoo.find("res.users", [("login", "=", login)])
        if user_id:
            result.append(user_id)
    return result or [fallback]


def add_chatter(odoo, model, record_id, body):
    if not record_id or not odoo.supports("mail.message"):
        return
    existing = odoo.find("mail.message", [("model", "=", model), ("res_id", "=", record_id), ("body", "ilike", DEMO_MARKER)])
    if existing:
        print("EXISTE     mail.message          Seguimiento visual")
        return
    print(f"{'CREARÍA' if odoo.dry_run else 'CREAR':10} mail.message          Seguimiento visual")
    if not odoo.dry_run:
        odoo.call(model, "message_post", [[record_id]], {"body": f"<p>{DEMO_MARKER}</p>{body}", "message_type": "comment", "subtype_xmlid": "mail.mt_comment"})
        odoo.created += 1


def main():
    parser = argparse.ArgumentParser(description="Prepara una demo integral y visual del módulo Proyectos para GDG Ingeniería.")
    parser.add_argument("--env", default="script/creacion-usuarios/.env")
    parser.add_argument("--dry-run", action="store_true", help="Muestra lo que se crearía o actualizaría")
    parser.add_argument("--start-date", help="Inicio YYYY-MM-DD; por defecto, 14 días antes de hoy")
    parser.add_argument("--project-id", type=int, help="ID de un proyecto existente que recibirá la demo")
    args = parser.parse_args()

    env_path = Path(args.env)
    if not env_path.exists():
        raise RuntimeError(f"No existe el archivo de entorno: {env_path}")
    config = load_env(env_path)
    url = config.get("URLODOO", "").rstrip("/")
    admin, password = config.get("ADMIN-USER", ""), config.get("PASS", "")
    if not url or not admin or not password:
        raise RuntimeError(".env debe contener URLODOO, ADMIN-USER y PASS")
    database = config.get("ODOO_DB") or database_from_url(url)
    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(database, admin, password, {})
    if not uid:
        raise RuntimeError("No se pudo autenticar el usuario administrador")
    anchor = date.fromisoformat(args.start_date) if args.start_date else date.today() - timedelta(days=14)
    odoo = Odoo(url, database, uid, password, args.dry_run)
    if not odoo.supports("project.project") or not odoo.supports("project.task"):
        raise RuntimeError("El módulo Proyectos no está instalado")

    target_name = PROJECT_NAME
    project_domain = [("name", "=", PROJECT_NAME)]
    if args.project_id:
        rows = odoo.call("project.project", "read", [[args.project_id]], {"fields": ["name"]})
        if not rows:
            raise RuntimeError(f"No existe el proyecto con ID {args.project_id}")
        target_name = rows[0]["name"]
        project_domain = [("id", "=", args.project_id)]

    print(f"\nDemo: {target_name} (proyecto {args.project_id or 'por nombre'})\nPeriodo: {day(anchor, 0)} → {day(anchor, 36)}\n")
    partner_id = odoo.upsert("res.partner", [("name", "=", PARTNER_NAME)], {"name": PARTNER_NAME, "email": "cliente.energia.norte@example.com", "city": "Antofagasta", "comment": "Contacto ficticio para demostración de GDG Ingeniería."}, PARTNER_NAME)

    tag_ids = {}
    for name, color in TAGS:
        tag_ids[name] = odoo.upsert("project.tags", [("name", "=", name)], {"name": name, "color": color}, name)

    manager_ids = user_ids(odoo, ("project.user",), uid)
    sale_line_id = None
    if odoo.supports("sale.order") and odoo.supports("sale.order.line"):
        sale_order_id = odoo.find("sale.order", [("name", "=", "DEMO-COT-ENERGIA-NORTE")])
        if sale_order_id:
            sale_line_id = odoo.find("sale.order.line", [("order_id", "=", sale_order_id)])
    if not sale_line_id:
        odoo.omit("Vínculo comercial", "ejecuta primero seed_demo_data.py para crear DEMO-COT-ENERGIA-NORTE")
    project_values = {
        "name": target_name, "partner_id": partner_id or False, "user_id": manager_ids[0],
        "date_start": day(anchor, 0), "date": day(anchor, 36),
        "tag_ids": [(6, 0, [tag_ids[name] for name in ("⚡ Crítica", "🧪 Pruebas") if tag_ids.get(name)])],
        "privacy_visibility": "employees", "allow_milestones": True, "allow_task_dependencies": True,
        "allow_recurring_tasks": True, "allow_billable": True,
        "sale_line_id": sale_line_id or False,
        "description": "<h2>⚡ Puesta en servicio · Energía Norte</h2><p><b>Objetivo:</b> montar, probar y energizar una subestación con trazabilidad técnica, documental y comercial.</p><table class='table table-sm'><tbody><tr><td><b>Contrato demo</b></td><td>$18.500.000 CLP</td></tr><tr><td><b>Estado ejecutivo</b></td><td>68% · En riesgo controlado</td></tr><tr><td><b>Próximo hito</b></td><td>Montaje completado</td></tr></tbody></table><p>Todos los nombres, importes y documentos son ficticios.</p>",
    }
    project_id = odoo.upsert("project.project", project_domain, project_values, target_name)
    project_ref = project_id or 0

    stage_ids = {}
    for name, sequence, fold, previous_name in STAGES:
        values = {"name": name, "sequence": sequence, "fold": fold, "is_closed": fold}
        if project_id:
            values["project_ids"] = [(4, project_id)]
        stage_domain = ["|", ("name", "=", name), ("name", "=", previous_name)]
        stage_ids[name] = odoo.upsert("project.task.type", stage_domain, values, name)

    milestone_ids = {}
    if odoo.supports("project.milestone"):
        for name, offset, reached in MILESTONES:
            milestone_ids[name] = odoo.upsert("project.milestone", [("name", "=", name), ("project_id", "=", project_ref)], {"name": name, "deadline": day(anchor, offset + 14), "is_reached": reached, "project_id": project_ref}, name)
    else:
        odoo.omit("Hitos", "modelo project.milestone no disponible")

    task_ids = {}
    for task in TASKS:
        start_offset = task["deadline"] - max(1, round(task["hours"] / 8))
        task_state = task.get("state", "01_in_progress")
        values = {
            "name": task["name"], "project_id": project_ref, "partner_id": partner_id or False,
            "planned_date_begin": deadline(anchor, start_offset + 14),
            "stage_id": stage_ids.get(task["stage"]) or False, "date_deadline": deadline(anchor, task["deadline"] + 14),
            "allocated_hours": task["hours"], "priority": task["priority"],
            "state": task_state,
            "user_ids": [(6, 0, user_ids(odoo, task["users"], manager_ids[0]))],
            "tag_ids": [(6, 0, [tag_ids[name] for name in task["tags"] if tag_ids.get(name)])],
            "milestone_id": milestone_ids.get(task.get("milestone")) or False, "description": task["description"],
            "sale_line_id": sale_line_id or False,
        }
        if task.get("recurring"):
            values.update({"recurring_task": True, "repeat_interval": 1, "repeat_unit": "week", "repeat_type": "forever"})
        task_ids[task["name"]] = odoo.upsert("project.task", [("name", "=", task["name"]), ("project_id", "=", project_ref)], values, task["name"])

    for name, parent, stage, offset, hours, tags in SUBTASKS:
        values = {"name": name, "project_id": project_ref, "parent_id": task_ids.get(parent) or False, "stage_id": stage_ids.get(stage) or False, "planned_date_begin": deadline(anchor, offset + 12), "date_deadline": deadline(anchor, offset + 14), "allocated_hours": hours, "state": "01_in_progress", "user_ids": [(6, 0, manager_ids)], "tag_ids": [(6, 0, [tag_ids[tag] for tag in tags if tag_ids.get(tag)])], "description": f"<p>Subtarea operativa de <b>{parent}</b>.</p>"}
        task_ids[name] = odoo.upsert("project.task", [("name", "=", name), ("project_id", "=", project_ref)], values, name)

    if "active" in odoo.fields("project.task"):
        for legacy_name in LEGACY_TASK_NAMES:
            legacy_id = odoo.find("project.task", [("name", "=", legacy_name), ("project_id", "=", project_ref), ("active", "=", True)])
            if legacy_id:
                print(f"{'ARCHIVARÍA' if args.dry_run else 'ARCHIVAR':10} project.task          {legacy_name}")
                if not args.dry_run:
                    odoo.call("project.task", "write", [[legacy_id], {"active": False}])
                    odoo.updated += 1

    if "depend_on_ids" in odoo.fields("project.task"):
        for task in TASKS:
            dependencies = [task_ids[name] for name in task.get("depends", ()) if task_ids.get(name)]
            task_id = task_ids.get(task["name"])
            if task_id and dependencies:
                print(f"{'REVISAR' if args.dry_run else 'ENLAZAR':10} project.task          Dependencias · {task['name']}")
                if not args.dry_run:
                    odoo.call("project.task", "write", [[task_id], {"depend_on_ids": [(6, 0, dependencies)]}])
    else:
        odoo.omit("Dependencias", "campo depend_on_ids no disponible")

    if odoo.supports("project.update"):
        for name, offset, progress, status, description in UPDATES:
            odoo.upsert("project.update", [("name", "=", name), ("project_id", "=", project_ref)], {"name": name, "project_id": project_ref, "user_id": manager_ids[0], "date": day(date.today(), offset), "progress": progress, "status": status, "description": description}, name)
    else:
        odoo.omit("Actualizaciones del proyecto", "modelo project.update no disponible")

    for task_name, filename, content in ATTACHMENTS:
        task_id = task_ids.get(task_name)
        if task_id:
            odoo.upsert("ir.attachment", [("name", "=", filename), ("res_model", "=", "project.task"), ("res_id", "=", task_id)], {"name": filename, "res_model": "project.task", "res_id": task_id, "type": "binary", "datas": base64.b64encode(content.encode("utf-8")).decode("ascii"), "description": "Documento ficticio para la demostración."}, filename)

    add_chatter(odoo, "project.project", project_id, "<p>⚠️ <b>Comité de avance:</b> la integración SCADA requiere aprobación. El montaje continúa y el responsable hará seguimiento en 24 horas.</p>")
    analytic_fields = odoo.fields("account.analytic.line") if odoo.supports("account.analytic.line") else {}
    if not ({"project_id", "task_id"} & set(analytic_fields)):
        odoo.omit("Partes de horas", "la extensión de partes de horas no está instalada o vinculada a Proyectos")

    print("\nResumen")
    print("Simulación completa: no se modificó Odoo." if args.dry_run else f"Demo lista: {odoo.created} registros creados y {odoo.updated} actualizados.")
    if not args.dry_run:
        active_tasks = odoo.call("project.task", "search_count", [[("project_id", "=", project_ref), ("active", "=", True)]])
        completed_tasks = odoo.call("project.task", "search_count", [[("project_id", "=", project_ref), ("active", "=", True), ("state", "=", "1_done")]])
        milestones = odoo.call("project.milestone", "search_count", [[("project_id", "=", project_ref)]]) if odoo.supports("project.milestone") else 0
        updates = odoo.call("project.update", "search_count", [[("project_id", "=", project_ref)]]) if odoo.supports("project.update") else 0
        print(f"Control en Odoo: {active_tasks} tareas activas · {completed_tasks} terminadas · {milestones} hitos · {updates} actualizaciones.")
    print("Cobertura: tablero, etapas, responsables, Gantt/calendario, prioridades, etiquetas, subtareas, dependencias, hitos, recurrencia, actualizaciones, adjuntos y chatter.")
    for feature, reason in odoo.skipped:
        print(f"Pendiente por configuración: {feature} — {reason}.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError, xmlrpc.client.Fault, xmlrpc.client.ProtocolError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
