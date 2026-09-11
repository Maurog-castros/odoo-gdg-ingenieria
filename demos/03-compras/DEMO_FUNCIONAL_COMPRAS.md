# Demo funcional integral de Compras

## Objetivo

Mostrar cómo GDG Ingeniería puede controlar el ciclo completo de abastecimiento de una obra: clasificar necesidades, comparar proveedores, solicitar precios, aprobar montos, emitir órdenes, recibir materiales y revisar desempeño.

La demostración usa datos ficticios vinculados por referencia al proyecto `Demo - Puesta en servicio Subestacion Energia Norte`.

## Historia que se contará

La obra está en montaje y necesita materiales eléctricos, ferretería, hormigón, EPP, equipos de prueba y servicios de maquinaria. Algunas compras recién comienzan; otras requieren aprobación; una recepción está atrasada y otra ya fue completada. El tablero permite decidir dónde actuar sin revisar planillas separadas.

## Datos preparados

### Categorías

- Materiales de obra.
- Material eléctrico AT/MT.
- Ferretería y montaje.
- Obras civiles.
- Equipos de prueba.
- EPP y seguridad.
- Servicios y arriendos.

### Proveedores

- Equipos Eléctricos.
- Ferretería Industrial.
- Hormigones Norte.
- Maquinaria y Transporte.
- Seguridad Industrial.

Cada proveedor tiene datos ficticios y una tarifa con plazo de entrega para los productos que suministra.

### Documentos de compra

| Referencia | Situación | Uso durante la demo |
| --- | --- | --- |
| `DEMO-RFQ-CABLES-101` | Solicitud nueva | Crear, revisar líneas, descuentos y fechas. |
| `DEMO-RFQ-EPP-102` | Solicitud enviada y vencida | Seguimiento al proveedor y actividad atrasada. |
| `DEMO-APR-HORMIGON-103` | Esperando aprobación | Separación entre comprador y responsable. |
| `DEMO-PO-MONTAJE-104` | Orden confirmada | Recepción pendiente con fecha futura. |
| `DEMO-PO-ATRASADA-105` | Orden confirmada | Recepción vencida que requiere gestión. |
| `DEMO-PO-RECIBIDA-106` | Servicio completado | Cantidad recibida sin movimiento físico de inventario. |
| `DEMO-PO-RECIBIDA-108` | Material recibido | Recepción física completa y a tiempo en Inventario. |
| `DEMO-RFQ-PRUEBAS-107` | Solicitud cancelada | Historial de una decisión de compra. |

## Preparación técnica

Consultar primero qué funciones están instaladas; esta operación no modifica Odoo:

```bash
python3 script/inspect_purchase_capabilities.py --env script/creacion-usuarios/.env
```

Simular y luego cargar la demostración:

```bash
python3 script/demo_compras_integral.py --env script/creacion-usuarios/.env --dry-run
python3 script/demo_compras_integral.py --env script/creacion-usuarios/.env
```

El script busca los registros por referencia antes de crearlos. Se puede ejecutar nuevamente sin duplicar categorías, proveedores, productos, tarifas ni documentos.

## Guion de presentación — 25 minutos

### 1. Panel de control — 3 minutos

1. Entrar a **Compras**.
2. Explicar los indicadores: solicitudes nuevas, enviadas, atrasadas, órdenes sin recibir y recepciones atrasadas.
3. Abrir primero el indicador atrasado para demostrar que cada tarjeta funciona como filtro operativo.

Mensaje para el cliente: “El comprador comienza el día viendo excepciones y prioridades, sin construir un informe manual”.

### 2. Categorías y catálogo — 4 minutos

1. Ir a **Productos > Productos** y agrupar por categoría.
2. Buscar `DEMO-CAB-CTRL`, `DEMO-HORM-H30` y `DEMO-ARR-GRUA`.
3. Comparar un material almacenable con un servicio de arriendo.
4. Abrir un producto y mostrar referencia interna, categoría, coste y descripción de compra.

