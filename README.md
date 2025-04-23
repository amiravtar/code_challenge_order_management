# About
This is a code challenge using Django/Drf/Postgres/docker
There are 2 models (User and Order)

Authentication is JWT tokens (Access token and Refresh token)

Swagger is used to document the apis

there are some default users and groups added by django management commnads

you can run the production docker compose in 3 steps:
- copy/rename .env.prod to .env
- using make create-secret-key (if you have windows or dont want to use make, get a random string from anywhere) and set the key in .env file (SECRET_KEY)
- docker compose -f docker-compose.yaml up 
	- ocker compose -f docker-compose.yaml run --rm test (for running the tests)

for more details read blow
# Base project for django
this is a bare setup for a new django project, this is based on [this](https://github.com/amiravtar/django-base-project) project

# Running the project
Note for production you can just rename the .env.prod and run the project (all of the configs are there but some of them are not good on production, you might want to change them)
## Development
### File permissions for development (important)
Use UID=1000 GID=1000 (use your own users ids) in env file to make the container user id same as the host

## Setup the environment variables
There are 2 sample env files, .env.prod and .env.development. Copy/Rename one of them to .env and change the desired values

use the debug or prod docker compose files
Note: Install the requirements first
```bash
pip install -r requirements-dev.txt
```

```bash
make create-secret-key # use this to create a django random key, also you can use your own
```
also set the ALLOWED_HOSTS if you are running on a remote server
sample:
```bash
ALLOWED_HOSTS=localhost,172.17.17.10
```
## Cors
**you can ignore this (not good on production)**
**Optional** change the CORS_ALLOW_ALL_ORIGINS in the env file for prod (remove it or make it false), use CORS_ALLOWED_ORIGINS
## Docker
### Run the project
```bash
docker compose -f docker-compose.debug.yaml up # development

docker compose -f docker-compose.yaml up # production, less work needed, recommended
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
docker compose -f docker-compose.yaml run -e WAIT=True -p 5678:5678 --rm test
# you can use both docker compose files to run tests, they both use the same dockerfile
```
and then attach using your IDE


# Default data
There are 2 defualt groups, admin and normal_user
there is also 2 default users (created by management commands)

user: normaluser
pass: normal123

user: admin
pass: admin123

also there is a superuser created (enabled by defautl in env files)

user: amir
pass: 123

# Docs

# Swagger
use /swagger for the swagger docs
you can also use the authorization in swagger (jwt)
**Note**: Use Bearer <Token> in the field, not the empty token