# Perfil de GDG Ingeniería

Ficha de referencia para diseñar demos funcionales de Odoo. Los datos se basan en la información pública de [gdging.cl](https://www.gdging.cl/). Los nombres de clientes y cifras de los demos deben ser ficticios, aunque el proceso esté inspirado en la actividad publicada.

## Identidad

- **Empresa:** GDG Ingeniería.
- **Grupo:** forma parte del Grupo OD Ingeniería junto con OD Ingeniería.
- **Origen del grupo:** OD Ingeniería declara experiencia desde 1976 en montaje de transformadores de alta tensión.
- **Rol de GDG:** brazo industrial y minero orientado al montaje, pruebas y mantención de equipos eléctricos de media y alta tensión.
- **Cobertura:** servicios a nivel nacional en Chile.
- **Ubicación publicada:** Av. Cerro El Plomo 5420, oficina 402, Las Condes, Santiago.

## Sectores y tipos de proyecto

- Generación de energía.
- Transmisión de energía.
- Distribución de energía.
- Industria minera.
- Subestaciones y líneas eléctricas.

## Servicios publicados

### Construcción y montaje

- Montaje de transformadores de poder, interruptores, desconectadores, equipos de medida, pararrayos, reactores y GIS.
- Construcción de fundaciones y montaje de estructuras de líneas.
- Montaje de barras aéreas y tendido de cables de alta, media y baja tensión.
- Tendido de cables de control.
- Proceso de vacío en cuba.
- Tratamiento y desgasificado de aceite de transformadores.

### Pruebas eléctricas

- Pruebas de puesta en servicio de transformadores, reactores, interruptores, switchgear, baterías, cables y equipos asociados.
- Ajuste, calibración y análisis de sistemas de control y protecciones.
- Verificación y ajuste de relés y medidas.
- Puesta en servicio de sistemas SCADA, PLC e instrumentación industrial.
- Puesta en servicio de subestaciones.
- Pruebas y certificación de fibra óptica.

### Mantención e inspección técnica

- Mantenimiento preventivo y correctivo de equipos de alta, media y baja tensión.
- Planes y pautas de mantenimiento.
- Muestreo y pruebas físico-químicas y cromatográficas de aceites.
- Inspección y recepción de equipos en fábrica y puerto.
- Inspección de montaje de equipos eléctricos.

## Procesos que conviene demostrar en Odoo

1. **CRM:** oportunidad de una subestación, línea o faena minera.
2. **Ventas:** cotización de montaje, pruebas o mantención.
3. **Compras:** adquisición de un equipo o consumible que no existe en el catálogo.
4. **Inventario:** recepción, ubicación y trazabilidad de equipos y materiales.
5. **Proyectos:** planificación, responsables, tareas, avances y cierre documental.
6. **Contabilidad y facturación:** factura de cliente, factura de proveedor y control de pagos.

## Reglas para datos de prueba

- Usar nombres con prefijo `Demo -` o código `DEMO-`.
- Usar contactos ficticios y correos `example.com`.
- No copiar credenciales, datos personales ni información privada publicada.
- No usar nombres de clientes reales como si fueran registros de prueba.
- Mantener los scripts idempotentes: ejecutarlos otra vez no debe duplicar registros.
- Ejecutar primero el modo `--dry-run` cuando el script lo soporte.

## Fuente

Información pública consultada en https://www.gdging.cl/ el 11 de septiembre de 2026.