Mensaje: “El catálogo distingue material eléctrico, obras civiles, seguridad, equipos y servicios”.

### 3. Proveedores y tarifas — 4 minutos

1. Abrir un producto y revisar la pestaña de compra.
2. Mostrar proveedor, precio, cantidad mínima y plazo.
3. Explicar que Odoo propone información del proveedor al preparar una solicitud.
4. Buscar el mismo proveedor desde **Pedidos > Proveedores** y revisar sus compras históricas.

### 4. Solicitud y negociación — 4 minutos

1. Abrir `DEMO-RFQ-CABLES-101`.
2. Revisar proveedor, referencia de oferta, origen del proyecto y fecha prevista.
3. Mostrar dos líneas de categorías diferentes, cantidades, precios y descuentos.
4. Abrir `DEMO-RFQ-EPP-102` para mostrar una solicitud enviada cuya respuesta está vencida.
5. Revisar la actividad “Comparar oferta y solicitar vigencia”.

### 5. Aprobación de compra — 3 minutos

1. Abrir `DEMO-APR-HORMIGON-103`.
2. Explicar por qué el monto requiere revisión.
3. Mostrar que el comprador prepara el documento y el responsable decide su aprobación.
4. No aprobar durante la primera presentación; conservar el estado para que el cliente vea la bandeja pendiente.

### 6. Orden y recepción — 5 minutos

1. Abrir `DEMO-PO-MONTAJE-104` y usar el botón inteligente de recepción.
2. Mostrar cantidades solicitadas, recibidas y pendientes.
3. Abrir `DEMO-PO-ATRASADA-105` y señalar la fecha comprometida vencida y su actividad de seguimiento.
4. Abrir `DEMO-PO-RECIBIDA-108` y recorrer la recepción física completada.
5. Volver a la orden para enseñar la trazabilidad entre proveedor, documento y recepción.

### 7. Reportes y cierre — 2 minutos

1. Ir a **Reportes > Compras**.
2. Agrupar por proveedor y categoría de producto.
3. Comparar importe comprado, cantidad y plazo de entrega.
4. Cerrar regresando al panel para comprobar que las excepciones siguen visibles.

## Funcionalidades que deben quedar visibles

- Categorías jerárquicas de producto.
- Productos almacenables y servicios.
- Varios proveedores y precios de proveedor.
- Referencias internas y plazos de abastecimiento.
- Solicitud nueva, enviada y vencida.
- Flujo de aprobación.
- Orden confirmada y documentos cancelados.
- Recepción pendiente, atrasada y completada.
- Actividades del comprador.
- Origen relacionado con el proyecto.
- Informes agrupados por proveedor y categoría.

La distribución analítica debe mostrarse solamente si la base tiene un plan y cuenta analítica configurados para el proyecto. Los acuerdos de compra no aparecen en esta instancia porque el módulo correspondiente no está instalado.

## Usuarios sugeridos

- `purchase.user`: crea solicitudes, compara ofertas y sigue entregas.
- `purchase.manager`: revisa y aprueba compras de mayor importe.
- `inventory.user`: procesa y consulta recepciones.

## Lista de control antes de la reunión

- Verificar que el panel muestre documentos en varios estados.
- Abrir previamente las referencias 101, 103, 105 y 106 en pestañas separadas.
- Confirmar que los productos se agrupen por las categorías `DEMO`.
- Comprobar que el usuario funcional pueda abrir proveedores, productos y recepciones.
- Mantener pendiente la compra 103 y atrasada la recepción 105 para conservar el relato.
- Usar únicamente los documentos con prefijo `DEMO-`.
- No validar nuevas recepciones ni generar facturas durante la demo sin revisar antes el documento.

## Resultado esperado

La persona funcional puede mostrar el ciclo completo desde una necesidad de obra hasta la recepción y el reporte, mientras el cliente distingue rápidamente compras nuevas, decisiones pendientes y atrasos que necesitan atención.
