#!/usr/bin/env bash

fly scale count app=1  --region yul -y # Montreal, Quebec (Canada)

fly scale count app=3  --region iad -y # Washington DC, Virginia (US)
fly scale count app=1  --region sjc -y # San Jose, California (US)
fly scale count app=2  --region lax -y # Los Angeles, California (US)
fly scale count app=3  --region mia -y # Miami, Florida (US)
fly scale count app=1  --region sea -y # Seattle, Washington (US)

fly scale count app=5  --region fra -y # Frankfurt, Germany
fly scale count app=2  --region ams -y # Amsterdam, Netherlands
fly scale count app=1  --region mad -y # Madrid, Spain
fly scale count app=1  --region cdg -y # Paris, France
fly scale count app=2  --region lhr -y # London, England (UK)
fly scale count app=1  --region otp -y # Bucharest, Romania

fly scale count app=1  --region jnb -y # Johannesburg, South Africa

fly scale count app=1  --region bom -y # Mumbai, India
fly scale count app=3  --region nrt -y # Tokyo, Japan
fly scale count app=1  --region sin -y # Singapore
fly scale count app=4  --region hkg -y # Hong Kong

fly scale count app=1  --region syd -y # Sydney, Australia

fly scale count app=1  --region gru -y # Sao Paulo, Brazil
