#!/usr/bin/env bash

<<<<<<< Updated upstream
fly scale count app=5  --region fra -y
fly scale count app=3  --region iad -y
fly scale count app=1  --region jnb -y
fly scale count app=3  --region lax -y
fly scale count app=4  --region lhr -y
fly scale count app=3  --region cdg -y
fly scale count app=2  --region bom -y
fly scale count app=2  --region mad -y
fly scale count app=3  --region mia -y
fly scale count app=3  --region nrt -y
fly scale count app=3  --region sea -y
fly scale count app=3  --region sin -y
=======
fly scale count app=1  --region fra -y # Frankfurt, Germany
fly scale count app=1  --region ams -y # Amsterdam, Netherlands
fly scale count app=1  --region mad -y # Madrid, Spain
fly scale count app=1  --region cdg -y # Paris, France
fly scale count app=1  --region lhr -y # London, England (UK)

fly scale count app=1  --region iad -y # Washington DC, Virginia (US)
fly scale count app=1  --region sjc -y # San Jose, California (US)
fly scale count app=1  --region lax -y # Los Angeles, California (US)
fly scale count app=1  --region mia -y # Miami, Florida (US)
fly scale count app=1  --region sea -y # Seattle, Washington (US)

fly scale count app=1  --region jnb -y # Johannesburg, South Africa

fly scale count app=1  --region bom -y # Mumbai, India
fly scale count app=1  --region nrt -y # Tokyo, Japan
fly scale count app=1  --region sin -y # Singapor
>>>>>>> Stashed changes
