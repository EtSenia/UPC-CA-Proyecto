from . import db

class Aereopuerto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    nombre = db.Column(db.String(100))
    ciudad = db.Column(db.String(40))
    pais = db.Column(db.String(40))
    latitud = db.Column(db.Float())
    longitud = db.Column(db.Float())

class Ruta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_aereopuerto_origen = db.Column(db.Integer, db.ForeignKey('aereopuerto.id'))
    id_aereopuerto_destino = db.Column(db.Integer, db.ForeignKey('aereopuerto.id'))
    distancia = db.Column(db.Float)