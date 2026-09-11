# Demo: puesta en servicio de una subestación

## Objetivo

Practicar el uso del módulo **Proyectos** para planificar un servicio típico de GDG Ingeniería: montaje y pruebas eléctricas para poner en servicio una subestación.

El caso usa datos ficticios inspirados en los servicios públicos de la empresa. No representa un contrato real.

## Resultado esperado

Al terminar debe existir:

- Proyecto: `Demo - Puesta en servicio Subestacion Energia Norte`.
- Cliente: `Cliente Demo Energia Norte`.
- Tablero con cinco etapas visuales y una obra en ejecución.
- Trece tareas principales y tres subtareas, con responsables, fechas, horas planificadas, prioridades y etiquetas.
- Cinco actividades iniciales terminadas y documentadas para mostrar el historial real de ejecución.
- Cuatro hitos, dependencias entre tareas y tres actualizaciones ejecutivas.
- Una tarea atrasada y bloqueada para mostrar gestión de riesgos.
- Tres documentos ficticios adjuntos y una conversación de seguimiento.

## Preparar la demo automáticamente

El inspector consulta la versión, modelos y campos sin modificar la base:

```bash
python3 script/inspect_project_capabilities.py --env script/creacion-usuarios/.env
```

Ejecuta primero la simulación y después la carga:

```bash
python3 script/demo_proyecto_gdg.py --env script/creacion-usuarios/.env --dry-run
python3 script/demo_proyecto_gdg.py --env script/creacion-usuarios/.env
```

Para cargar la demo en un proyecto específico de la URL de Odoo, usa su ID:

```bash
python3 script/demo_proyecto_gdg.py --env script/creacion-usuarios/.env --project-id 2 --dry-run
python3 script/demo_proyecto_gdg.py --env script/creacion-usuarios/.env --project-id 2
```

Las fechas se sitúan alrededor del día de ejecución para que el tablero siempre muestre pasado, presente y futuro. Para repetir una fecha concreta:

```bash
python3 script/demo_proyecto_gdg.py --env script/creacion-usuarios/.env --start-date 2026-08-28
```

El script se adapta a los campos disponibles, busca cada registro antes de crearlo y puede ejecutarse nuevamente sin duplicar la demo.

## Guion de demostración con efecto wow

1. Entra a **Proyectos** y abre `Demo - Puesta en servicio Subestacion Energia Norte`.
2. Presenta la portada ejecutiva: contrato ficticio, 68% de avance, siguiente hito y fecha final.
3. Abre el tablero Kanban y recorre las fases reales: Ingeniería y permisos, Compras y logística, Montaje electromecánico, Pruebas y energización, y Entrega documental y cierre.
4. En **Ingeniería y permisos**, abre una de las cinco tareas terminadas. Muestra el estado completado, la descripción, el responsable, las horas y el hito de ingeniería aprobado.
5. Entra en `06 · Integración SCADA y señales de control`: está vencida, tiene prioridad alta y explica el bloqueo y la acción requerida.
6. Abre `05 · Montaje de equipos AT/MT` y despliega sus subtareas. Muestra horas asignadas, responsables, etiquetas y el control de calidad adjunto.
7. Abre `07 · Pruebas de protecciones y control` y muestra que depende de la integración SCADA. Continúa la cadena hasta facturación y cierre.
8. Cambia a Gantt o Calendario para enseñar el programa completo y abre `♻️ Inspección semanal de seguridad` para mostrar su recurrencia.
9. Cambia a la vista de hitos: ingeniería está aprobada y montaje, energización y dossier muestran las próximas fechas.
10. Revisa las actualizaciones del proyecto: el historial pasa de 30% a 58% y luego a 68% con estado **En riesgo**.
11. Cierra en el chatter con la alerta del comité y explica cómo el responsable mantiene trazabilidad sin recurrir a planillas o correos separados.

## Lista de control antes de recibir al cliente

- Abrir el proyecto y dejar el tablero como favorito.
- Confirmar que las cinco columnas se ven completas en pantalla.
- Verificar que el usuario `project.user` puede abrir las tareas y adjuntos.
- Evitar cambiar datos durante la primera explicación; usar una subtarea para la interacción en vivo.
- No confirmar facturas, recepciones ni asientos: la demostración de Proyectos usa únicamente registros ficticios.

## Relación con el negocio

La demo representa un servicio compuesto por:

1. Levantamiento técnico.
2. Planificación de montaje.
3. Montaje de equipos de alta y media tensión.
4. Pruebas eléctricas y puesta en servicio.
5. Informe y cierre documental.

Este flujo se basa en las líneas públicas de construcción y montaje, pruebas eléctricas, y mantención e inspección técnica de GDG Ingeniería.
