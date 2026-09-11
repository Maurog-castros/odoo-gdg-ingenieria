# Demo: crear un item nuevo desde Compras

## Objetivo

Esta demo enseña qué hacer cuando un proveedor ofrece un producto que todavía no existe en Odoo:

1. Crear el producto la primera vez que se necesita.
2. Agregarlo a la orden de compra.
3. Guardar la orden.
4. Encontrar el mismo producto en la siguiente orden, sin volver a crearlo.

El ejemplo usa un producto ficticio llamado **Demo - Kit de pruebas de aislamiento 23 kV**. No representa un producto real ni modifica productos existentes.

## Antes de comenzar

- Debes tener acceso al módulo **Compras**.
- Debes tener un proveedor seleccionado. En la demo automática se usa `Proveedor Demo Equipos Electricos`.
- Debes tener permisos para crear productos y órdenes de compra.
- El archivo `script/creacion-usuarios/.env` debe existir y mantenerse fuera de Git.

## Opción A: hacerlo desde la pantalla de Odoo

### 1. Crear una nueva orden de compra

1. Entra a **Compras**.
2. Abre **Órdenes de compra**.
3. Pulsa **Nuevo**.
4. Selecciona el proveedor.
5. En la sección **Productos**, pulsa **Agregar un producto**.

### 2. Crear el producto que no existe

1. En la línea de producto, escribe `Demo - Kit de pruebas de aislamiento 23 kV`.
2. Si Odoo no encuentra coincidencias, selecciona **Crear** o **Crear y editar**.
3. Completa los campos básicos:
   - **Nombre del producto:** `Demo - Kit de pruebas de aislamiento 23 kV`
   - **Tipo de producto:** `Consumible` o `Almacenable`, según la política de inventario de la empresa.
   - **Se puede comprar:** activado.
   - **Referencia interna:** `DEMO-KIT-23KV`.
   - **Precio de coste:** `650000`.
4. Pulsa **Guardar y cerrar**.

El producto queda registrado en **Compras > Productos > Productos**. La próxima vez aparecerá en el buscador.

### 3. Completar y confirmar la orden

1. Verifica la cantidad y el precio acordado con el proveedor.
2. Pulsa **Guardar**.
3. Revisa la orden y pulsa **Confirmar orden** cuando corresponda.
4. No pulses **Recibir productos** en una demo si no quieres generar movimientos de inventario.

### 4. Usar el producto en una segunda orden

1. Crea otra orden desde **Compras > Órdenes de compra > Nuevo**.
2. Selecciona el proveedor.
3. En la línea de producto, busca `DEMO-KIT-23KV` o el nombre completo.
4. Selecciona el producto existente.
5. Completa cantidad, precio y confirma la orden según el flujo normal.

En este paso no se debe crear otro producto. Se reutiliza el registro original.

## Opción B: ejecutar la demo automática

Desde la carpeta raíz del proyecto, primero revisa la simulación:

```bash
python3 script/demo_nuevo_item_compra.py --env script/creacion-usuarios/.env --dry-run
```

Si la simulación es correcta, crea el producto y dos órdenes de compra:

```bash
python3 script/demo_nuevo_item_compra.py --env script/creacion-usuarios/.env
```

El script crea:

- Producto: `DEMO-KIT-23KV`
- Primera orden: `DEMO-OC-NUEVO-ITEM-001`
- Segunda orden: `DEMO-OC-NUEVO-ITEM-002`

Si vuelves a ejecutarlo, mostrará `EXISTE` y no duplicará el producto ni las órdenes.

## Comprobación final

En Odoo, busca `DEMO-KIT-23KV` en **Compras > Productos > Productos** y confirma que:

- El producto existe una sola vez.
- Está marcado como comprable.
- Aparece en las dos órdenes demo.
- La referencia interna permite encontrarlo rápidamente.

## Importante

Los datos de esta guía son de prueba. Revisa proveedor, precio, impuestos, unidad de medida y tipo de producto antes de usar el mismo procedimiento en producción. No guardes contraseñas en este documento ni subas `.env` al repositorio.