#!/usr/bin/env python3
import argparse
import re
import sys
from typing import Dict, List

import requests

BASE_URL = 'https://api.github.com/repos/zauberzeug/nicegui'

parser = argparse.ArgumentParser(description='Fetch the content of a milestone from a GitHub repo.')
parser.add_argument('milestone_title', help='Title of the milestone to fetch.')
args = parser.parse_args()
milestone_title: str = args.milestone_title

page = 0
while True:
    page += 1
    response = requests.get(f'{BASE_URL}/milestones?state=all&page={page}&per_page=100', timeout=5)
    milestones = response.json()
    if not milestones:
        print(f'Milestone "{milestone_title}" not found!')
        sys.exit(1)
    matching = [m for m in milestones if m['title'] == milestone_title]
    if matching:
        milestone_number = matching[0]['number']
        break


def link(number: int) -> str:
    # https://stackoverflow.com/a/71309268/3419103
    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'
    return escape_mask.format('', f'https://github.com/zauberzeug/nicegui/issues/{number}', f'#{number}')


issues = requests.get(f'{BASE_URL}/issues?milestone={milestone_number}&state=all', timeout=5).json()
notes: Dict[str, List[str]] = {
    'New features and enhancements': [],
    'Bugfixes': [],
    'Documentation': [],
    'Dependencies': [],
    'Others': [],
}
for issue in issues:
    title: str = issue['title']
    user: str = issue['user']['login'].replace('[bot]', '')
    body: str = issue['body'] or ''
    labels: List[str] = [label['name'] for label in issue['labels']]
    if user == 'dependabot':
        number_patterns = []
    else:
        number_patterns = [r'#(\d+)', r'https://github.com/zauberzeug/nicegui/(?:issues|discussions|pulls)/(\d+)']
    numbers = [issue['number']] + [int(match) for pattern in number_patterns for match in re.findall(pattern, body)]
    numbers_str = ', '.join(link(number) for number in sorted(numbers))
    note = f'{title.strip()} ({numbers_str} by @{user})'
    if 'bug' in labels:
        notes['Bugfixes'].append(note)
    elif 'enhancement' in labels:
        notes['New features and enhancements'].append(note)
    elif 'documentation' in labels:
        notes['Documentation'].append(note)
    elif 'dependencies' in labels:
        notes['Dependencies'].append(note)
    else:
        notes['Others'].append(note)

for title, lines in notes.items():
    if not lines:
        continue
    print(f'### {title}')
    print()
    for line in lines:
        print(f'- {line}')
    print()
