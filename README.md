# Base project for django
this is a bare setup for a new django project, this is based on [this](https://github.com/amiravtar/django-base-project) project

# Running the project
## Docker
### Setup the environment variables
There are 2 sample env files, .env.prod and .env.development. Copy/Rename one of them to .env and change the desired values

use the debug or prod docker compose files

```bash
make create-secret-key # use this to create a djang random key, also you can use your own
```

### Run the project
```bash
docker compose -f docker-compose.debug.yaml up
```