import requests
import json

ceturbUrlBase = "https://sistemas.es.gov.br/webservices/ceturb/onibus/api/"

def get_rota(itinerario, sentido):
    # Pega somente a rota do sentido escolhido
    itinerarioI = [waypoint['Desc_Via'].strip() for waypoint in itinerario if waypoint['Sentido'] == sentido]
    itinerarioIOrigin = itinerarioI[0]  # Ponto de origem
    itinerarioIDestination = itinerarioI[-1]  # Ponto de destino
    itinerarioIWaypoints = [item for item in itinerarioI[1:-2]]  # Pontos de passagem

    return [itinerarioIOrigin, itinerarioIWaypoints, itinerarioIDestination]

# Funcao para obter itinerario
def get_itineraio(linha):
    response = requests.get(ceturbUrlBase+'BuscaItinerarios/'+linha)
    #Parsea o resultado em um json
    parsedResponse = json.loads(response.text)

    return {
        'I': get_rota(parsedResponse, 'I'),
        'V': get_rota(parsedResponse, 'V')
    }

def main():
    itinerario = get_itineraio("843")
    print(itinerario)

if __name__ == "__main__":
    main()
