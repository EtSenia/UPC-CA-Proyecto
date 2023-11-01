from . import models, db
import math
import time
import heapq as hq

def latlon_to_xy(lat, lon):

    R = 6371000.0
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)

    
    tan_arg = max(0.000001, math.tan(math.pi / 4 + lat_rad / 2))

    x = R / 100000 * lon_rad
    y = R / 100000 * math.log(tan_arg)

    return x , y

def crear_grafo():
    G = {}
    rutas = []
    

    inicio = time.time()
    with db.session.begin():
        rutas = db.session.query(models.Ruta).all()
        db.session.remove()
    for ruta in rutas:
        origen = ruta.id_aereopuerto_origen
        destino = ruta.id_aereopuerto_destino
        distancia = ruta.distancia

        # Agregar una entrada para el nodo de origen si aún no existe
        if origen not in G:
            G[origen] = []

        # Agregar la arista al grafo
        G[origen].append((destino, distancia))

    fin = time.time()
    print(f"Tiempo: {fin - inicio} segundos")

    return G



"""def Dijkstra(Grafo, ):
    n = len(Grafo)
    visited = [False] * n
    path = [-1] * n
    cost = [math.inf] * n

    cost[nodo_inicial] = 0
    pqueue = [(0, nodo_inicial)]

    while pqueue:
        g, u = hq.heappop(pqueue)
        if not visited[u]:
            visited[u] = True
            for v, w in Grafo[u]:
                if not visited[v]:
                    f = g + w
                    if f < cost[v]:
                        cost[v] = f
                        path[v] = u
                        hq.heappush(pqueue, (f, v))
    return path, cost"""

def dijkstra(grafo, inicio, nodos_a_evitar=[]):
    inicio_t = time.time()

    distancias = {nodo: float('infinity') for nodo in grafo}
    camino = {nodo: -1 for nodo in grafo}

    visitados = set()
    distancias[inicio] = 0


    cola_prioridad = [(0, inicio)]

    while cola_prioridad:
        distancia_actual, nodo_actual = hq.heappop(cola_prioridad)
        if nodo_actual in grafo:
            if not nodo_actual in visitados:
                visitados.add(nodo_actual)
                for v, peso in grafo[nodo_actual]:
                    if nodos_a_evitar and v in nodos_a_evitar: continue
                    if not v in visitados:
                        distancia_nueva = distancia_actual + peso
                        if v not in distancias or distancia_nueva < distancias[v]:
                            distancias[v] = distancia_nueva
                            camino[v] = nodo_actual
                            hq.heappush(cola_prioridad, (distancia_nueva, v))

    fin = time.time()
    print(f"Tiempo dijkstra: {fin - inicio_t} segundos")
    return camino, distancias