from elementos_red import Generador, Carga, LineaTransmision

#Clase SistemaPotencia que contiene los elementos de la red
class SistemaPotencia:
    """
    Gestora de la red de potencia con capacidad de despacho económico.

    Utiliza tablas hash para O(1) acceso a elementos.
    Implementa QuickSort O(n log n) para ordenamiento de generadores.
    """
    def __init__(self):
        """Se inicializa la clase gestora con diccionarios vacíos."""
        self.__generadores = {} #Diccionario para almacenar generadores
        self.__cargas = {}      #" para almacenar cargas
        self.__lineas = {}      #" para almacenar líneas de transmisión
        self.__nodos = {}       #" para almacenar nodos

        self.__demanda_total = 0 #Atributo privado para almacenar la demanda total del sistema
        self.__generadores_ordenados = None #Atributo privado para almacenar los generadores ordenados 


    def agregar_generador(self, generador: Generador):
        """
        Agrega un generador al sistema de potencia.
        Complejidad O(1) - inserción a tabla hash.

        Args:
        generador(Generador): Objeto Generador a añadir.
        """
        if not isinstance(generador, Generador):
            raise TypeError("El argumento debe ser de tipo Generador")

        self.__generadores[generador.id] = generador
        self.__generadores_ordenados = None          #Evita el caché

    def agregar_carga(self, carga: Carga):
        """
        Agrega una carga a la red.
        Complejidad O(1) - inserción a tabla hash.

        Args:
        carga(Carga): Objeto Carga a añadir.
        """
        if not isinstance(carga, Carga):
            raise TypeError("El argumento debe ser de tipo Carga")

        self.__cargas[carga.id] = carga
        self.__demanda_total += carga.get_demanda()  #Actualiza la demanda total del sistema

    def agregar_linea(self, linea: LineaTransmision):
        """
        Agrega una línea de transmisión a la red.
        Complejidad O(1) - inserción a tabla hash.

        Argas:
        linea(LineaTransmision): Objeto LineaTransmision a añadir.
        """

        if not isinstance(linea, LineaTransmision):
            raise TypeError("El argumento debe ser de tipo LineaTransmision")

        self.__lineas[linea.id] = linea




    #####################################

    def __quicksort_generadores(self, generadores: list, izq: int, der:int) -> None:
        """
        Implementa Quicksort de forma recursiva. Ordena generadores por costo operativo,
        de menor a mayor. 

        Complejidad Promedio: O(n log n)
        Complejidad peor caso: O(n^2) (cuando el pivote siempre es extremo)
        Espacio auxiliar: O(log n) (pila de recursión)

        Args:
        generadores(list): Lista de objetos Generador
        izq(int): Índice izquierdo del rango
        der(int): Índice derecho del rango
        """

        if izq < der:
            #Particionamos y obtenemos el índice del pivote
            pivote = self.__particionar_generadores(generadores, izq, der)

            #Recursión para la sublista izquierda
            self.__quicksort_generadores(generadores, izq, pivote - 1)

            #Recursión para la sublista derecha
            self.__quicksort_generadores(generadores, pivote + 1, der)

    def __particionar_generadores(self, generadores: list, izq:int, der:int) -> int:
        """
        Particiona la lista alrededor de un pivote (último elemento).
        Mueve elementos con costo menor al pivote a la izquierda.

        Complejidad: O(n) - una sola pasada a través del rango.

        Args:
        generadores(list): Lista de objetos Generador
        izq(int): Índice izquierdo
        der(int): Índice derecho

        Returns:
        int: Índice donde quedó el pivote
        """

        pivote = generadores[der]
        costo_pivote = pivote.get_costo_operativo()

        #Indice que marca la frontera entre menores y mayores al pivote
        i = izq - 1

        #Recorre desde izquierda hasta el penúltimo elemento (der-1)
        for j in range(izq, der):
            if generadores[j].get_costo_operativo() < costo_pivote:
                i += 1
                generadores[i], generadores[j] = generadores[j], generadores[i]

        #Coloca el pivote en su posición final
        generadores[i+1], generadores[der] = generadores[der], generadores[i+1]
        return i +1
    
