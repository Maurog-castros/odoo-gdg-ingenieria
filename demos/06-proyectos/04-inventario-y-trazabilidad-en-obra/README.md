# Demo: inventario y trazabilidad en obra

## Objetivo

Controlar equipos, materiales y elementos de protección desde la bodega central hasta una obra, incluyendo su retorno temporal.

## Caso de negocio

La bodega central mantiene equipos de prueba, transformadores y EPP. Los materiales de consumo pueden quedar directamente en cada obra.

## Pasos

1. En **Inventario**, crea o revisa las ubicaciones `Bodega central` y `Obra Energia Norte`.
2. Registra el equipo o material con referencia interna.
3. Realiza una transferencia interna desde la bodega a la obra.
4. Relaciona el movimiento con el proyecto si la configuración lo permite.
5. Consulta la existencia por ubicación.
6. Para equipos temporales, registra el retorno a la bodega al terminar la actividad.

## Resultado esperado

El equipo no se pierde ni se convierte automáticamente en gasto: se conoce dónde está y quién lo utiliza.

## Validación

- Existencia correcta en origen y destino.
- Fecha y responsable del movimiento.
- Trazabilidad del equipo.
- Retorno registrado para activos temporales.

Este flujo refleja la necesidad de separar bodega central, materiales de obra y equipos que salen temporalmente.