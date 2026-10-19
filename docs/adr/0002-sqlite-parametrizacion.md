# ADR 0002: SQLite para las tablas de parametrización

- Estado: Aceptado
- Fecha: 2026-10-19

## Contexto

La hoja "Reglas Aplicabilidad" contiene listas que cambian cuando salen planes nuevos (IDs de
cambio de plan, scoring, roles, add-ons, campos estáticos…). Un solo usuario las mantiene en su
PC. No se quiere cargar Excel en tiempo de uso: la información debe vivir en tablas propias.

## Decisión

- **SQLite** en un archivo `recetas.db` junto al ejecutable.
- **SQLAlchemy 2** como ORM y **Alembic** para versionar el esquema.
- Datos iniciales cargados desde `data/seeds/` (extraídos una vez de los Excel de Anticipados y
  Corriente) en la primera ejecución.
- Columna `tipo_facturacion` (`CORRIENTE`, `ANTICIPADA`, `AMBAS`) en todas las tablas de
  parametrización.

## Alternativas consideradas

- **Leer el Excel en cada ejecución:** acopla la app al formato del libro; descartado por el usuario.
- **JSON/CSV editables:** sin integridad referencial ni restricciones de unicidad.
- **PostgreSQL/SQL Server:** requieren servidor; innecesario para un solo usuario.

## Consecuencias

- Archivo único, fácil de respaldar (copia automática al iniciar).
- Las migraciones permiten evolucionar el esquema sin perder datos del usuario.
- Para uso multiusuario futuro habría que revisar esta decisión.
