import sys
import yaml
import os
from datetime import datetime


import os
import requests
import yaml


def get_infos() -> str:
    headers = {'Accept': 'application/json'}
    params = {
        'access_token': os.environ['ZENODO_TOKEN'],
        'q': 'nicegui', 'sort': 'mostrecent', 'status': 'published'
    }
    try:
        response = requests.get('https://zenodo.org/api/records', params=params, headers=headers)
        response.raise_for_status()
    # Hide all error details to avoid leaking the token
    except Exception:
        print('Error while getting the Zenodo infos')
        sys.exit(1)
    data = response.json()[0]['metadata']
    return data['doi'], data['version'], data['publication_date']


if __name__ == '__main__':
    with open('CITATION.cff', 'r') as file:
        citation = yaml.safe_load(file)
    citation['doi'], citation['version'],  citation['date-released'] = get_infos()
    with open('CITATION.cff', 'w') as file:
        yaml.dump(citation, file, sort_keys=False, default_flow_style=False)
