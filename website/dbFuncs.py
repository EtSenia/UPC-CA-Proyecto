from . import models, db, functions
import math

class nodo:
    def __init__(self, id, nombre, ciudad, pais, latitud, longitud):
        self.id = id
        self.nombre = nombre
        self.ciudad = ciudad
        self.pais = pais
        self.latitud = latitud
        self.longitud = longitud
        self.conexiones = False

def cargar_datos_en_bd():
    with db.session.begin():
        db.session.query(models.Aereopuerto).delete()
        db.session.query(models.Ruta).delete()

    nodos, rutas = cargar()
    #functions.crear_imagen(nodos, rutas)
    with db.session.begin():
        for i, a in nodos.items():
            if a.conexiones:
                aereopuerto = models.Aereopuerto(
                            id=a.id,
                            nombre=a.nombre,
                            ciudad=a.ciudad,
                            pais=a.pais,
                            latitud=a.latitud,
                            longitud=a.longitud
                            )
                db.session.add(aereopuerto)
        
        for a1, a2, d in rutas:
            ruta = models.Ruta(id_aereopuerto_origen=a1, id_aereopuerto_destino=a2, distancia=d)
            db.session.add(ruta)
        
        db.session.commit()

def distancia_haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(math.radians, [lat1, lon1, lat2, lon2])

    d_lat = lat2_rad - lat1_rad
    d_lon = lon2_rad - lon1_rad

    e1 = math.sin(d_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(d_lon/2)**2

    return 2 * R * math.asin(math.sqrt(e1))

def cargar():
    nodos = {}
    rutas = []
    with open('airports.dat', 'r', encoding='utf-8') as file:
        lines = file.readlines()

        for linea in lines:
            campos = []
            dentro_comillas = False
            campo_actual = ''

            for char in linea:
                if char == ',' and not dentro_comillas:
                    campos.append(campo_actual)
                    campo_actual = ''
                elif char == '"':
                    dentro_comillas = not dentro_comillas
                else:
                    campo_actual += char

            campos.append(campo_actual.strip())  # Añadir el último campo
            
            nodos[int(campos[0])] = nodo(int(campos[0]), campos[1], campos[2], campos[3], float(campos[6]), float(campos[7]))

    with open('routes.dat', 'r') as file:
        lines = file.readlines()
        added = set()
        for line in lines:
            line = line.strip()

            values = line.split(',')
            # 3 y 5

            if values[3] == '\\N' or values[5] == '\\N':
                continue
            if not int(values[3]) in nodos or not int(values[5]) in nodos:
                continue


            n1 = nodos[int(values[3])]
            n2 = nodos[int(values[5])]

            if f"{n1.id},{n2.id}" in added or f"{n2.id},{n1.id}" in added:
                continue

            nodos[int(values[3])].conexiones = True
            nodos[int(values[5])].conexiones = True

            added.add(f"{n1.id},{n2.id}")
            added.add(f"{n2.id},{n1.id}")
            
            distancia = distancia_haversine(n1.latitud, n1.longitud, n2.latitud, n2.longitud)

            rutas.append((n1.id, n2.id, distancia))
    return nodos, rutas
