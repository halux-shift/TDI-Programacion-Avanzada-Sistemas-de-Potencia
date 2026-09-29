import numpy as np

#Clase padre ElementoRed
class ElementoRed:
    def __init__(self, id: str, nombre:str):
        self.id = id
        self.nombre = nombre



#Clase hija Generador que hereda ElementoRed
class Generador(ElementoRed):
    #Se decidió añadir el atributo de potencia mínima para mejorar la definición
    #del Unit Commitment, ya que algunos generadores tienen un rango de operación limitado.
    def __init__(self, id:str, nombre:str, potencia_max:float, potencia_min:float, 
    costo_operativo:int):
        super().__init__(id, nombre)
        self.__potencia_max = potencia_max        #Atributo privado
        self.__potencia_min = potencia_min        #Atributo privado
        self.__costo_operativo = costo_operativo  #Atributo privado

    #########
    #Métodos getter para acceder a los atributos privados
    def get_potencia_max(self) -> float:
        return self.__potencia_max

    def get_potencia_min(self) -> float:
        return self.__potencia_min

    def get_costo_operativo(self) -> int:
        return self.__costo_operativo
    #########



#Clase hija Carga que hereda ElementoRed
class Carga(ElementoRed):

    def __init__(self, id:str, nombre:str, tipo_carga: str, demanda:int):
        super().__init__(id, nombre)
        self.tipo_carga = tipo_carga
        self.__demanda = demanda                  #Atributo privado

    #Método getter para acceder al atributo privado demanda
    def get_demanda(self) -> int:
        return self.__demanda
        


#Clase hija LineaTransmision que hereda ElementoRed
class LineaTransmision(ElementoRed):

    def __init__(self, id:str, nombre:str, capacidad_linea:float, nodo_origen: int, nodo_destino:int, reactancia:float):
        super().__init__(id, nombre)
        self.__capacidad_linea = capacidad_linea   #Atributo privado
        self.nodo_origen = nodo_origen             #Atributo privado
        self.nodo_destino = nodo_destino           #Atributo privado
        self.__reactancia = reactancia             #Atributo privado

    #########       
    #Método getter para acceder al atributo privado capacidad_linea
    def get_capacidad_linea(self) -> float:
        return self.__capacidad_linea

    #Método getter para acceder al atributo privado reactancia
    def get_reactancia(self) -> float:
        return self.__reactancia
    #########