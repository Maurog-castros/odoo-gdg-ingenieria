# Demo: puesta en servicio de una subestación

## Objetivo

Practicar el uso del módulo **Proyectos** para planificar un servicio típico de GDG Ingeniería: montaje y pruebas eléctricas para poner en servicio una subestación.

El caso usa datos ficticios inspirados en los servicios públicos de la empresa. No representa un contrato real.

## Resultado esperado

Al terminar debe existir:

- Proyecto: `Demo - Puesta en servicio Subestacion Energia Norte`.
- Cliente: `Cliente Demo Energia Norte`.
- Cinco tareas ordenadas por etapa.
- Una descripción breve en cada tarea.

## Pasos para un usuario básico

1. Entra a **Proyectos**.
2. Pulsa **Nuevo**.
3. Escribe `Demo - Puesta en servicio Subestacion Energia Norte`.
4. Selecciona `Cliente Demo Energia Norte` si el campo cliente está disponible.
5. Guarda el proyecto.
6. Crea estas tareas en el orden indicado:
   - `01 - Levantamiento tecnico`
   - `02 - Planificacion de montaje`
   - `03 - Montaje de equipos AT/MT`
   - `04 - Pruebas electricas PES`
   - `05 - Informe y cierre`
7. En cada tarea escribe qué se debe revisar y asigna un responsable.
8. Mueve cada tarea por las etapas del proyecto a medida que avanza.
9. Al finalizar, adjunta protocolos, evidencias e informe de cierre.

## Ejecutar automáticamente

Primero revisa qué se crearía:

```bash
python3 script/demo_proyecto_gdg.py --env script/creacion-usuarios/.env --dry-run
```

Luego carga el proyecto y sus tareas:

```bash
python3 script/demo_proyecto_gdg.py --env script/creacion-usuarios/.env
```

El script busca por nombre antes de crear. Si se ejecuta nuevamente, informa `EXISTE` y no duplica el proyecto ni las tareas.

## Relación con el negocio

La demo representa un servicio compuesto por:

1. Levantamiento técnico.
2. Planificación de montaje.
3. Montaje de equipos de alta y media tensión.
4. Pruebas eléctricas y puesta en servicio.
5. Informe y cierre documental.

Este flujo se basa en las líneas públicas de construcción y montaje, pruebas eléctricas, y mantención e inspección técnica de GDG Ingeniería.