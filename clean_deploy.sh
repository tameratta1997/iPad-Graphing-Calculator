#!/bin/bash
HOST="72.61.95.112"
USER="root"
REMOTE_DIR="/var/www/gold_app"
LOCAL_ZIP="/Users/tamerelwakeel/Documents/Python_Projects/Python_Diploma/gold-price-complete-v9.zip"

echo "========================================"
echo "      SaghaLive CLEAN RE-DEPLOY (v9)"
echo "========================================"

echo "1. Uploading verified local version..."
scp $LOCAL_ZIP $USER@$HOST:$REMOTE_DIR/

echo "2. Cleaning server & Installing new version..."
ssh $USER@$HOST "cd $REMOTE_DIR && \
    echo 'Stopping service...' && \
    systemctl stop gold_app && \
    echo 'Removing old application files (keeping venv)...' && \
    rm -rf static templates app.py wsgi.py requirements.txt && \
    echo 'Unzipping fresh package...' && \
    unzip -o gold-price-complete-v9.zip && \
    cp -r gold-price-egypt/* . && \
    rm -rf gold-price-egypt && \
    echo 'Clean install complete. Restarting service...' && \
    systemctl start gold_app"

echo "========================================"
echo "SUCCESS! Clean Deployment Finished."
echo "Please clear your browser cache and check https://saghalive.com"
echo "========================================"
