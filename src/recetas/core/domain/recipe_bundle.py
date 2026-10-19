"""Receta armada en memoria: archivos con ruta relativa, contenido y codificación."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath

from recetas.core.domain.errors import (
    DuplicateRecipeFileError,
    InvalidRecipeContentError,
    InvalidRecipePathError,
)

WINDOWS_ENCODING = "cp1252"
CRLF = "\r\n"


@dataclass(frozen=True, slots=True)
class RecipeFile:
    path: PurePosixPath
    content: str
    encoding: str = WINDOWS_ENCODING
    newline: str = CRLF

    def to_bytes(self) -> bytes:
        """Contenido final: fines de línea unificados y codificado."""
        normalizado = self.content.replace("\r\n", "\n")
        return normalizado.replace("\n", self.newline).encode(self.encoding)


class RecipeBundle:
    def __init__(self, root: str) -> None:
        self._root = _validar_ruta(root)
        self._files: dict[PurePosixPath, RecipeFile] = {}

    @property
    def root(self) -> PurePosixPath:
        return self._root

    def add(
        self,
        path: str,
        content: str,
        *,
        encoding: str = WINDOWS_ENCODING,
        newline: str = CRLF,
    ) -> RecipeBundle:
        ruta = _validar_ruta(path)
        if ruta in self._files:
            raise DuplicateRecipeFileError(str(ruta))

        archivo = RecipeFile(ruta, content, encoding, newline)
        try:
            archivo.to_bytes()
        except UnicodeEncodeError as exc:
            invalidos = exc.object[exc.start : exc.end]
            raise InvalidRecipeContentError(str(ruta), encoding, invalidos) from exc

        self._files[ruta] = archivo
        return self

    def get(self, path: str) -> RecipeFile:
        return self._files[PurePosixPath(path)]

    @property
    def files(self) -> tuple[RecipeFile, ...]:
        return tuple(sorted(self._files.values(), key=lambda f: f.path))

    def __len__(self) -> int:
        return len(self._files)

    def __contains__(self, path: object) -> bool:
        return isinstance(path, str) and PurePosixPath(path) in self._files


def _validar_ruta(valor: str) -> PurePosixPath:
    if not valor.strip() or "\\" in valor or ":" in valor:
        raise InvalidRecipePathError(valor)
    ruta = PurePosixPath(valor)
    if ruta.is_absolute() or ".." in ruta.parts:
        raise InvalidRecipePathError(valor)
    return ruta
