#!/bin/bash
HOST="72.61.95.112"
USER="root"
REMOTE_DIR="/var/www/gold_app"
LOCAL_ZIP="/Users/tamerelwakeel/Documents/Python_Projects/Python_Diploma/latest_deploy.zip"

# Check if package exists
if [ ! -f "$LOCAL_ZIP" ]; then
    echo "Error: latest_deploy.zip not found! Run ./package_app.sh first."
    exit 1
fi

echo "========================================"
echo "      SaghaLive CLEAN INSTALLATION"
echo "========================================"

echo "1. Uploading full application package..."
scp $LOCAL_ZIP $USER@$HOST:$REMOTE_DIR/

echo "2. Performing Clean Install on Server..."
# Logic: STOP service -> REMOVE code files -> UNZIP new code -> START service
ssh $USER@$HOST "cd $REMOTE_DIR && \
    echo '[Server] Stopping gold_app service...' && \
    systemctl stop gold_app && \
    echo '[Server] Wiping old application files...' && \
    rm -rf static templates app.py wsgi.py requirements.txt gold-price-egypt && \
    echo '[Server] Extracting new package...' && \
    unzip -o latest_deploy.zip > /dev/null && \
    cp -a gold-price-egypt/. . && \
    rm -rf gold-price-egypt && \
    echo '[Server] Installing dependencies...' && \
    /var/www/gold_app/venv/bin/pip install -r requirements.txt && \
    echo '[Server] Restarting gold_app service...' && \
    systemctl start gold_app"

echo "========================================"
echo "SUCCESS! Clean Installation Complete."
echo "Active @ https://saghalive.com"
echo "========================================"
