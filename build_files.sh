# Ensure pip is installed and accessible
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip

# Install dependencies
python3 -m pip install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --noinput