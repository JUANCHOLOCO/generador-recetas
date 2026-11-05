# Glosario

Términos del negocio y del proyecto que aparecen en el código, los scripts y la documentación.
Los marcados con **(por confirmar)** son la mejor interpretación disponible; corregirlos si el área
de negocio indica otra cosa.

## Negocio y recetas

| Término | Significado |
|---|---|
| **RQ / Requerimiento** | Solicitud de cambio que origina una receta. Formato `TPFB-####` (ej. `TPFB-2753`). Da nombre a la carpeta raíz y aparece en los nombres de archivo y en las cabeceras |
| **Receta** | Paquete de carpetas y scripts SQL que el operador ejecuta para desplegar un cambio de catálogo. Es lo que genera la app |
| **Aplica / Rollback** | Script que hace el cambio / script que lo revierte. Toda receta trae los dos |
| **Lanzador (wrapper)** | `aplica-cambio.sql` y `rollback-cambio.sql`: fijan el esquema (`alter session set current_schema=…`) y llaman a los scripts de datos de `SQL/` y `ROLLBACK/` |
| **Ambiente** | `Dev`, `UAT` o `Prod`. Define el sufijo de la carpeta raíz (`TPFB-2753_Prod`) |
| **MOP** | Documento de cambio (Excel) que acompaña la receta y describe los pasos al operador. La app no lo genera (está en el backlog); el panel "Propiedades para el MOP" ayuda a llenarlo |
| **ACTIVATOR (ACTIVADOR)** | Base de datos donde viven planes (`PLANS`), paquetes (`SERVICES`) y sus reglas. La carpeta de la receta se llama `ACTIVADOR` |
| **SIEBEL** | Base de datos del CRM. La receta actualiza los productos con su POID |
| **PROMOTIONS** | Base de datos de promociones. La receta registra los POID de planes y paquetes (`IDENTIFY`) |
| **Conf** | Carpeta de la receta con archivos de configuración para los servidores de aplicación: el `Pool-RQ-….txt` y los `.properties` |
| **`.properties`** | Archivos de configuración de servicios (`InfranetService`, `PCRFService`, `PostSale`, `promotions`, `SiebelService`, `ussdGw`). Los valores empiezan con coma porque el operador los **agrega** al final de la línea existente en el servidor |
| **Infranet** | Nombre del sistema de facturación (Oracle BRM) al que apuntan los POID y `InfranetService.properties` **(por confirmar)** |
| **PCRF** | Sistema que controla las políticas de uso de datos de la línea. El *código perfil PCRF* identifica el perfil de navegación del plan |
| **ussdGw** | Pasarela USSD (menús `*####` del teléfono); su `.properties` lista los planes que la consultan **(por confirmar)** |

## Planes y paquetes

