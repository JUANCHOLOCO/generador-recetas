"""Lo que cambia según el tipo de facturación (patrón Strategy)."""

from abc import ABC, abstractmethod
from typing import assert_never

from recetas.core.domain.billing import BillingType

SUFIJO_FC = " FC"


class BillingStrategy(ABC):
    @property
    @abstractmethod
    def tipo(self) -> BillingType: ...

    @property
    @abstractmethod
    def billing_type_plans(self) -> str:
        """Valor de ACTIVATOR.PLANS.BILLING_TYPE."""

    @property
    @abstractmethod
    def carpeta(self) -> str:
        """Carpeta de la receta dentro del RQ."""

    @property
    @abstractmethod
    def sufijo_rq(self) -> str:
        """Sufijo del RQ en nombres de archivo y cabeceras de los scripts."""

    @property
    @abstractmethod
    def sufijo_propiedades(self) -> str:
        """Sufijo de las claves .properties propias del tipo (idPlansNintendo<sufijo>)."""

    @abstractmethod
    def advertencia_nombre(self, nombre: str) -> str | None:
        """Mensaje si el nombre no parece de este tipo de facturación; None si está bien."""

    def rq_archivos(self, requerimiento: str) -> str:
        return f"{requerimiento}{self.sufijo_rq}"


class CorrienteStrategy(BillingStrategy):
    @property
    def tipo(self) -> BillingType:
        return BillingType.CORRIENTE

    @property
    def billing_type_plans(self) -> str:
        return "Vencida"

    @property
    def carpeta(self) -> str:
        return "Corriente"

    @property
    def sufijo_rq(self) -> str:
        return "_CORRIENTE"

    def advertencia_nombre(self, nombre: str) -> str | None:
        if nombre.endswith(SUFIJO_FC):
            return None
        return f"'{nombre}' no termina en 'FC', habitual en planes Corriente."

    @property
    def sufijo_propiedades(self) -> str:
        return "Corriente"

class AnticipadaStrategy(BillingStrategy):
    @property
    def tipo(self) -> BillingType:
        return BillingType.ANTICIPADA

    @property
    def billing_type_plans(self) -> str:
        return "Anticipada"

    @property
    def carpeta(self) -> str:
        return "Anticipados"

    @property
    def sufijo_rq(self) -> str:
        return ""

    def advertencia_nombre(self, nombre: str) -> str | None:
        if not nombre.endswith(SUFIJO_FC):
            return None
        return (
            f"'{nombre}' termina en 'FC', propio de Corriente. ¿El tipo de facturación es correcto?"
        )

    @property
    def sufijo_propiedades(self) -> str:
        return ""
    

def estrategia_para(tipo: BillingType) -> BillingStrategy:
    match tipo:
        case BillingType.CORRIENTE:
            return CorrienteStrategy()
        case BillingType.ANTICIPADA:
            return AnticipadaStrategy()
        case _:
            assert_never(tipo)
