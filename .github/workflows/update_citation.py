import os
import sys
from pathlib import Path
from typing import Tuple

import requests
import yaml


def get_infos() -> Tuple[str]:
    headers = {
        'Accept': 'application/json',
    }
    params = {
        'access_token': os.environ['ZENODO_TOKEN'],
        'q': 'nicegui',
        'sort': 'mostrecent',
        'status': 'published',
    }
    try:
        response = requests.get('https://zenodo.org/api/records', params=params, headers=headers, timeout=5)
        response.raise_for_status()
    # Hide all error details to avoid leaking the token
    except Exception:
        print('Error while getting the Zenodo infos')
        sys.exit(1)
    data = response.json()[0]['metadata']
    return data['doi'], data['version'], data['publication_date']


if __name__ == '__main__':
    path = Path('CITATION.cff')
    citation = yaml.safe_load(path.read_text())
    citation['doi'], citation['version'], citation['date-released'] = get_infos()
    path.write_text(yaml.dump(citation, sort_keys=False, default_flow_style=False))
