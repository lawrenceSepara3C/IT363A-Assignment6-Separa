#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install all dependencies from your text file
pip install -r requirements.txt

# 2. Bundle up static assets for production layout (WhiteNoise handles this)
python manage.py collectstatic --no-input

# 3. Apply any fresh structural changes to the online database automatically
python manage.py migrate