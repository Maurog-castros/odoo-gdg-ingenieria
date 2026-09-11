# Demo: ciclo completo de una obra

Este caso presenta el proyecto `3` de Odoo desde la cotización hasta la entrega final.

## Etapas

1. Cotización.
2. Diagnóstico en terreno.
3. Ejecución de obra.
4. Cierre / entrega de obra.

Cada etapa contiene cuatro tareas con objetivo, actividades, resultado o entregable, responsable, fechas, horas, etiquetas e hito asociado.

## Preparación

```bash
python3 script/demo_proyecto_ciclo_obra.py --env script/creacion-usuarios/.env --project-id 3 --dry-run
python3 script/demo_proyecto_ciclo_obra.py --env script/creacion-usuarios/.env --project-id 3
```

El script es idempotente y busca cada tarea por nombre y proyecto antes de crearla.

## Recorrido funcional

1. Abrir el proyecto y presentar las cuatro columnas como el ciclo real de la obra.
2. En **Cotización**, abrir la oferta técnica y enseñar sus dependencias con alcance, APU y precios de proveedores.
3. Mostrar que Cotización y Diagnóstico están terminados y sus hitos fueron alcanzados.
4. En **Diagnóstico en terreno**, abrir el informe final y recorrer hallazgos, criticidad y plan aprobado.
5. En **Ejecución de obra**, mostrar dos tareas simultáneas y el control de calidad esperando sus dependencias.
6. Cambiar a Gantt para visualizar solapamientos, duración y camino hasta la entrega.
7. En **Cierre / entrega**, recorrer pruebas SAT, dossier, capacitación, aceptación y facturación final.
8. Cerrar con los cuatro hitos y explicar cómo el jefe de proyecto distingue avance de fase y estado de tarea.
