import os
import csv
import concurrent.futures

from strategies import BFSStrategy, DFSStrategy, IDDFSStrategy, AStarStrategy, IDAStarStrategy

ruta_niveles = "levels"
archivos = [f for f in os.listdir(ruta_niveles) if os.path.isfile(os.path.join(ruta_niveles, f))]

niveles = {}

for archivo in archivos:
    with open(os.path.join(ruta_niveles, archivo), "r") as f:
        lineas = f.readlines()
        datos = [list(linea.rstrip()) for linea in lineas]
        niveles[archivo.split(".")[0]] = datos

print(niveles)

estrategias = [BFSStrategy, DFSStrategy, IDDFSStrategy, AStarStrategy, IDAStarStrategy]

# ["Algoritmo", "Tiempo", "Nodos generados", "Nodos abiertos", "Profundidad máxima"]

def resolver_nivel_con_estrategia(nivel, estrategia):
    print(f"Resolviendo nivel {nivel} con {estrategia.__name__}")
    resultado = estrategia(niveles[nivel]).resolver()
    return estrategia.__name__, resultado


resultados = {}

for nivel in niveles:
    resultados_nivel = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Crear una lista de tareas para cada estrategia
        futures = [executor.submit(resolver_nivel_con_estrategia, nivel, estrategia) for estrategia in estrategias]
        for future in concurrent.futures.as_completed(futures):
            estrategia_nombre, resultado = future.result()
            resultados_nivel[estrategia_nombre] = resultado
    resultados[nivel] = resultados_nivel

print(resultados)

with open("resultados.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Nivel", "Algoritmo", "Hay Solucion?", "Tiempo", "Nodos generados", "Nodos abiertos", "Profundidad máxima"])
    for nivel in resultados:
        for estrategia in resultados[nivel]:
            resultado = resultados[nivel][estrategia]
            writer.writerow([nivel, estrategia, (resultado["camino"] != None), resultado["tiempo_total"], resultado["nodos_generados"], resultado["nodos_abiertos"], resultado["profundidad_maxima"]])