#!/bin/sh
if [ "$TESTING" = "False" ]; then
    echo "Waiting for PostgreSQL..."
    ./docker/wait-for-it.sh postgres:5432 --timeout=30 --strict -- echo "PostgreSQL is up"

    echo "Starting Django app..."
    exec "$@"
fi

# Start application setup
echo "Running migrations..."
python3 manage.py migrate

echo "Loading defualt groups..."
python3 manage.py load_default_groups

echo "Loading defualt users..."
python3 manage.py load_default_users

# Check if a env variable called WORKERS exists
if [ -n "$WORKERS" ]; then
    WORKERS=$WORKERS
else
    WORKERS=4
fi
if [ "$TESTING" = "True" ]; then
    if [ -n "$TEST_APP" ]; then
        # Run tests only on the specified app if TEST_APP is set
        if [ "$WAIT" = "True" ]; then
            python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m pytest "$TEST_APP" -v
        else
            pytest "$TEST_APP" -v
        fi
    else
        # Run tests on the entire project if TEST_APP is not set
        if [ "$WAIT" = "True" ]; then
            python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m pytest -v
        else
            pytest -v -n "$WORKERS" --cov=. --cov-report=html
        fi
    fi
    exit 0
fi
# Pre-run commands
if [ "$CREATE_SUPERUSER" = "True" ]; then
    echo "Creating superuser..."
    python3 manage.py createsuperuser --noinput
fi

if [ "$COLLECT_STATIC" = "True" ]; then
    echo "Collecting static files..."
    python3 manage.py collectstatic --noinput
fi

# Check if DEBUG environment variable is set to true
if [ "$DEBUG" = "True" ]; then
    # Run Gunicorn with fewer workers for easier debugging
    exec gunicorn config.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 1 \
        --reload \
        --log-level info
else
    # Run Gunicorn normally
    exec gunicorn config.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers $WORKERS
fi
