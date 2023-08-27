## .env

List of variable with example values

```
APP_NAME=page_security_scan
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_QUEUE_NAME=example
STRAPI_BASE_URL=http://strapi:1337
LOG_LEVEL=INFO
```

Below variable should be setup according to main README first run instructions.

```
STRAPI_TOKEN=
```

## Poetry

Poetry is used to manage this service.

To update `requirements.txt` needed while docker run use below line:

```
poetry export -f requirements.txt --output requirements.txt
```

## Just

To format code or run tests use just. You need to install just on your computer. Example of use:

```
just test-all
```
