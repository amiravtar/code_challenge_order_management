# Base project for django
this is a bare setup for a new django project, this is based on [this](https://github.com/amiravtar/django-base-project) project

# Running the project
## Setup the environment variables
There are 2 sample env files, .env.prod and .env.development. Copy/Rename one of them to .env and change the desired values

use the debug or prod docker compose files

```bash
make create-secret-key # use this to create a djang random key, also you can use your own
```
## Docker

#### File permissions for development
Use UID=1000 GID=1000 (use your own users ids) in env file to make the container user id same as the host
#### Cors
**Please** change the CORS_ALLOW_ALL_ORIGINS in the env file for prod (remove it or make it false), use CORS_ALLOWED_ORIGINS
### Run the project
```bash
docker compose -f docker-compose.debug.yaml up
```

## Tests
Note: Set the environments first
### Running all of the tests
```bash
docker compose -f docker-compose.debug.yaml run --rm test
```

### Tests only for a spesific file/class/function
Use TEST_APP environment variable
```bash
docker compose -f docker-compose.debug.yaml run -e TEST_APP=./accounts/tests/test_authentication.py --rm test
```

### Debug the tests
Use WAIT env variable
```bash
docker compose -f docker-compose.debug.yaml run -e WAIT=True -p 5678:5678 --rm test
```
and then attach using your IDE
