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
    response = requests.get('https://zenodo.org/api/records', params=params, headers=headers)
    response.raise_for_status()
    data = response.json()[0]['metadata']
    return data['doi'], data['version'], data['publication_date']


if __name__ == '__main__':
    with open('CITATION.cff', 'r') as file:
        citation = yaml.safe_load(file)
    citation['doi'], citation['version'],  citation['date-released'] = get_infos()
    with open('citation.cff', 'w') as file:
        yaml.dump(citation, file, sort_keys=False, default_flow_style=False)
