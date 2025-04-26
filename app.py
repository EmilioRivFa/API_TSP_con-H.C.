from flask import Flask, render_template, jsonify
import math
import random

app = Flask(__name__)

# Coordenadas de las ciudades
coord = {
    'Jiloyork': (19.916012, -99.580580),
    'Toluca': (19.289165, -99.655697),
    'Atlacomulco': (19.799520, -99.873844),
    'Guadalajara': (20.677754472859146, -103.34625354877137),
    'Monterrey': (25.69161110159454, -100.321838480256),
    'QuintanaRoo': (21.163111924844458, -86.80231502121464),
    'Michohacan': (19.701400113725654, -101.20829680213464),
    'Aguascalientes': (21.87641043660486, -102.26438663286967),
    'CDMX': (19.432713075976878, -99.13318344772986),
    'QRO': (20.59719437542255, -100.38667040246602)
}

def distancia(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def evalua_ruta(ruta):
    total = 0
    for i in range(len(ruta) - 1):
        total += distancia(coord[ruta[i]], coord[ruta[i + 1]])
    total += distancia(coord[ruta[-1]], coord[ruta[0]])
    return total

def i_hill_climbing():
    ciudades = list(coord.keys())
    mejor_ruta_global = None
    mejor_distancia_global = float('inf')

    for _ in range(10):  # iteraciones
        ruta_actual = ciudades[:]
        random.shuffle(ruta_actual)
        mejora = True

        while mejora:
            mejora = False
            mejor_vecino = ruta_actual[:]
            mejor_distancia = evalua_ruta(ruta_actual)

            for i in range(len(ruta_actual)):
                for j in range(i + 1, len(ruta_actual)):
                    vecino = ruta_actual[:]
                    vecino[i], vecino[j] = vecino[j], vecino[i]
                    dist = evalua_ruta(vecino)
                    if dist < mejor_distancia:
                        mejor_distancia = dist
                        mejor_vecino = vecino
                        mejora = True

            ruta_actual = mejor_vecino[:]

        if evalua_ruta(ruta_actual) < mejor_distancia_global:
            mejor_distancia_global = evalua_ruta(ruta_actual)
            mejor_ruta_global = ruta_actual[:]

    return mejor_ruta_global, mejor_distancia_global

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/ruta')
def obtener_ruta():
    ruta, distancia_total = i_hill_climbing()
    return jsonify({'ruta': ruta, 'distancia': round(distancia_total, 4)})

if __name__ == '__main__':
    app.run(debug=True)
    #App.get