| Término | Significado |
|---|---|
| **Plan pospago** | Plan de línea móvil que se factura cada mes. Una fila del formulario de Creación de planes |
| **Familia Nintendo** | Nombre interno del grupo de planes pospago que crea el módulo (heredado de la macro `Receta Planes Nintendo.xlsm`) **(por confirmar el origen del nombre)** |
| **Tipo de facturación** | **Anticipada** (se cobra al inicio del periodo) o **Corriente** (se cobra al final; en `PLANS.BILLING_TYPE` es `'Vencida'`). Lo que cambia entre las dos está en `BillingStrategy` |
| **FC** | Sufijo ` FC` en los nombres de planes y paquetes Corriente (ej. `Pospago Conectados 5.1 FC`). Lo escribe el usuario; la app solo advierte si falta o sobra |
| **Id_Plan** | Identificador numérico del plan en ACTIVATOR (`PLANS.ID`) |
| **Part_num / PLCON** | Código del plan: `PLCON` + 4 dígitos (`PLCON0454`) |
| **Svall / SVALL** | Código de un paquete (servicio): `SVALL` + 4 dígitos (`SVALL2632`). Cada plan tiene un Svall de Datos y uno de SMS |
| **Paquete Datos / SMS** | Los dos servicios que acompañan a cada plan. Subtipo `DPI` (Datos) o `SMS` |
| **POID** | Identificador de un producto en el sistema de facturación (`0.0.0.1 /product <POID> 1`). Lo tienen el plan, el paquete de Datos y el de SMS |
| **Tarif group** | Grupo tarifario del plan. También es el **POID del plan** |
| **IDENTIFY** | Código numérico de PROMOTIONS por tipo de producto: PLAN = 21, SMS = 22, DATA = 23 |
| **5.3 / 5.3 OLDS** | Generación de planes "5.3". Los marcados "Es 5.3 = S" entran en la consulta `SQL.ADD.ON.IS.NINTENDO` de `SiebelService.properties` junto con la lista de planes 5.3 anteriores (*OLDS*, tabla `pospago_plan_53_old`) |
| **Matriz CPL_PLAN_PLAN** | Tabla de ACTIVATOR con los cambios de plan permitidos (de qué plan a qué plan se puede migrar). La receta agrega los planes nuevos cruzados con las listas Nintendo, Prepago, CONTROL y ATP |
| **Prepago / CONTROL / ATP** | Listas de planes de la matriz de cambios de plan (`pospago_cpl_plan_plan.lista`) **(por confirmar el significado de CONTROL y ATP)** |
| **ATP_CORP_PRECIOS_SERVICE** | Tabla de ACTIVATOR con el precio con y sin IVA de cada paquete. La actualiza el alza de paquetes |
| **Scoring** | Reglas de evaluación crediticia: los planes nuevos se agregan a `SCORING_PLAN` y `CPL_SCORING_PLAN` con los IDs de `pospago_scoring` |
| **Canal** | Canal de venta (`pospago_canal`) para el que se habilita el scoring del plan |
| **Pool** | Archivo `Pool-RQ-<RQ>.txt` de Conf con las cadenas (`LNALL…`, `SMALL…`, `PQCON…`) que acompañan a los planes nuevos |
| **Add-on** | Paquete adicional (`pospago_addon`) asociado a los planes nuevos |
| **Rol (Perfil_###)** | Perfil de usuario de SIEBEL que recibe permiso sobre los planes nuevos (`pospago_rol`) |
| **Alza de tarifas** | Cambio de precio de planes pospago o de paquetes existentes. Módulo con dos pestañas; no calcula precios: escribe los que ingresa el usuario |
| **Precio con / sin IVA** | En el alza de paquetes, `SERVICES.ITEM_PRICE` y `ITEM_PRICE_IVA` llevan el precio con IVA; `ATP_CORP_PRECIOS_SERVICE.ITEM_PRICE`, el precio sin IVA |
| **Prorrateo** | `ITEM_PRICE_PRORRATE`: valor que se cobra por los días de un mes incompleto. En el alza de pospago lo ingresa el usuario |

## Proyecto y código

| Término | Significado |
|---|---|
| **Parametrización** | Datos que no cambian entre recetas (scoring, canales, roles, campos estáticos…). Antes era la hoja "Reglas Aplicabilidad" del Excel; hoy son tablas SQLite editables en la pestaña *Parametrización* |
| **Seeds** | CSV con la parametrización inicial (`modules/<modulo>/seeds/`). Solo se cargan en tablas vacías |
| **`AMBAS`** | Valor de `tipo_facturacion` en la parametrización: la fila aplica a Corriente y a Anticipada |
| **Golden test** | Test que compara la receta generada byte a byte con un archivo aprobado (`tests/golden/…/esperado`) |
| **Equivalencia / corrección declarada** | Los golden también comparan, sentencia por sentencia, con los scripts originales del RQ de referencia. Las diferencias intencionales (errores de los originales) se declaran como funciones `Correccion` en el test |
| **RQ de referencia** | Receta real usada como verdad en los golden: TPFB-2753 (Creación de planes) y TPFB-1726 (Alza de tarifas) |
| **Módulo** | Tipo de receta (Creación de planes, Alza de tarifas). Implementa el contrato `Module` y se registra en `modules/__init__.py` |
| **`ModuleRegistry`** | Lista de módulos instalados; la ventana arma el menú lateral desde ella |
| **`AppContext`** | Dependencias que reciben los módulos: rutas, fábrica de sesiones, reloj, usuario y preferencias |
| **`RecipeBundle`** | Árbol de carpetas y archivos de una receta, en memoria, antes de escribirlo en disco |
| **Escritor** | Escribe el `RecipeBundle` en disco (cp1252, CRLF). Si la carpeta de primer nivel ya existe, lanza `RecetaExistenteError` y la vista pregunta si sobrescribir |
| **Caso de uso** | Clase de `application/` con un método `ejecutar` por acción de negocio (`GenerarReceta`, `GenerarAlzaPaquetes`…) |
| **Puerto** | Interfaz (`Protocol`) que el dominio o el presenter usan sin conocer la implementación (`Reloj`, `UsuarioActual`, `VistaFormulario`…) |
| **MVP** | Model-View-Presenter. La vista (Qt) solo muestra y avisa; el presenter (sin Qt) decide. Así la lógica de pantalla se prueba sin abrir ventanas |
| **cp1252 / CRLF** | Codificación Windows-1252 y fin de línea de Windows. Los scripts se escriben así para ser idénticos a los instaladores históricos |
| **`preferencias.json`** | Último autor y carpeta de salida, en la carpeta de la app (no en el registro de Windows, para que siga siendo portable) |
