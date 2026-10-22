"""Escritura atómica de una receta en disco (adaptador de BundleWriter)."""

import shutil
import uuid
from pathlib import Path

from recetas.core.domain.errors import RecetaExistenteError
from recetas.core.domain.recipe_bundle import RecipeBundle


class EscritorDeRecetas:
    def escribir(self, bundle: RecipeBundle, carpeta: Path, *, sobrescribir: bool = False) -> Path:
        if len(bundle) == 0:
            raise ValueError("La receta no tiene archivos.")

        raiz = carpeta.joinpath(*bundle.root.parts)
        secciones = sorted({archivo.path.parts[0] for archivo in bundle.files})
        ocupadas = [raiz / s for s in secciones if (raiz / s).exists()]
        if ocupadas and not sobrescribir:
            raise RecetaExistenteError([str(r) for r in ocupadas])

        temporal = raiz / f".tmp-{uuid.uuid4().hex}"
        try:
            for archivo in bundle.files:
                ruta = temporal.joinpath(*archivo.path.parts)
                ruta.parent.mkdir(parents=True, exist_ok=True)
                ruta.write_bytes(archivo.to_bytes())
            for seccion in secciones:
                destino = raiz / seccion
                _borrar(destino)
                (temporal / seccion).rename(destino)
        finally:
            shutil.rmtree(temporal, ignore_errors=True)
        return raiz


def _borrar(ruta: Path) -> None:
    if ruta.is_dir():
        shutil.rmtree(ruta)
    elif ruta.exists():
        ruta.unlink()
