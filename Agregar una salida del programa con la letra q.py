import requests
from geopy.geocoders import Nominatim

api_key = '7ebbb702-ea0b-4182-a06d-4bef4a6661fa'

def obtener_coordenadas(ciudad):
    geolocator = Nominatim(user_agent="distance_calculator")
    location = geolocator.geocode(ciudad)
    if location:
        return f'{location.latitude:.2f},{location.longitude:.2f}'
    else:
        print(f"No se pudo obtener coordenadas para {ciudad}")
        return None

def convertir_tiempo(ms):
    seconds = ms // 1000
    minutes = seconds // 60
    hours = minutes // 60
    seconds = seconds % 60
    minutes = minutes % 60
    return hours, minutes, seconds

def obtener_narrativa_ruta(data):
    narrative = data['paths'][0]['instructions']
    return narrative

while True:
    opcion = input("Para calcular una ruta, ingrese 's'. Para salir, ingrese 'q': ").lower()

    if opcion == 'q':
        print("Saliendo del programa...")
        break
    elif opcion == 's':
        # Solicitar Ciudad de Origen y Ciudad de Destino
        ciudad_origen = input("Ingrese la Ciudad de Origen: ")
        if ciudad_origen.lower() == 'q':
            print("Saliendo del programa...")
            break
        
        ciudad_destino = input("Ingrese la Ciudad de Destino: ")
        if ciudad_destino.lower() == 'q':
            print("Saliendo del programa...")
            break

        # Obtener coordenadas de las ciudades
        origen_coords = obtener_coordenadas(ciudad_origen)
        destino_coords = obtener_coordenadas(ciudad_destino)

        if origen_coords and destino_coords:
            # URL de la API de GraphHopper
            url = f'https://graphhopper.com/api/1/route?point={origen_coords}&point={destino_coords}&vehicle=car&locale=es&key={api_key}'

            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                distance_meters = data['paths'][0]['distance']
                distance_kilometers = distance_meters / 1000
                
                time_ms = data['paths'][0]['time']
                hours, minutes, seconds = convertir_tiempo(time_ms)

                # Eficiencia de combustible asumida en kilómetros por litro
                eficiencia_combustible = 12
                combustible_requerido = distance_kilometers / eficiencia_combustible

                print(f'La distancia entre {ciudad_origen} y {ciudad_destino} es de aproximadamente {distance_kilometers:.2f} km')
                print(f'La duración estimada del viaje es de {hours:02d} horas, {minutes:02d} minutos y {seconds:02d} segundos')
                print(f'El combustible requerido para el viaje es de aproximadamente {combustible_requerido:.2f} litros')

                # Obtener narrativa de la ruta
                narrative = obtener_narrativa_ruta(data)
                print("\nNarrativa del Viaje:")
                print(narrative)
            else:
                print('Error en la solicitud:', response.status_code, response.text)
        else:
            print("No se pudo calcular la distancia debido a problemas con las coordenadas.")
    else:
        print("Opción no válida. Por favor, ingrese 's' para calcular una ruta o 'q' para salir.")

