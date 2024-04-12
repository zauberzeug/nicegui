
fly deploy --wait-timeout 360 --build-arg VERSION=$(git describe --abbrev=0 --tags --match 'v*' 2>/dev/null | sed 's/^v//' || echo '0.0.0')
