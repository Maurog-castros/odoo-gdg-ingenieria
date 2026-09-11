# odoo-gdg-ingenieria

Proyecto Odoo de GDG Ingenieria.

## Crear usuarios funcionales

El script `script/creacion-usuarios/create_users.py` crea diez usuarios de prueba, uno por cada perfil funcional. Sirven para validar permisos y flujos de CRM, ventas, compras, inventario, facturacion, contabilidad y proyectos.

| Login | Perfil |
| --- | --- |
| `crm.user` | CRM |
| `sales.user` | Ventas |
| `sales.manager` | Responsable de ventas |
| `purchase.user` | Compras |
| `purchase.manager` | Responsable de compras |
| `inventory.user` | Inventario |
| `inventory.manager` | Responsable de inventario |
| `invoicing.user` | Facturacion |
| `accounting.user` | Contabilidad |
| `project.user` | Proyectos |

### Preparacion

1. Copia `script/creacion-usuarios/.env` si necesitas crear otro entorno.
2. Mantén en `.env` `URLODOO`, `ADMIN-USER`, `PASS` y añade `ODOO_DB` con el nombre de la base de datos.
3. Añade `USER_PASSWORD` con una contraseña temporal para los diez usuarios. No la publiques ni la reutilices en produccion.

Ejemplo:

```dotenv
ODOO_DB=nombre-de-la-base
USER_PASSWORD=una-clave-temporal-segura
```

### Ejecutar

Desde la carpeta del proyecto:

```bash
python3 script/creacion-usuarios/create_users.py --env script/creacion-usuarios/.env --dry-run
python3 script/creacion-usuarios/create_users.py --env script/creacion-usuarios/.env
```

La primera orden solo comprueba la conexion, los grupos y los usuarios existentes. La segunda crea los que no existan. El script es idempotente: volver a ejecutarlo no duplica usuarios con el mismo login.

> Usa estos usuarios para pruebas funcionales. Cambia sus contraseñas al entrar y no ejecutes el script contra produccion sin revisar antes los permisos.

## Cargar datos de prueba

El script `script/seed_demo_data.py` usa como referencia la información pública de [GDG Ingeniería](https://www.gdging.cl/): construcción y montaje, pruebas eléctricas, y mantención e inspección técnica para proyectos de energía y minería.

Los registros son ficticios y están marcados como demo. Crea contactos, servicios, oportunidades, una cotización, una solicitud de compra y un proyecto con tareas. No publica facturas ni valida documentos contables.

Primero revisa la simulación:

```bash
python3 script/seed_demo_data.py --env script/creacion-usuarios/.env --dry-run
```

Cuando el resultado sea correcto, carga los datos:

```bash
python3 script/seed_demo_data.py --env script/creacion-usuarios/.env
```

El script evita duplicar contactos, productos, oportunidades y documentos con los nombres demo. Haz una copia de seguridad y revisa el entorno antes de usarlo en una base compartida.