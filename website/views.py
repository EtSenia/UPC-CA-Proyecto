from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from . import models, db, functions
from . import dbFuncs

views = Blueprint('views', __name__)
G = {}

@views.route('/', methods=['GET', 'POST'])
def home():
    global G
    action = request.form.get("action")
    
    if action == 'dbload':
        try:
            dbFuncs.cargar_datos_en_bd()
            flash('Database cargada exitosamente', category='success')
            G = functions.crear_grafo()
            flash('Grafo creado exitosamente', category='success')
        except Exception as e:
            flash(f'Error al cargar la base de datos: {str(e)}', category='error')
          
    return render_template("home.html")

@views.route('/buscar', methods=['GET'])
def buscar():
    query = request.args.get('termino', '')
    results = models.Aereopuerto.query.filter(models.Aereopuerto.ciudad.ilike(f'%{query}%')).all()
    
    suggestions = set()
    exactos = set()
    for item in results:
        ciudad_pais = f"{item.ciudad}, {item.pais}"

        if item.ciudad.lower() == query.lower():
            exactos.add(ciudad_pais)
        else:
            suggestions.add(ciudad_pais)

        if len(suggestions) >= 10:
            break
    resultados = list(exactos) + list(suggestions)
    return jsonify({'suggestions': resultados})

@views.route('/map', methods=['GET', 'POST'])
def mapa():
    global G
    if not G:
        G = functions.crear_grafo()
    camino, costo = functions.dijkstra(G, 2786, [1847])
    print(f'La distancia es: {costo[2279]}')
    index = 2279
    temp = []
    while index != -1:
        temp.append(index)
        index = camino[index] 
    print(temp)
    temp.reverse()
    aeropuertos = []
    with db.session.begin():
        for a in temp:
            aeropuerto = db.session.query(models.Aereopuerto).get(a)
            aeropuertos.append({'nombre': aeropuerto.ciudad + ', ' + aeropuerto.pais + ' (' + aeropuerto.nombre +')', 'lat': aeropuerto.latitud, 'lon': aeropuerto.longitud})

    return render_template('mapa.html', aeropuertos=aeropuertos)

@views.route('/get_suggestions')
def get_suggestions():
    input_text = request.args.get('input')
    if len(input_text) == 0:
        return jsonify({'suggestions': []})
    results = models.Aereopuerto.query.filter(models.Aereopuerto.ciudad.ilike(f'%{input_text}%')).all()
    print(input_text)
    suggestions = set()
    exactos = set()
    for item in results:
        ciudad_pais = f"{item.ciudad}, {item.pais}"

        if item.ciudad.lower() == input_text.lower():
            exactos.add(ciudad_pais)
        else:
            suggestions.add(ciudad_pais)

        if len(suggestions) >= 10:
            break
    resultados = list(exactos) + list(suggestions)
    return jsonify({'suggestions': resultados})