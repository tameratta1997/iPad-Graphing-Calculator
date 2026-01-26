#!/bin/bash
# 1. Cleaner: Remove old zip
rm -f latest_deploy.zip

# 2. Packager: Create a full package of the application
echo "Packaging application..."
zip -r latest_deploy.zip gold-price-egypt/app.py gold-price-egypt/wsgi.py gold-price-egypt/requirements.txt gold-price-egypt/.env gold-price-egypt/static gold-price-egypt/templates

echo "Package created: latest_deploy.zip"
