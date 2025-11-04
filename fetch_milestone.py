#!/usr/bin/env python3
import argparse
import re
import sys

import httpx

BASE_URL = 'https://api.github.com/repos/zauberzeug/nicegui'

parser = argparse.ArgumentParser(description='Fetch the content of a milestone from a GitHub repo.')
parser.add_argument('milestone_title', help='Title of the milestone to fetch.')
parser.add_argument('--check', action='store_true', help='Check if the description mentions all issues.')
args = parser.parse_args()
milestone_title: str = args.milestone_title
check: bool = args.check

page = 0
while True:
    page += 1
    response = httpx.get(f'{BASE_URL}/milestones?state=all&page={page}&per_page=100', timeout=5)
    milestones = response.json()
    if not milestones:
        print(f'Milestone "{milestone_title}" not found!')
        sys.exit(1)
    matching = [m for m in milestones if m['title'] == milestone_title]
    if matching:
        milestone_number = matching[0]['number']
        milestone_description = matching[0]['description']
        break


def link(number: int) -> str:
    # https://stackoverflow.com/a/71309268/3419103
    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'
    return escape_mask.format('', f'https://github.com/zauberzeug/nicegui/issues/{number}', f'#{number}')


issues = []
page = 0
while True:
    page += 1
    response = httpx.get(f'{BASE_URL}/issues?milestone={milestone_number}&state=all&page={page}', timeout=5)
    page_issues = response.json()
    if not page_issues:
        break
    issues.extend(page_issues)

notes: dict[str, list[str]] = {
    'New features and enhancements': [],
    'Bugfixes': [],
    'Documentation': [],
    'Testing': [],
    'Dependencies': [],
    'Infrastructure': [],
    'Others': [],
}
for issue in issues:
    title: str = issue['title']
    user: str = issue['user']['login'].replace('[bot]', '')
    body: str = issue['body'] or ''
    labels: list[str] = [label['name'] for label in issue['labels']]
    if user == 'dependabot':
        number_patterns = []
    else:
        number_patterns = [r'#(\d+)', r'https://github.com/zauberzeug/nicegui/(?:issues|discussions|pulls)/(\d+)']
    numbers = [issue['number']] + [int(match) for pattern in number_patterns for match in re.findall(pattern, body)]
    numbers_str = ', '.join(link(number) for number in sorted(numbers))
    note = f'{title.strip()} ({numbers_str} by @{user})'
    if 'bug' in labels:
        notes['Bugfixes'].append(note)
    elif 'feature' in labels:
        notes['New features and enhancements'].append(note)
    elif 'documentation' in labels:
        notes['Documentation'].append(note)
    elif 'testing' in labels:
        notes['Testing'].append(note)
    elif 'dependencies' in labels:
        notes['Dependencies'].append(note)
    elif 'infrastructure' in labels:
        notes['Infrastructure'].append(note)
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

if check:
    for issue in issues:
        if f'#{issue["number"]}' not in milestone_description:
            print(f'Issue {link(issue["number"])} is not mentioned in the milestone description')
