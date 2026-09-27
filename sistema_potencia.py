from elementos_red import Generador, Carga, LineaTransmision

#Clase SistemaPotencia que contiene los elementos de la red
class SistemaPotencia:
    def __init__(self):
        self.__generadores = {} #Diccionario para almacenar generadores
        self.__cargas = {}      #" para almacenar cargas
        self.__lineas = {}      #" para almacenar líneas de transmisión
        self.__nodos = {}       #" para almacenar nodos

    def agregar_generador(self, generador):
        self.__generadores[generador.id] = generador

    def agregar_carga(self, carga):
        self.__cargas[carga.id] = carga

    #Retorna la estructura de la red
    #Se completa en Hito 2 o 3
    def obtener_topologia(self):
        pass