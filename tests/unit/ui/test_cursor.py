import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from recetas.ui.widgets.cursor import cursor_de_espera

pytestmark = pytest.mark.ui


def test_el_cursor_de_espera_se_quita_aunque_haya_un_error(qapp: QApplication) -> None:
    formas = []

    with pytest.raises(ValueError), cursor_de_espera():
        cursor = QApplication.overrideCursor()
        formas.append(cursor.shape() if cursor else None)
        raise ValueError("falla")

    assert formas == [Qt.CursorShape.WaitCursor]
    assert QApplication.overrideCursor() is None
