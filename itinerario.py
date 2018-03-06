import requests
import json

ceturbUrlBase = "https://sistemas.es.gov.br/webservices/ceturb/onibus/api/"
#getLinhas = "ConsultaLinha/?Tipo_Linha=T"  # Params T e S


def getLinhas(tipo):
    linhasBuffer = None
    with open('linhas.json', 'r+t') as linhasFile:
        try:
            linhasBuffer = json.loads(linhasFile.read())
        except json.JSONDecodeError:
            linhasResponse = requests.get(ceturbUrlBase + "/ConsultaLinha/?Tipo_Linha=" + tipo)
            linhasBuffer = json.loads(linhasResponse.text)
            linhasFile.write(json.dumps(linhasBuffer))

        linhasFile.close()

    return linhasBuffer


def getRota(itinerario, sentido):
    # Pega somente a rota do sentido escolhido
    itinerarioI = [waypoint['Desc_Via'].strip() for waypoint in itinerario if waypoint['Sentido'] == sentido]
    itinerarioIOrigin = itinerarioI[0]  # Ponto de origem
    itinerarioIDestination = itinerarioI[-1]  # Ponto de destino
    itinerarioIWaypoints = [item for item in itinerarioI[1:-2]]  # Pontos de passagem

    return [itinerarioIOrigin, itinerarioIWaypoints, itinerarioIDestination]


# Funcao para obter itinerario
def getItinerario(linha):
    rotasBuffer = None
    rotasFile = open('rotas.json', 'r+t')
    try:
        rotasBuffer = json.loads(rotasFile.read())
        if linha in rotasBuffer.keys():
            return rotasBuffer[linha]
        else:
            itinerarioResponse = requests.get(ceturbUrlBase + 'BuscaItinerarios/' + linha)
            parsedRota = json.dumps({
                'I': getRota(itinerarioResponse.text, 'I'),
                'V': getRota(itinerarioResponse.text, 'V')
            })
            rotasBuffer[linha] = parsedRota
            rotasFile.write(rotasBuffer)
            rotasFile.close()

            return parsedRota

    except json.JSONDecodeError:
        itinerarioResponse = requests.get(ceturbUrlBase + 'BuscaItinerarios/' + linha)
        parsedResponse = json.loads(itinerarioResponse.text)

        rotasBuffer = dict({})[linha] = json.dumps({
            'I': getRota(parsedResponse, 'I'),
            'V': getRota(parsedResponse, 'V')
        })

        rotasFile.write(rotasBuffer)
        return rotasBuffer[linha]


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

    return mapsResponse.url


def main():
    #print(getLinhas('T'))
    itinerario = getItinerario("860")
    #print(itinerario, 'I')


if __name__ == "__main__":
    main()
