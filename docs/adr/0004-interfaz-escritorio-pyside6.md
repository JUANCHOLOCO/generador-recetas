# ADR 0004: Interfaz de escritorio con PySide6 y patrón MVP

- Estado: Aceptado
- Fecha: 2026-10-19

## Contexto

El usuario prefiere una ventana de escritorio. El formulario principal es una tabla de N planes
(similar a Excel, con copiar/pegar) y las pantallas de mantenimiento editan tablas de
parametrización.

## Decisión

- **PySide6** (binding oficial de Qt 6, licencia LGPL).
- Tablas con `QTableView` + modelos propios (`QAbstractTableModel`) para editar y pegar filas.
- Patrón **MVP**: la vista solo pinta y emite señales; el *presenter* contiene la lógica de la
  pantalla y llama a los casos de uso. Los presenters se prueban sin Qt.

## Alternativas consideradas

- **Tkinter:** viene con Python, pero sus tablas editables son limitadas y el aspecto es anticuado.
- **Web local (FastAPI + HTMX) o pywebview:** propuesta inicial; descartada por preferencia de
  ventana de escritorio y para evitar un servidor local.
- **Electron:** otro lenguaje (JavaScript) y ejecutable mucho más pesado.

## Consecuencias

- Empaquetado con PyInstaller incluye Qt (~100 MB).
- Se usará `pytest-qt` para las pocas pruebas que requieren widgets reales.
