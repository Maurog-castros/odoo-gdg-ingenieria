# Demo funcional de Contabilidad y Facturación

## Objetivo

Mostrar el ciclo financiero con factura en borrador, cuenta por cobrar vigente, documento vencido, factura pagada y factura de proveedor.

## Datos preparados

| Referencia | Tipo | Contraparte | Estado funcional | Importe antes de impuestos |
|---|---|---|---|---:|
| `DEMO-FAC-BORRADOR-301` | Factura de cliente | Cliente Demo Minería Central | Borrador | $3.500.000 |
| `DEMO-FAC-PENDIENTE-302` | Factura de cliente | Cliente Demo Energía Norte | Publicada, pendiente | $6.000.000 |
| `DEMO-FAC-VENCIDA-303` | Factura de cliente | Cliente Demo Transmisión Sur | Publicada, vencida | $4.000.000 |
| `DEMO-FAC-PAGADA-304` | Factura de cliente | Cliente Demo Industria Andina | Publicada y pagada | $2.500.000 |
| `DEMO-FCP-BORRADOR-305` | Factura de proveedor | Proveedor Demo Maquinaria y Transporte | Borrador | $1.200.000 |

Los impuestos y totales finales dependen de la configuración fiscal vigente en la base.

## Guion sugerido, 15 minutos

1. Abra **Facturación/Contabilidad > Clientes > Facturas** y busque `DEMO-FAC` en la referencia.
2. Entre a la factura borrador. Muestre cliente, fechas, vencimiento, producto, asiento preliminar y total; explique el control antes de publicar.
3. Compare las facturas pendiente y vencida. Muestre fecha de vencimiento, importe residual y estado de pago.
4. Abra `DEMO-FAC-PAGADA-304` y enseñe la banda **Pagado**, el pago relacionado y la conciliación automática generada por el registro de pago.
5. Abra **Proveedores > Facturas** y busque `DEMO-FCP-BORRADOR-305`. Explique revisión, cuenta de gasto y posterior publicación/pago.
6. Termine en el tablero contable o informe de cuentas por cobrar para mostrar cómo los documentos alimentan indicadores y reportes.

## Mensaje para el cliente

Odoo separa claramente preparación, publicación, vencimiento y pago. La misma información queda disponible para cobranza, bancos, impuestos, libro mayor y análisis sin planillas paralelas.

## Resultado esperado

- Se observan cuatro situaciones distintas de factura de cliente.
- La factura pagada tiene pago registrado y saldo residual cero.
- La factura de proveedor permanece en borrador para demostrar revisión y contabilización.
- La factura vencida aparece como deuda pendiente según su fecha de vencimiento.
