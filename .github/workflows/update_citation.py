import yaml
import os
from datetime import datetime

with open('CITATION.cff', 'r') as f:
    citation = yaml.safe_load(f)

citation['version'] = os.environ['GITHUB_REF'].split('/')[-1]
citation['date-released'] = datetime.utcnow().strftime('%Y-%m-%d')
# citation['doi'] = 'doi base (not ready yet)' + os.environ['GITHUB_REF'].split('/')[-1]

with open('CITATION.cff', 'w') as f:
    yaml.dump(citation, f, sort_keys=False, default_flow_style=False)

os.system('git add CITATION.cff')
os.system('git commit -m "Update CITATION.cff for release"')
os.system('git push')
