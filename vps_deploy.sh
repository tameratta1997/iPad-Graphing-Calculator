#!/bin/bash

# 1. System Updates & Dependencies
echo "Installing system dependencies..."
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y python3-pip python3-venv nginx unzip

# 2. Setup Directory
echo "Setting up project directory..."
mkdir -p /var/www/gold_app
# Move uploaded zip to target if not already there
if [ -f "/root/gold-price-app-deploy-vps.zip" ]; then
    mv /root/gold-price-app-deploy-vps.zip /var/www/gold_app/
fi

cd /var/www/gold_app

# 3. Unzip
echo "Unzipping application..."
unzip -o gold-price-app-deploy-vps.zip
# If it unzips into a subfolder 'gold-price-egypt', move contents up
if [ -d "gold-price-egypt" ]; then
    mv gold-price-egypt/* .
    rm -rf gold-price-egypt
fi

# 4. Python Environment
echo "Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Systemd Service
echo "Creating Gunicorn service..."
cat > /etc/systemd/system/gold_app.service <<EOF
[Unit]
Description=Gunicorn instance to serve gold_app
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/gold_app
Environment="PATH=/var/www/gold_app/venv/bin"
ExecStart=/var/www/gold_app/venv/bin/gunicorn --workers 3 --bind unix:gold_app.sock -m 007 wsgi:application

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl restart gold_app
systemctl enable gold_app

# 6. Nginx Configuration
echo "Configuring Nginx..."
cat > /etc/nginx/sites-available/gold_app <<EOF
server {
    listen 80;
    server_name saghalive.com www.saghalive.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/gold_app/gold_app.sock;
    }
}
EOF

# Enable site
rm -f /etc/nginx/sites-enabled/default
ln -sf /etc/nginx/sites-available/gold_app /etc/nginx/sites-enabled
nginx -t
systemctl restart nginx

echo "--------------------------------------------------"
echo "Deployment Complete! Visit http://saghalive.com"
echo "--------------------------------------------------"
