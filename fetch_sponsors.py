#!/usr/bin/env python3
import json
import os
import re
from pathlib import Path

import httpx

# NOTE:
# requires a GitHub token with the necessary permissions read:org and read:user
# call with `GITHUB_TOKEN=ghp_XXX ./fetch_sponsors.py`


response = httpx.post(
    'https://api.github.com/graphql',
    json={
        'query': '''
            query($organization: String!) {
                organization(login: $organization) {
                    sponsorshipsAsMaintainer(first: 100, includePrivate: true) {
                        nodes {
                            sponsorEntity {
                                ... on User {
                                    login
                                    name
                                    url
                                    avatarUrl
                                }
                                ... on Organization {
                                    login
                                    name
                                    url
                                    avatarUrl
                                }
                            }
                            tier {
                                monthlyPriceInDollars
                                name
                                isOneTime
                            }
                            createdAt
                        }
                    }
                }
            }
        ''',
        'variables': {'organization': 'zauberzeug'},
    },
    headers={
        'Authorization': f'token {os.getenv("GITHUB_TOKEN")}',
        'Accept': 'application/vnd.github.v3+json',
    },
    timeout=10.0,
)
response.raise_for_status()
data = response.json()
if 'errors' in data:
    raise RuntimeError(f'GitHub API Error: {data["errors"]}')

sponsors = []
for sponsor in data['data']['organization']['sponsorshipsAsMaintainer']['nodes']:
    sponsor_entity = sponsor['sponsorEntity']
    tier = sponsor['tier']
    sponsors.append({
        'login': sponsor_entity['login'],
        'name': sponsor_entity['name'],
        'url': sponsor_entity['url'],
        'avatar_url': sponsor_entity['avatarUrl'],
        'tier_name': tier['name'],
        'tier_amount': tier['monthlyPriceInDollars'],
        'tier_is_one_time': tier['isOneTime'],
        'created_at': sponsor['createdAt'],
    })
sponsors.sort(key=lambda s: s['created_at'])

contributors = []
page = 1
while True:
    contributors_response = httpx.get(
        f'https://api.github.com/repos/zauberzeug/nicegui/contributors?page={page}&per_page=100',
        headers={
            'Authorization': f'token {os.getenv("GITHUB_TOKEN")}',
            'Accept': 'application/vnd.github.v3+json',
        },
        timeout=10.0,
    )
    contributors_response.raise_for_status()
    page_contributors = contributors_response.json()
    if not page_contributors:
        break
    contributors.extend(page_contributors)
    page += 1

print(f'Found {len(sponsors)} sponsors')
print(f'Total contributors for NiceGUI: {len(contributors)}')

Path('website/sponsors.json').write_text(json.dumps({
    'top': [s['login'] for s in sponsors if s['tier_amount'] >= 100 and not s['tier_is_one_time']],
    'total': len(sponsors),
    'contributors': len(contributors),
}, indent=2) + '\n', encoding='utf-8')

sponsor_html = '<p align="center">\n'
for sponsor in sponsors:
    if sponsor['tier_amount'] >= 25 and not sponsor['tier_is_one_time']:
        sponsor_html += f'  <a href="{sponsor["url"]}"><img src="{sponsor["url"]}.png" width="50px" alt="{sponsor["name"]}" /></a>\n'
sponsor_html += '</p>'
readme_path = Path('README.md')
readme_content = readme_path.read_text(encoding='utf-8')
updated_content = re.sub(
    r'<!-- SPONSORS -->.*?<!-- SPONSORS -->',
    f'<!-- SPONSORS -->\n{sponsor_html}\n<!-- SPONSORS -->',
    readme_content,
    flags=re.DOTALL,
)
readme_path.write_text(updated_content, encoding='utf-8')

print('README.md and sponsors.json updated successfully.')
