import requests

api_key = '7ebbb702-ea0b-4182-a06d-4bef4a6661fa'

# Coordenadas de Santiago y Ovalle
santiago_coords = '-33.45694, -70.64827'  # Latitud, Longitud de Santiago
ovalle_coords = '-30.60106, -71.19901'    # Latitud, Longitud de Ovalle

url = f'https://graphhopper.com/api/1/route?point={santiago_coords}&point={ovalle_coords}&vehicle=car&locale=es&key={api_key}'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    distance_meters = data['paths'][0]['distance']
    distance_kilometers = distance_meters / 1000
    print(f'La distancia entre Santiago y Ovalle es de aproximadamente {distance_kilometers:.2f} km')
else:
    print('Error en la solicitud:', response.status_code, response.text)
