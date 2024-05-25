import requests
from geopy.geocoders import Nominatim

api_key = '7ebbb702-ea0b-4182-a06d-4bef4a6661fa'

def obtener_coordenadas(ciudad):
    geolocator = Nominatim(user_agent="distance_calculator")
    location = geolocator.geocode(ciudad)
    if location:
        return f'{location.latitude},{location.longitude}'
    else:
        print(f"No se pudo obtener coordenadas para {ciudad}")
        return None
#Función para convertir milisegundos a horas, minutos y segundos
def convertir_tiempo(ms):
    seconds = ms // 1000
    minutes = seconds // 60
    hours = minutes // 60
    seconds = seconds % 60
    minutes = minutes % 60
    return hours, minutes, seconds
#Solicitar Ciudad de Origen y Ciudad de Destino
ciudad_origen = input("Ingrese la Ciudad de Origen: ")
ciudad_destino = input("Ingrese la Ciudad de Destino: ")
#Obtener coordenadas de las ciudades
origen_coords = obtener_coordenadas(ciudad_origen)
destino_coords = obtener_coordenadas(ciudad_destino)

if origen_coords and destino_coords:
    url = f'https://graphhopper.com/api/1/route?point={origen_coords}&point={destino_coords}&vehicle=car&locale=es&key={api_key}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        #Extraer la distancia de la respuesta (en metros)
        distance_meters = data['paths'][0]['distance']
        #Convertir la distancia a kilómetros
        distance_kilometers = distance_meters / 1000

        #Extraer la duración del viaje (en milisegundos)
        time_ms = data['paths'][0]['time']
        hours, minutes, seconds = convertir_tiempo(time_ms)

        print(f'La distancia entre {ciudad_origen} y {ciudad_destino} es de aproximadamente {distance_kilometers:.2f} km')
        print(f'La duración estimada del viaje es de {hours} horas, {minutes} minutos y {seconds} segundos')
    else:
        print('Error en la solicitud:', response.status_code, response.text)
else:
    print("No se pudo calcular la distancia debido a problemas con las coordenadas.")
