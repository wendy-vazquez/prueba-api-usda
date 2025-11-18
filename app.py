from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "zHYga31MsqopFACKsNz8AWNXvs0h6tyKxULQ9hKz"
API_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

# Recetas predeterminadas
RECETAS = [
    {
        "nombre": "Ensalada de pollo",
        "descripcion": "Una ensalada ligera con pollo a la plancha, lechuga y aceite de oliva.",
        "ingredientes": [
            {"nombre": "chicken breast", "cantidad": 150, "unidad": "g"},
            {"nombre": "lettuce", "cantidad": 50, "unidad": "g"},
            {"nombre": "olive oil", "cantidad": 10, "unidad": "g"},
        ],
        "preparacion": [
            "Cocina la pechuga de pollo a la plancha hasta que esté bien cocida.",
            "Lava y corta la lechuga.",
            "Mezcla todo en un tazón y agrega el aceite de oliva por encima."
        ]
    },
    {
        "nombre": "Avena con plátano y miel",
        "descripcion": "Desayuno nutritivo con avena cocida, plátano en rodajas y un toque de miel.",
        "ingredientes": [
            {"nombre": "oats", "cantidad": 40, "unidad": "g"},
            {"nombre": "banana", "cantidad": 100, "unidad": "g"},
            {"nombre": "honey", "cantidad": 15, "unidad": "g"},
        ],
        "preparacion": [
            "Cocina la avena en agua o leche durante unos minutos.",
            "Corta el plátano en rodajas y agrégalo encima.",
            "Añade miel al gusto y mezcla suavemente."
        ]
    },
    {
        "nombre": "Tacos de carne asada",
        "descripcion": "Tacos mexicanos con carne asada, cebolla y cilantro.",
        "ingredientes": [
            {"nombre": "beef steak", "cantidad": 120, "unidad": "g"},
            {"nombre": "onion", "cantidad": 30, "unidad": "g"},
            {"nombre": "cilantro", "cantidad": 10, "unidad": "g"},
            {"nombre": "corn tortilla", "cantidad": 2, "unidad": "pieza"},
        ],
        "preparacion": [
            "Asa la carne hasta que esté bien cocida y córtala en trozos pequeños.",
            "Pica la cebolla y el cilantro.",
            "Sirve la carne sobre las tortillas y añade la cebolla y el cilantro por encima."
        ]
    }
]

# Obtener nutrientes desde USDA
def obtener_nutrientes(ingrediente):
    params = {
        "query": ingrediente,
        "pageSize": 1,
        "api_key": API_KEY
    }
    resp = requests.get(API_URL, params=params)
    data = resp.json()

    if not data.get("foods"):
        return None

    nutrientes = {}
    for n in data["foods"][0]["foodNutrients"]:
        nombre = n.get("nutrientName", "").lower()
        valor = n.get("value", 0)
        unidad = n.get("unitName", "")

        if "energy" in nombre:
            nutrientes["Energía (kcal)"] = f"{valor} {unidad}"
        elif "protein" in nombre:
            nutrientes["Proteínas"] = f"{valor} {unidad}"
        elif "fat" in nombre:
            nutrientes["Grasas"] = f"{valor} {unidad}"
        elif "carbohydrate" in nombre:
            nutrientes["Carbohidratos"] = f"{valor} {unidad}"

    return nutrientes

# Traducción básica
def traducir_ingrediente(nombre):
    traducciones = {
        "chicken breast": "pechuga de pollo",
        "lettuce": "lechuga",
        "olive oil": "aceite de oliva",
        "oats": "avena",
        "banana": "plátano",
        "honey": "miel",
        "beef steak": "carne de res",
        "onion": "cebolla",
        "cilantro": "cilantro",
        "corn tortilla": "tortilla de maíz"
    }
    return traducciones.get(nombre, nombre)

# Rutas
@app.route('/')
def index():
    return render_template('index.html', recetas=RECETAS)

@app.route('/receta/<int:id>')
def receta(id):
    receta = RECETAS[id]
    datos_ingredientes = []

    for ingr in receta["ingredientes"]:
        info = obtener_nutrientes(ingr["nombre"])
        datos_ingredientes.append({
            "nombre": traducir_ingrediente(ingr["nombre"]),
            "cantidad": ingr["cantidad"],
            "unidad": ingr["unidad"],
            "nutrientes": info or {}
        })

    return render_template('receta.html', receta=receta, ingredientes=datos_ingredientes)

if __name__ == '__main__':
    app.run(debug=True)
