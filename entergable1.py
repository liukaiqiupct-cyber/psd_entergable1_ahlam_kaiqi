from abc import ABC, abstractmethod
from enum import Enum
from typing import List

# ==================== EXCEPCIONES ====================

class ErrorStockInsuficiente(Exception):
    pass

class ErrorRepuestoNoEncontrado(Exception):
    pass

class ErrorUbicacionInvalida(Exception):
    pass

class ErrorClaseNaveInvalida(Exception):
    pass

# ==================== ENUMERACIONES ====================

class ClaseNave(Enum):
    EJECUTOR = "Ejecutor"
    ECLIPSE = "Eclipse"
    SOBERANO = "Soberano"

class Ubicacion(Enum):
    ENDOR = "Endor"
    CUMULO_RAIMOS = "Cúmulo Raimos"
    NEBULOSA_KALIIDA = "Nebulosa Kaliida"

# ==================== CLASES ABSTRACTAS ====================

class UnidadCombate(ABC):
    def __init__(self, id_combate: str, clave_cifrada: int):
        self._id_combate = id_combate
        self._clave_cifrada = clave_cifrada

    def get_id(self) -> str:
        return self._id_combate

    def get_clave_cifrada(self) -> int:
        return self._clave_cifrada

    @abstractmethod
    def mostrar_info(self) -> str:
        pass

class Nave(UnidadCombate, ABC):
    def __init__(self, nombre: str, catalogo_repuesto: List[str], id_combate: str, clave_cifrada: int):
        super().__init__(id_combate, clave_cifrada)
        self._nombre = nombre
        self._catalogo_repuesto = catalogo_repuesto

    def get_nombre(self) -> str:
        return self._nombre

    def añadir_repuesto(self, repuesto: str):
        if repuesto not in self._catalogo_repuesto:
            self._catalogo_repuesto.append(repuesto)

    def consultar_repuesto(self) -> List[str]:
        return self._catalogo_repuesto.copy()

    @abstractmethod
    def mostrar_info(self) -> str:
        pass

# ==================== NAVES ====================

class NaveEstelar(Nave):
    def __init__(self, nombre, catalogo_repuesto, id_combate, clave_cifrada,
                 tripulacion, pasaje, clase):
        super().__init__(nombre, catalogo_repuesto, id_combate, clave_cifrada)
        self._tripulacion = tripulacion
        self._pasaje = pasaje
        if not isinstance(clase, ClaseNave):
            raise ErrorClaseNaveInvalida
        self._clase = clase

    def get_tripulacion_nav_estelar(self):
        return self._tripulacion

    def get_pasaje_nav_estelar(self):
        return self._pasaje

    def get_clase(self):
        return self._clase.value

    def mostrar_info(self):
        return f"Nave Estelar: {self._nombre}\nID Combate: {self.get_id()}"

    def __str__(self):
        return self.mostrar_info()

class CazaEstelar(Nave):
    def __init__(self, nombre, catalogo_repuesto, id_combate, clave_cifrada, dotacion):
        super().__init__(nombre, catalogo_repuesto, id_combate, clave_cifrada)
        self._dotacion = dotacion

    def get_dotacion(self):
        return self._dotacion

    def mostrar_info(self):
        return f"Caza Estelar: {self._nombre}"

    def __str__(self):
        return self.mostrar_info()

class EstacionEspacial(Nave):
    def __init__(self, nombre, catalogo_repuesto, id_combate, clave_cifrada,
                 tripulacion, pasaje, ubicacion):
        super().__init__(nombre, catalogo_repuesto, id_combate, clave_cifrada)
        self._tripulacion = tripulacion
        self._pasaje = pasaje
        if not isinstance(ubicacion, Ubicacion):
            raise ErrorUbicacionInvalida
        self._ubicacion = ubicacion

    def get_ubicacion(self):
        return self._ubicacion.value

    def mostrar_info(self):
        return f"Estación Espacial: {self._nombre}"

    def __str__(self):
        return self.mostrar_info()

# ==================== REPUESTOS ====================

class Repuesto:
    def __init__(self, nombre: str, proveedor: str, cantidad: int, precio: float):
        self._nombre = nombre
        self._proveedor = proveedor
        self.__cantidad = cantidad
        self._precio = precio

    def get_nombre(self):
        return self._nombre

    def get_proveedor(self):
        return self._proveedor

    def get_cantidad(self):
        return self.__cantidad

    def set_cantidad(self, cantidad):
        if cantidad < 0:
            raise ValueError
        self.__cantidad = cantidad

    def get_precio(self):
        return self._precio

    def añadir_stock(self, cantidad):
        if cantidad < 0:
            raise ValueError
        self.__cantidad += cantidad

    def retirar_stock(self, cantidad):
        if cantidad <= 0:
            raise ValueError
        if cantidad <= self.__cantidad:
            self.__cantidad -= cantidad
            return cantidad
        retirado = self.__cantidad
        self.__cantidad = 0
        return retirado

    def __str__(self):
        return f"Repuesto: {self._nombre}, Proveedor: {self._proveedor}, Cantidad: {self.__cantidad}, Precio: {self._precio}€"

    def __eq__(self, other):
        return isinstance(other, Repuesto) and self._nombre == other._nombre

# ==================== ALMACEN ====================

class Almacen:
    def __init__(self, nombre, ubicacion):
        self._nombre = nombre
        self._ubicacion = ubicacion
        self._catalogo = []

    def get_nombre(self):
        return self._nombre

    def get_ubicacion(self):
        return self._ubicacion

    def añadir_repuesto(self, repuesto):
        self._catalogo.append(repuesto)

    def eliminar_repuesto(self, nombre):
        for rep in self._catalogo:
            if rep.get_nombre() == nombre:
                self._catalogo.remove(rep)
                return
        raise ErrorRepuestoNoEncontrado

    def consultar_stock(self, nombre):
        for rep in self._catalogo:
            if rep.get_nombre() == nombre:
                return rep.get_cantidad()
        raise ErrorRepuestoNoEncontrado

    def actualizar_stock(self, nombre, cantidad):
        for rep in self._catalogo:
            if rep.get_nombre() == nombre:
                if cantidad > rep.get_cantidad():
                    raise ErrorStockInsuficiente
                rep.set_cantidad(rep.get_cantidad() - cantidad)
                return
        raise ErrorRepuestoNoEncontrado

    def valor_total_stock(self):
        return sum(r.get_cantidad() * r.get_precio() for r in self._catalogo)

    def __str__(self):
        info = f"Almacén: {self._nombre} ({self._ubicacion})\n"
        info += f"Repuestos disponibles: {len(self._catalogo)}\n"
        for repuesto in self._catalogo:
            info += f"  - {repuesto}\n"
        return info
