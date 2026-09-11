# Demo funcional de Inventario

## Objetivo

Mostrar recepción, disponibilidad, transferencias internas y control de materiales entre bodega, obra y calibración.

## Datos preparados

Producto físico: `DEMO-REP-FUSIBLE`, fusible de control industrial 10 A.

Ubicaciones creadas:

- `DEMO · Obra Proyecto 3`
- `DEMO · Equipos en calibración`

| Referencia de origen | Operación | Cantidad | Estado esperado |
|---|---|---:|---|
| `DEMO-STOCK-INICIAL-401` | Recepción de proveedor a bodega | 30 | Hecho |
| `DEMO-TRANSFERENCIA-OBRA-402` | Bodega a obra | 12 | Hecho |
| `DEMO-REPOSICION-OBRA-403` | Reposición desde bodega a obra | 8 | Preparado/listo |
| `DEMO-RETORNO-CALIBRACION-404` | Obra a calibración | 2 | Preparado/listo |

## Guion sugerido, 10 minutos

1. Abra **Inventario > Operaciones > Transferencias** y filtre por origen `DEMO-`.
2. Abra la recepción inicial y muestre origen, destino, producto, demanda, cantidad procesada y estado hecho.
3. Abra la transferencia a obra. Explique la trazabilidad de 12 unidades desde existencias centrales hacia una ubicación operativa.
4. Abra la reposición pendiente y muestre disponibilidad/reserva. Valídela durante la presentación sólo si desea demostrar el cambio de stock en vivo.
5. Abra el retorno a calibración para mostrar que las ubicaciones pueden representar procesos y custodias, además de bodegas físicas.
6. Entre al producto y revise **A mano**, **Pronosticado** y **Movimientos** para explicar existencias actuales y futuras.

## Mensaje para el cliente

Cada movimiento indica qué material salió, desde dónde, hacia qué frente de trabajo y en qué estado se encuentra. Las transferencias pendientes permiten planificar; las validadas dejan trazabilidad del movimiento real.

## Resultado esperado

- La bodega recibió 30 unidades y transfirió 12 a obra.
- Hay operaciones listas para demostrar reserva y validación.
- Las cantidades a mano y pronosticadas cambian según la ubicación seleccionada.
