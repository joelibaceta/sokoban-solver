import os

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

resultados = {}

for nivel in niveles:
    resultados_nivel = {}
    for estrategia in estrategias:
        print(f"Resolviendo nivel {nivel} con {estrategia.__name__}")
        resultado = estrategia(niveles[nivel]).resolver()
        resultados_nivel[estrategia.__name__] = resultado
    resultados[nivel] = resultados_nivel

print(resultados)