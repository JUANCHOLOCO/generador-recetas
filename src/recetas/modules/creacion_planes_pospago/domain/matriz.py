"""Regla de la matriz de cambios de plan (ACTIVATOR.CPL_PLAN_PLAN).

Por cada plan nuevo N y cada ID X de la parametrización (los IDs del formulario se tratan
siempre como planes nuevos, aunque ya estén registrados):

- PREPAGO:  (N, X) y (X, N)
- NINTENDO: (X, N) y (N, X); para los demás planes del formulario solo (X, N), porque
            el par inverso se genera en el bloque de X
- ATP, CONTROL: solo (X, N)
"""

from collections.abc import Sequence
from dataclasses import dataclass

from recetas.modules.creacion_planes_pospago.domain.parametrizacion import Parametrizacion
from recetas.modules.creacion_planes_pospago.domain.tipos import ListaCambioPlan

Par = tuple[str, str]


@dataclass(frozen=True, slots=True)
class SeccionMatriz:
    lista: ListaCambioPlan
    pares: tuple[Par, ...]


def matriz_cambio_plan(
    id_plan: str, ids_nuevos: Sequence[str], parametrizacion: Parametrizacion
) -> tuple[SeccionMatriz, ...]:
    nuevos = set(ids_nuevos)
    secciones = []
    for lista in ListaCambioPlan:
        existentes = [x for x in parametrizacion.ids_de_lista(lista) if x not in nuevos]
        pares: list[Par] = []
        match lista:
            case ListaCambioPlan.PREPAGO:
                for x in existentes:
                    pares += [(id_plan, x), (x, id_plan)]
            case ListaCambioPlan.NINTENDO:
                for x in existentes:
                    pares += [(x, id_plan), (id_plan, x)]
                pares += [(x, id_plan) for x in ids_nuevos if x != id_plan]
            case ListaCambioPlan.ATP | ListaCambioPlan.CONTROL:
                pares += [(x, id_plan) for x in existentes]
        secciones.append(SeccionMatriz(lista, tuple(pares)))
    return tuple(secciones)
