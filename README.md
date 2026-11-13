# Simulador de red de sistemas de potencia

Proyecto semestral de Programación Avanzada. Simula una red eléctrica compuesta por generadores, cargas y líneas de transmisión, y calcula el **despacho económico**: qué generadores encender, y cuánta potencia entregar 
cada uno, para cubrir la demanda al menor costo.

Integrantes
- Danae Merillu R.
- Belén Cortés F.

# Estructura del repositorio
| Archivo | Descripción |
|---|---|
| `elementos_red.py` | Clases `ElementoRed`, `Generador`, `Carga` y `LineaTransmision` |
| `sistema_potencia.py` | Clase `SistemaPotencia`: gestiona la red, ordena generadores y calcula el despacho |
| `main_hito2.py` | Programa de demostración |

# Requisitos y ejecución
- Python 3.10 o superior (no requiere librerías externas)

# Cómo ejecutar:
1) Ejecutar el archivo `elementos_red.py`
2) Luego, ejecutar el archivo `sistema_potencia.py`
3) Ejecutar el archivo de demostración `main_hito2.py`

# Ejemplo de resultado
Con los datos de `main_hito2.py` (5 generadores, 3 cargas y 3 líneas):
- 3 nodos en el sistema.
- Demanda total de 500 MW, cubierta por Gen_Sur, Gen_Solar y Gen_Central.
- Costo total de operación de 8.000 $/h.

# Flujo de trabajo en Git
- `main`: versión estable.
- `codigo_hito2`: rama de desarrollo del hito 2, integrada a `main` mediante pull request.
