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
        self.__nodos = set()    #" para almacenar nodos

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

        #Verifica que no haya un generador con el mismo id en el sistema
        if generador.id in self.__generadores:
            raise ValueError("Ya existe un generador con ese id en el sistema")

        self.__generadores[generador.id] = generador
        self.__generadores_ordenados = None          #Invalida el caché

    def agregar_carga(self, carga: Carga):
        """
        Agrega una carga a la red.
        Complejidad O(1) - inserción a tabla hash.

        Args:
        carga(Carga): Objeto Carga a añadir.
        """
        if not isinstance(carga, Carga):
            raise TypeError("El argumento debe ser de tipo Carga")

        # Verificar si ya existe una carga con el mismo id
        if carga.id in self.__cargas:
            raise ValueError("Ya existe una carga con ese id en el sistema")

        # Si no existe una carga con el mismo id, se agrega y se actualiza la demanda
        self.__cargas[carga.id] = carga
        self.__demanda_total += carga.get_demanda()  #Actualiza la demanda total del sistema


    def agregar_linea(self, linea: LineaTransmision):
        """
        Agrega una línea de transmisión a la red.
        Complejidad O(1) - inserción a tabla hash.

        Args:
        linea(LineaTransmision): Objeto LineaTransmision a añadir.
        """

        if not isinstance(linea, LineaTransmision):
            raise TypeError("El argumento debe ser de tipo LineaTransmision")

        # Verificar si ya existe una línea con el mismo id
        if linea.id in self.__lineas:
            raise ValueError("Ya existe una línea con ese id en el sistema")

        # Si no existe una línea con el mismo id, se agrega al sistema.
        self.__lineas[linea.id] = linea

        #Registra los nodos extremos de cada línea, el set ignora los elementos repetidos - O(1)
        self.__nodos.add(linea.get_nodo_origen())
        self.__nodos.add(linea.get_nodo_destino())



    #####################################

    def __quicksort_generadores(self, generadores: list, izq: int, der:int) -> None:
        """
        Implementa Quicksort de forma recursiva. Ordena generadores por costo operativo,
        de menor a mayor. 

        Complejidad Promedio: O(n log n)
        Complejidad peor caso: O(n^2) (cuando el pivote siempre es extremo)
        Espacio auxiliar: O(log n) en promedio, O(n) en el peor caso (pila de recursión)

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

    def __ordenar_generadores(self) -> list:
        """
        Ordena los generadores según su costo operativo,
        de menor a mayor, utilizando QuickSort.

        Complejidad: O(1) si existe caché, O(n log n) primera vez.

        Returns:
        lista: Lista con los generadores ordenados
        """
        if self.__generadores_ordenados is None:
            lista_generadores = list(self.__generadores.values())

            self.__quicksort_generadores(
                lista_generadores, 0, len(lista_generadores) - 1
            )

            self.__generadores_ordenados = lista_generadores

        return self.__generadores_ordenados
    
###########################DESPACHO ECONOMICO###########################


    def despacho_economico(self) -> dict:
        """
        Algoritmo de despacho económico simplificado.
        Enciende generadores en orden de menor a mayor costo operativo hasta satisfacer
        la demanda total.

        Análisis de complejidad:
        - Ordenamiento por costo (Quicksort con caché): O(n log n) la primera vez,
          O(1) en llamadas siguientes sin cambios en los generadores.
        - Iteración para despacho: O(n)

        Complejidad total: O(n log n) + O(n) = O(n log n) la primera vez, 
        O(1) + O(n) = O(n) después.

        Returns:
        dict: Resultado del despacho con generadores seleccionados y costos asociados.
        """

        #Validación inicial: Si no hay generadores, no se puede despachar
        if not self.__generadores:
            return{
                "generadores_despachados": [],
                "potencia_total_despachada": 0.0, 
                "costo_total": 0.0,
                "demanda_insatisfecha": self.__demanda_total,
                "exito": False,
                "error": "No hay generadores en la red"
            }

        #Paso 1: Ordenar los generadores por costo operativo de 
        #menor a mayor (usa caché) [O(nlogn) ó O(1)]
        lista_generadores = self.__ordenar_generadores()

        #Paso 2: Despacho económico [O(n)]
        potencia_despachada = 0.0
        costo_total = 0.0
        generadores_en_servicio = []

        for generador in lista_generadores:
            #Si ya se cubrió la demanda, se detiene el despacho
            if potencia_despachada >= self.__demanda_total:
                break

            #Límites del sistema y potencia requerida
            potencia_minima = generador.get_potencia_min()
            potencia_maxima = generador.get_potencia_max()

            potencia_requerida = self.__demanda_total - potencia_despachada

            # Si la potencia requerida es menor que la potencia mínima
            # del generador, no se enciende dicho generador y se continua
            # con el siguiente
            if potencia_requerida < potencia_minima:
                continue

            #Despachar el mínimo entre lo maximo disponible y lo requerido
            potencia_a_despachar = min(potencia_maxima, potencia_requerida)

            #Acumular en los contadores
            potencia_despachada += potencia_a_despachar
            costo_generador = (potencia_a_despachar * generador.get_costo_operativo())
            costo_total += costo_generador 

            generadores_en_servicio.append({
                "generador_id": generador.id,
                "generador_nombre": generador.nombre,
                "potencia_despachada": potencia_a_despachar,
                "costo_operativo": generador.get_costo_operativo(),
                "costo_generador": costo_generador
            })

        #Cálculo de demanda insatisfecha y éxito del despacho
        demanda_insatisfecha = max(0, self.__demanda_total - potencia_despachada)
        exito = demanda_insatisfecha < 0.01   #Tolerancia numérica

        return {
            "generadores_despachados": generadores_en_servicio,
            "potencia_total_despachada": round(potencia_despachada, 2),
            "costo_total": round(costo_total, 2),
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
            "cantidad_nodos": len(self.__nodos),
            "demanda_total": self.__demanda_total,
            "generadores": {
                gen_id: {
                    "nombre": gen.nombre,
                    "potencia_max": gen.get_potencia_max(),
                    "potencia_min": gen.get_potencia_min(),
                    "costo": gen.get_costo_operativo()
                }
                for gen_id, gen in self.__generadores.items()
            }
        }
    