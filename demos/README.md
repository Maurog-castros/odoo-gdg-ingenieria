# Demos funcionales

Esta carpeta organiza los casos de prueba de GDG Ingeniería por área de trabajo.

## Estructura de cada demo

Cada caso puede tener esta forma:

```text
area/
└── nombre-del-demo/
    ├── README.md       # explicación para el usuario funcional
    ├── data/            # archivos CSV, XLSX o JSON de prueba
    ├── docs/            # pasos, reglas y resultados esperados
    └── scripts/         # automatizaciones específicas del caso
```

## Áreas

- `01-crm/`: clientes potenciales, oportunidades y actividades.
- `02-ventas/`: cotizaciones, pedidos y seguimiento comercial.
- `03-compras/`: proveedores, productos nuevos y órdenes de compra.
- `04-inventario/`: recepciones, movimientos y existencias.
- `05-contabilidad-facturacion/`: facturas, pagos y registros contables.
- `06-proyectos/`: proyectos, tareas, responsables y avances.
- `07-integracion/`: casos que conectan dos o más módulos.

Los scripts generales siguen en `script/`. Las guías generales siguen en `docs/`.
Las credenciales y archivos `.env` no deben guardarse en esta carpeta ni en Git.