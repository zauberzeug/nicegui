#!/usr/bin/env bash

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