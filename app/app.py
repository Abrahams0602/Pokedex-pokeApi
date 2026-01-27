from flask import Flask, render_template, request
import requests

app = Flask(__name__)

URL_POKEMON= "https://pokeapi.co/api/v2/pokemon/"
URL_TIPO = "https://pokeapi.co/api/v2/type/"

#   Busqueda por nombre: 
# -Recibe el nombre del Pokémon desde request.form.
# -Hace una petición (requests.get) a la URL de la PokeAPI.
# -Si la respuesta es exitosa (200), extrae: Nombre, Tipos, Movimientos (limitados a 10) y las imágenes (Sprites).
#     Filtrado por tipo:
# -Recibe el tipo seleccionado (ej: "fire").
# -Pide a la API la lista de todos los Pokémon de ese tipo.
# -Procesamiento de IDs: Como la lista de tipos no trae imágenes, recorre la lista y extrae el número de ID de la URL de cada Pokémon para que el HTML pueda construir el link de la foto directamente.
#  Envía al archivo index.html tres variables clave: pokemon (datos individuales), tipo_data (la lista filtrada) y error (si algo salió mal).

@app.route('/', methods=["GET","POST"])
def index():
    datos_pokemon = {}#Diccionario que luego se enviará al HTML si se encuentra un Pokémon
    lista_por_tipo = None
    error = None #En caso de que el Pokémon no exista o haya un error en la petición.

    if request.method == "POST":
        nombre = request.form.get("pokemon", "").lower() #obtiene el texto escrito en el input name="pokemon" del formulario HTML. / .lower(): lo pasa a minúsculas para evitar errores de búsqueda.
        tipo_elegido = request.form.get("type_filter")
        
        if nombre:
            respuesta = requests.get(URL_POKEMON + nombre)   
            if respuesta.status_code == 200:
                datos = respuesta.json() #agarra el objeto 'respuesta' y lo convierte en formato json
                official_art = datos["sprites"]["other"]["official-artwork"]["front_default"]
                gen_8_sprite = datos["sprites"]["versions"]["generation-viii"]["brilliant-diamond-shining-pearl"]["front_default"]
                datos_pokemon ={
                    "name": datos["name"],
                    "types":[t["type"]["name"] for t in datos["types"]],
                    "moves":[m["move"]["name"] for m in datos["moves"]],
                    "sprite": gen_8_sprite if gen_8_sprite else official_art,
                    "sprite_back": datos["sprites"]["front_default"],  #una URL de una imagen del Pokémon (sprite frontal).
                }


            else:
                error ="¡ERROR! Pokémon no encontrado :(" #Si la API devuelve otro código (como 404), se asigna un mensaje de error.

        elif tipo_elegido:
            respuesta = requests.get( URL_TIPO + tipo_elegido)
            if respuesta.status_code == 200:
                datos = respuesta.json()

                #Diccionario con Nombre e ID
                pokemon_con_ID = []
                for p in datos["pokemon"]:
                    url = p["pokemon"]["url"]

                    pokemon_id = url.split('/')[-2] #.split('/'): Rompe el texto cada vez que encuentra una /. [-2]: Como la URL termina en una barra (/), el último elemento está vacío y el penúltimo . (-2) es el número que necesitamos.
                    pokemon_con_ID.append({
                        "name": p["pokemon"]["name"],
                        "id": pokemon_id
                    })
                lista_por_tipo = {
                        "nombre_tipo": tipo_elegido,
                        "pokemon_list": pokemon_con_ID,
                    }
            else:
                error= "¡ERROR! Tipo no encontrado :("

    return render_template("index.html", pokemon=datos_pokemon, tipo_data=lista_por_tipo, error=error)


if __name__ == "__main__":
    app.run(debug=True)  





