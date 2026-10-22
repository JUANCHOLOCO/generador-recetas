"""Excepciones de la aplicación. Todas heredan de RecetasError."""


class RecetasError(Exception):
    """Error base: la UI puede capturar cualquier error propio con un solo except."""


class DuplicateModuleError(RecetasError):
    def __init__(self, module_id: str) -> None:
        super().__init__(f"El módulo '{module_id}' ya está registrado.")
        self.module_id = module_id


class UnknownModuleError(RecetasError):
    def __init__(self, module_id: str) -> None:
        super().__init__(f"No existe un módulo registrado con id '{module_id}'.")
        self.module_id = module_id


class InvalidRecipePathError(RecetasError):
    def __init__(self, path: str) -> None:
        super().__init__(
            f"Ruta de receta inválida: '{path}'. Use rutas relativas con '/' y sin '..'."
        )
        self.path = path


class DuplicateRecipeFileError(RecetasError):
    def __init__(self, path: str) -> None:
        super().__init__(f"El archivo '{path}' ya existe en la receta.")
        self.path = path


class InvalidRecipeContentError(RecetasError):
    def __init__(self, path: str, encoding: str, caracteres: str) -> None:
        super().__init__(
            f"El archivo '{path}' contiene caracteres que no existen en {encoding}: {caracteres!r}"
        )
        self.path = path
        self.caracteres = caracteres


class RecetaExistenteError(RecetasError):
    def __init__(self, rutas: list[str]) -> None:
        super().__init__(
            f"Ya existe una receta en: {', '.join(rutas)}. Confirme si desea sobrescribirla."
        )
        self.rutas = rutas
