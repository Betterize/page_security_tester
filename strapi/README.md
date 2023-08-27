# .env

All below variables have to be placed in .env file in service main directory (same level as this README file).
All needed variables with example values. Make sure that this values match with that from main .env file.

```
HOST=0.0.0.0
PORT=1337
APP_NAME=page_security_scan
STRAPI_HOST_PORT=127.0.0.1:1337

APP_KEYS=27ppYghTvIoTbCuCWiP37w==,HlzM2cOG/wy9W19W/vsepw==,qO5wsqx5fR4+aMcVC3K3qw==,opduN5fyCuuD2BRc+4+Cog==
API_TOKEN_SALT=6bdIWQL8H+BIjpw0NJQMXg==
ADMIN_JWT_SECRET=2Qwq41TkOj2gn3SLT53ndg==
TRANSFER_TOKEN_SALT=oIrsOufCnHr5qWleT+IkFQ==
JWT_SECRET=eJXywF4dePDmaMdGWXxVSg==

# db config
DATABASE_CLIENT=postgres
DATABASE_HOST=db
DATABASE_USERNAME=admin
DATABASE_PASSWORD=admin
DATABASE_NAME=some_db
DATABASE_PORT=5432
DATABASE_HOST_PORT=127.0.0.1:5432


REDIS_HOST=redis
REDIS_PORT=6379
REDIS_QUEUE_NAME=example
```

Below variables need to be configured for proper working email functionalities.

```
EMAIL_FROM=from_address@example.com
EMAIL_ADDRESS=from_address@example.com
EMAIL_PASSWORD=secret_password
EMAIL_ADMINISTRATOR=admin@example.com
```
