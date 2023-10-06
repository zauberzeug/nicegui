#!/usr/bin/env bash

fly scale count app=2  --region fra -y
fly scale count app=2  --region iad -y
fly scale count app=1  --region jnb -y
fly scale count app=2  --region lax -y
fly scale count app=2  --region lhr -y
fly scale count app=1  --region bom -y
fly scale count app=1  --region mad -y
fly scale count app=2  --region mia -y
fly scale count app=2  --region nrt -y
fly scale count app=2  --region sea -y
fly scale count app=2  --region sin -y