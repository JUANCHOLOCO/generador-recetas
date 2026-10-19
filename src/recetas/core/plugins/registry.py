"""Registro de los módulos instalados en la aplicación."""

from recetas.core.domain.errors import DuplicateModuleError, UnknownModuleError
from recetas.core.plugins.module import Module


class ModuleRegistry:
    def __init__(self) -> None:
        self._modules: dict[str, Module] = {}

    def register(self, module: Module) -> None:
        module_id = module.info.id
        if module_id in self._modules:
            raise DuplicateModuleError(module_id)
        self._modules[module_id] = module

    def get(self, module_id: str) -> Module:
        try:
            return self._modules[module_id]
        except KeyError:
            raise UnknownModuleError(module_id) from None

    def modules(self) -> list[Module]:
        """Módulos ordenados por `order` y luego por nombre."""
        return sorted(self._modules.values(), key=lambda m: (m.info.order, m.info.name))

    def __len__(self) -> int:
        return len(self._modules)

    def __contains__(self, module_id: object) -> bool:
        return module_id in self._modules
