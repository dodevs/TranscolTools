import json
import time
import urllib
import urllib2

def timezone(lat, lng, timestamp):
    maps_key = 'API key'
    timezone_base_url = 'https://maps.googleapis.com/maps/api/timezone/json'

    # Isso junta as partes da url em uma string
    url = timezone_base_url + '?' + urllib.urlencode({
        'location': "%s,%s" % (lat, lng),
        'timestamp': timestamp,
        'key': maps_key,
    })

    current_delay = 0.1  # Define o tempo de delay inicial em 100ms.
    max_delay = 3600  # Define o tempo maximo de delay em 1 hora.

    while True:
        try:
            # Pega a response da url
            response = str(urllib2.urlopen(url).read())
        except IOError:
            pass  # Fall through to the retry loop.
        else:
            # If we didn't get an IOError then parse the result.
            result = json.loads(response.replace('\\n', ''))
            if result['status'] == 'OK':
                return result['timeZoneId']
            elif result['status'] != 'UNKNOWN_ERROR':
                # Many API errors cannot be fixed by a retry, e.g. INVALID_REQUEST or
                # ZERO_RESULTS. There is no point retrying these requests.
                raise Exception(result['error_message'])

        if current_delay > max_delay:
            raise Exception('Too many retry attempts.')
        print('Waiting', current_delay, 'seconds before retrying.')
        time.sleep(current_delay)
        current_delay *= 2  # Increase the delay each time we retry.

tz = timezone(39.6034810, -119.6822510, 1331161200)
print('Timezone:', tz)
