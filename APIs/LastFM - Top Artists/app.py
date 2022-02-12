import json
import requests
import requests_cache
import credentials
import time
from IPython.core.display import clear_output
requests_cache.install_cache()


def pretty_json(j):
    # Create human readable strong from json obj
    pj = json.dumps(j, sort_keys=True, indent=4)
    print(pj)


def lastfm_request(payload):
    # Define headers and url
    headers = {'user-agent': credentials.api_user}
    url = 'http://ws.audioscrobbler.com/2.0/'

    # Add api key and format
    payload['api_key'] = credentials.api_key
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response


# Begin main program
responses = []
page = 1
total_pages = 99999 # Updated after first request

while page <= total_pages:
    payload = {
        'method': 'chart.gettopartists',
        'limit': 500,
        'page': page
    }

    # Print some status output
    print('Requesting page {}/{}'.format(page, total_pages))
    # Clear output to make things neater
    # clear_output(wait=True)

    # API call
    response = lastfm_request(payload)

    # Upon error, print and break
    if response.status_code != 200:
        print(response.text)
        break

    # Extract pagination info
    page = int(
        response.json()['artists']['@attr']['page']
    )
    total_pages = int(
        response.json()['artists']['@attr']['totalPages']
    )

    # Add response to list
    responses.append(response)

    # If cached continue, else wait
    if not getattr(response, 'from_cache', False):
        time.sleep(.25)

    # Increment page number
    page += 1

