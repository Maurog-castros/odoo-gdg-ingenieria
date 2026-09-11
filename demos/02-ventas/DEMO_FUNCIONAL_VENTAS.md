# Demo funcional de Ventas

## Objetivo

Mostrar estados comerciales, vigencias, descuentos, referencias del cliente y la conversión desde oportunidad hasta pedido confirmado.

## Datos preparados

| Documento | Estado | Cliente | Escenario |
|---|---|---|---|
| `DEMO-COT-DIAGNOSTICO-201` | Cotización | Cliente Demo Minería Central | Oferta nueva, vigente por 14 días |
| `DEMO-COT-MANTENCION-202` | Cotización enviada | Cliente Demo Transmisión Sur | Oferta vencida con dos servicios y 5 % de descuento |
| `DEMO-PED-OBRA-203` | Pedido de venta | Cliente Demo Energía Norte | Adjudicación confirmada por $18.500.000 antes de impuestos |
| `DEMO-COT-CANCELADA-204` | Cancelada | Cliente Demo Minería Central | Negocio no adjudicado |

Los productos de demo son diagnóstico en terreno, montaje electromecánico, pruebas y puesta en servicio, y fusibles de control.

## Guion sugerido, 10 minutos

1. Abra **Ventas > Pedidos > Cotizaciones** y busque `DEMO-`.
2. Compare la cotización nueva con la enviada y vencida. Muestre fecha, vencimiento, referencia, comercial, líneas, descuento, subtotal y total.
3. Abra `DEMO-PED-OBRA-203`. Explique que proviene de la oportunidad ganada **Puesta en servicio Subestación Norte**.
4. Muestre las dos líneas del pedido: montaje por $12.500.000 y puesta en servicio por $6.000.000.
5. Use la vista previa o impresión de cotización para enseñar el documento que recibe el cliente.
6. Compare con `DEMO-COT-CANCELADA-204` para explicar que Odoo conserva la historia aunque el proceso no se adjudique.

## Mensaje para el cliente

La cotización reúne alcance, precio, descuento, vigencia y responsable. Cuando el cliente acepta, se confirma el pedido y se habilita la continuidad operativa y financiera del servicio.

## Resultado esperado

- Hay documentos en borrador, enviados, confirmados y cancelados.
- Se puede seguir el vínculo entre oportunidad y pedido.
- El catálogo combina servicios y un repuesto físico para conectar Ventas con Inventario.
