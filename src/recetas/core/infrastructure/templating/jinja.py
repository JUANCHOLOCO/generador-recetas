"""Adaptador TemplateRenderer sobre Jinja2."""

from jinja2 import ChoiceLoader, Environment, PackageLoader, StrictUndefined


def sql_literal(valor: object) -> str:
    """Literal SQL seguro: comillas simples escapadas; None se convierte en NULL."""
    if valor is None:
        return "NULL"
    return "'" + str(valor).replace("'", "''") + "'"


class JinjaRenderer:
    """Busca cada plantilla en los paquetes indicados, en orden (el primero gana)."""

    def __init__(self, *paquetes: str) -> None:
        self._env = Environment(
            loader=ChoiceLoader([PackageLoader(p, "templates/sql") for p in paquetes]),
            undefined=StrictUndefined,
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
            autoescape=False,
        )
        self._env.filters["sql"] = sql_literal

    def render(self, plantilla: str, **contexto: object) -> str:
        return self._env.get_template(plantilla).render(**contexto)
