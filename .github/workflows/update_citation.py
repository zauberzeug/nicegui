import os
import sys
from pathlib import Path
from typing import Tuple

import requests
import yaml


def get_infos() -> Tuple[str, str, str]:
    """
    Retrieves information from Zenodo API about the most recent publication of 'nicegui'.

    Returns:
        A tuple containing the following information:
        - DOI (Digital Object Identifier) of the publication.
        - Version of the publication.
        - Publication date of the publication.

    Raises:
        Exception: If there is an error while retrieving the Zenodo information.

    Usage:
        - Ensure that the 'ZENODO_TOKEN' environment variable is set with the access token for Zenodo API.
        - Call this function to retrieve the information about the most recent publication of 'nicegui'.
    """
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
    data = response.json()
    metadata = data['hits']['hits'][0]['metadata']
    return str(metadata['doi']), str(metadata['version']), str(metadata['publication_date'])


if __name__ == '__main__':
    path = Path('CITATION.cff')
    citation = yaml.safe_load(path.read_text())
    citation['doi'], citation['version'], citation['date-released'] = get_infos()
    path.write_text(yaml.dump(citation, sort_keys=False, default_flow_style=False))
