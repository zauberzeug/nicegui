# Chrome and chromedriver versions must match as per
# https://googlechromelabs.github.io/chrome-for-testing/#stable
export CHROMEVERSION="116.0.5845.96"
export CHROMEURL=https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROMEVERSION}

# SElect chrome platfrom according to TARGETPLATFORM passed from Docker
if [ "$TARGETPLATFORM" = "linux/amd64" ]; then \
    export CHROMEPLATFORM=linux64; \
elif [ "$TARGETPLATFORM" = "linux/arm64" ]; then \
    export CHROMEPLATFORM=mac-arm64; \
else echo "WARNING: platform ($TARGETPLATFORM) might not be supported."; \
fi

# Echo variables for troubleshooting purposes
echo "TARGETPLATFORM: $TARGETPLATFORM"
echo "CHROMEVERSION: $CHROMEVERSION"
echo "CHROMEPLATFORM: $CHROMEPLATFORM"

# Install dependencies
apt-get update && apt-get install -y libglib2.0-0 libnss3 libdrm2 libatk1.0-0 \
    libatk-bridge2.0-0 libcups2 libxkbcommon0 libxcomposite1 libasound2 libxdamage1 \
    libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 \
    && rm -rf /var/lib/apt/lists/*

# Download and install chrome and chromedriver
wget -nv -O /tmp/chrome.zip ${CHROMEURL}/${CHROMEPLATFORM}/chrome-${CHROMEPLATFORM}.zip \
    && mkdir -p /opt/google/chrome \
    && unzip -j /tmp/chrome.zip -d /opt/google/chrome \
    && ln -s /opt/google/chrome/chrome /usr/bin/google-chrome \
    && rm /tmp/chrome.zip

wget -nv -O /tmp/chromedriver.zip ${CHROMEURL}/${CHROMEPLATFORM}/chromedriver-${CHROMEPLATFORM}.zip \
    && mkdir -p /opt/google/chromedriver \
    && unzip -j /tmp/chromedriver.zip -d /opt/google/chromedriver \
    && ln -s /opt/google/chromedriver/chromedriver /usr/bin/chromedriver \
    && rm /tmp/chromedriver.zip

echo "Installed google chrome and chromedriver versions:"
echo `google-chrome --version`
echo `chromedriver --version`