###########################DESPACHO ECONOMICO###########################


    def despacho_economico(self) -> dict:
        """
        Algoritmo de despacho económico simplificado.
        Enciende generadores en orden de menor a mayor costo operativo hasta satisfacer
        la demanda total.

        Análisis de complejidad:
        - Conversión de diccionario a lista: O(n) con n la cantidad de generadores.
        - Quicksort: O(n log n) en promedio
        - Iteración para despacho: O(n)

        Complejidad total: O(n) + O(n log n) + O(n) = O(n log n).
        El término O(n log n) es dominante (crece más rápido hacia inf.)

        Returns:
        dict: Resultado del despacho con generadores seleccionados y costos asociados.
        """

        #Validación inicial: Si no hay generadores, no se puede despachar
        if not self.__generadores:
            return{
                "generadores_despachados": [],
                "potencia_total_despachada": 0.0, 
                "costo_total": 0,
                "demanda_insatisfecha": self.__demanda_total,
                "exito": False,
                "error": "No hay generadores en la red"
            }

        #Paso 1: Convertir diccionario de generadores a lista [O(n)]
        lista_generadores = list(self.__generadores.values())

        #Paso 2: Ordenar por costo usando Quicksort [O(n log n)]
        self.__quicksort_generadores(lista_generadores, 0, len(lista_generadores) - 1)

        #Caché el resultado para futuras consultas
        self.__generadores_ordenados = lista_generadores

        #Paso 3: Despacho económico [O(n)]
        potencia_despachada = 0.0
        costo_total = 0
        generadores_en_servicio = []

        for generador in lista_generadores:
            #Si ya cubrimos la demanda, detenemos
            if potencia_despachada >= self.__demanda_total:
                break

            #Potencia disponible y requerida
            potencia_disponible = generador.get_potencia_max()
            potencia_requerida = self.__demanda_total - potencia_despachada

            #Despachar el mínimo entre lo disponible y lo requerido
            potencia_a_despachar = min(potencia_disponible, potencia_requerida)

            #Acumular en los contadores
            potencia_despachada += potencia_a_despachar
            costo_total += int(potencia_a_despachar * generador.get_costo_operativo()) 

            generadores_en_servicio.append({
                "generador_id": generador.id,
                "generador_nombre": generador.nombre,
                "potencia_despachada": potencia_a_despachar,
                "costo_operativo": generador.get_costo_operativo(),
                "costo_generador": int(potencia_a_despachar *
                                       generador.get_costo_operativo())
            })

        #Cálculo de demanda insatisfecha y éxito del despacho
        demanda_insatisfecha = max(0, self.__demanda_total - potencia_despachada)
        exito = demanda_insatisfecha < 0.01   #Tolerancia numérica

        return {
            "generadores_despachados": generadores_en_servicio,
            "potencia_total_despachada": round(potencia_despachada, 2),
            "costo_total": costo_total,
            "demanda_insatisfecha": round(demanda_insatisfecha, 2),
            "exito": exito
        }
    
    def obtener_generador(self, id_generador: str) -> Generador:
        """
        Obtiene un generador por su ID.

        Complejidad: O(1) - acceso directo en tabla hash

        Args:
        id_generador (str): ID del generador.

        Returns:
        Generador: El objeto Generador o None si no existe.
        """
        return self.__generadores.get(id_generador)
    
    def obtener_carga (self, id_carga: str) -> Carga:
        """
        Obtiene una carga por su ID.

        Complejidad: O(1) - acceso directo en tabla hash

        Args:
        id_carga (str): ID de la carga.

        Returns:
        Carga: El objeto Carga o None si no existe.
        """
        return self.__cargas.get(id_carga)

    #Retorna la estructura de la red
    #Se completa en Hito 2 o 3
    def obtener_topologia(self) -> dict:
        """
        Retorna la topología de la red en un diccionario.

        Complejidad: O(n) - iteración sobre todos los elementos.

        Returns:
        dict: Información de generadores, cargas y líneas.
        """
        return{
            "cantidad_generadores": len(self.__generadores), 
            "cantidad_cargas": len(self.__cargas),
            "cantidad_lineas": len(self.__lineas),
            "demanda_total": self.__demanda_total,
            "generadores": {
                gen_id: {
                    "nombre": gen.nombre,
                    "potencia_max": gen.get_potencia_max(),
                    "potecia_min": gen.get_potencia_min(),
                    "costo": gen.get_costo_operativo()
                }
                for gen_id, gen in self.__generadores.items()
            }
        }
    
    def obtener_generadores_ordenados(self) -> list:
        """
        Retorna lista de generadores ordenada por costo (usa caché si existe).

        Complejidad: O(1) si existe caché, O(n log n) primera vez.

        Returns:
        list: Generadores ordenados de menor a mayor costo.

        """
        if self.__generadores_ordenados is None:
            self.despacho_economico()

        return self.__generadores_ordenados if self.__generadores_ordenados else []