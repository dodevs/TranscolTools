import requests
import json

ceturbUrlBase = "https://sistemas.es.gov.br/webservices/ceturb/onibus/api/"

# Funcao para obter itinerario
def get_itineraio(linha):
    response = requests.get(ceturbUrlBase+'BuscaItinerarios/'+linha)
    #Parsea o resultado em um json
    parsed_response = json.loads(response.text)

    return parsed_response

def main():
    itinerario = get_itineraio("843")
    print(itinerario)

if __name__ == "__main__":
    main()
