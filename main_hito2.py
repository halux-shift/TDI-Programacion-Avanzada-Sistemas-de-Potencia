import math 
from elementos_red import Generador, Carga, LineaTransmision
from sistema_potencia import SistemaPotencia

def main():
    # =====================================================================
    #Crear sistema de potencia
    sistema = SistemaPotencia()
    print("Sistema de potencia creado.")

    # =====================================================================
    #Agregar generadores
    print("Agregando generadores...")
 
    gen1 = Generador("Gen_Central", "Central hidroeléctrica", potencia_max = 300.0, 
                     potencia_min = 50.0, costo_operativo = 25)
    gen2 = Generador("Gen_Norte", "Central térmica norte", potencia_max = 200.0,
                     potencia_min = 30.0, costo_operativo = 75)
    gen3 = Generador("Gen_Sur", "Central eólica sur",
                     potencia_max = 150.0, potencia_min = 0.0, costo_operativo = 5)
    gen4 = Generador("Gen_Este", "Central térmica este", potencia_max = 250.0,
                     potencia_min = 60.0, costo_operativo = 60)
    gen5 = Generador("Gen_Solar", "Planta solar", potencia_max = 100.0,
                     potencia_min = 0.0, costo_operativo = 10.0)
    
    sistema.agregar_generador(gen1)
    sistema.agregar_generador(gen2)
    sistema.agregar_generador(gen3)
    sistema.agregar_generador(gen4)
    sistema.agregar_generador(gen5)

    print(f"{gen1.nombre} Costo: ${gen1.get_costo_operativo()}/MWh")
    print(f"{gen2.nombre} Costo: ${gen2.get_costo_operativo()}/MWh")
    print(f"{gen3.nombre} Costo: ${gen3.get_costo_operativo()}/MWh")
    print(f"{gen4.nombre} Costo: ${gen4.get_costo_operativo()}/MWh")
    print(f"{gen5.nombre} Costo: ${gen5.get_costo_operativo()}/MWh")

    # =====================================================================
    #####Proceso de agregar cargas

    print("Agregando cargas...")
    carga1 = Carga("Carga_Santiago", "Demanda centro", demanda = 250)
    carga2 = Carga("Carga_Valparaiso", "Demanda puerto", demanda = 150)
    carga3 = Carga("Carga_Concepcion", "Demanda Sur", demanda = 100)

    sistema.agregar_carga(carga1)
    sistema.agregar_carga(carga2)
    sistema.agregar_carga(carga3)

    demanda_total = (carga1.get_demanda() + carga2.get_demanda() + carga3.get_demanda())
    print(f" {carga1.nombre}: {carga1.get_demanda()} MW")
    print(f" {carga2.nombre}: {carga2.get_demanda()} MW")
    print(f" {carga3.nombre}: {carga3.get_demanda()} MW")
    print(f"Demanda total: {demanda_total} MW")

    # =====================================================================
    #Ejecutar despacho económico
    print("\n" + "="*70)
    print("Ejecutando despacho económico (Quicksort O(n log n))")
    print("="*70)
 
    resultado = sistema.despacho_economico()

    # =====================================================================
    #Mostrar resultados
    print("\n[Resultado del despacho]")
    print("-"*70)
 
    if resultado["exito"]:
        print(f"Despacho exitoso")
    else:
        print(f"Despacho con insuficiencia")
 
    print(f"\nGeneradores Despachados (en orden de menor a mayor costo):")
    print("-"*70)
 
    total_despachado = 0.0
    for i, gen in enumerate(resultado["generadores_despachados"], 1):
        total_despachado += gen["potencia_despachada"]
        print(f"{i}. {gen['generador_nombre']:30s}")
        print(f"ID: {gen['generador_id']:20s} | Costo: ${gen['costo_operativo']}/MWh")
        print(f"Potencia Despachada: {gen['potencia_despachada']:6.1f} MW | Costo: ${gen['costo_generador']}")
        print()
 
    print("-"*70)
    print(f"Potencia Total Despachada: {resultado['potencia_total_despachada']:.2f} MW")
    print(f"Demanda Total Required:    {demanda_total} MW")
    print(f"Demanda Insatisfecha:      {resultado['demanda_insatisfecha']} MW")
    print(f"Costo Total de Operación:  ${resultado['costo_total']:,} por hora")
 
    # =====================================================================
    #Análsis de complejidad
   
    print("\n" + "="*70)
    print("Análisis de complejidad asintótica")
    print("="*70)
 
    N = len(sistema.obtener_topologia()["generadores"])
 
    print(f"\nCantidad de Generadores (n): {N}")
    print(f"\nOperación                | Complejidad | Descripción")
    print("-"*70)
    print(f"Conversión a lista         | O(n)        | dict → list")
    print(f"Quicksort                  | O(n log n)  | Ordenamiento recursivo")
    print(f"Despacho iterativo         | O(n)        | Selección de generadores")
    print(f"Complejidad total          | O(n log n)  | Término dominante")
 
    print(f"\nComparación con alternativas:")
    print("-"*70)
    print(f"Bubble Sort (naive):       O(n²)       ≈ {N}² = {N**2} comparaciones")
    print(f"Quicksort (propuesto):     O(n log n)  ≈ {N} × log₂({N}) ≈ {N * math.log2(N):.1f} comparaciones")
    print(f"Mejora:                    ~{N**2 // (N*20)}x más rápido")
 
    print("\n" + "="*70)
 
if __name__ == "__main__":
    main()