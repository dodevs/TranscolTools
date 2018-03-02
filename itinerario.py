import requests
import json

ceturbUrlBase = "https://sistemas.es.gov.br/webservices/ceturb/onibus/api/"

def getRota(itinerario, sentido):
    # Pega somente a rota do sentido escolhido
    itinerarioI = [waypoint['Desc_Via'].strip() for waypoint in itinerario if waypoint['Sentido'] == sentido]
    itinerarioIOrigin = itinerarioI[0]  # Ponto de origem
    itinerarioIDestination = itinerarioI[-1]  # Ponto de destino
    itinerarioIWaypoints = [item for item in itinerarioI[1:-2]]  # Pontos de passagem

    return [itinerarioIOrigin, itinerarioIWaypoints, itinerarioIDestination]

# Funcao para obter itinerario
def getItineraio(linha):
    itinerarioResponse = requests.get(ceturbUrlBase+'BuscaItinerarios/'+linha)
    #Parsea o resultado em um json
    parsedResponse = json.loads(itinerarioResponse.text)

    return {
        'I': getRota(parsedResponse, 'I'),
        'V': getRota(parsedResponse, 'V')
    }

def getDirecoes(rota, sentido):
    mapsUrl = "https://maps.googleapis.com/maps/api/directions/json"
    apiKey = open('google_api_key.json', 'rt')
    apiKey = json.loads(apiKey.read())['api_key']
    ''' PARAMETROS DISPONIVEIS
    
    mode: driving (por estradas); walking (caminhada); bicycling (de bike); transit (transporte publico)
    waypoints: optimize:true (Algoritmo do cacheiro viajante)
    region: us, uk, br (Por pais)
    '''
    mapsParametros = {
        'origin': rota[sentido][0],
        'destination': rota[sentido][2],
        'waypoints': "|".join([waypoint for waypoint in rota[sentido][1]]),
        'region': 'br',
        'key': apiKey
    }

    mapsResponse = requests.get(mapsUrl, mapsParametros)

    return mapsResponse.text


def main():
    itinerario = getItineraio("860")
    print(getDirecoes(itinerario, 'I'))

if __name__ == "__main__":
    main()
