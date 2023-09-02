# Page Security Tester

This tool enables users to easily conduct scans of their websites in order to detect potential threats and vulnerabilities. It integrates well-known scanning tools such as Wapiti and Nmap to provide users with comprehensive analysis, and presents aggregated results in a simple and comprehensible manner.

## Services diagram

![image](https://github.com/Betterize/page_security_tester/assets/68241874/4436a970-fcb2-4c0a-b25b-bcbd1668bd78)

- strapi - provide REST API, manage whole application
- redis - works as a queue that store messages from strapi to tests_runner
- database - store information about scans, their statuses and results
- tests_runner - run tests, process results and pass them to strapi
- web client - application web interface
- email - provided by user while scan request creation. Scan results are send there.

## Setup

### Configuration

Services configuration can be set up by environment variables. Services: database and redis loads variables from .env file that should be placed in main project directory. Other services configuration is described in their README files. Main .env file should contain below variables:

| variable             | description                                                                                             |
| -------------------- | ------------------------------------------------------------------------------------------------------- |
| APP_NAME             | value of this variable will be used with naming docker images, containers and network                   |
| DATABASE_USERNAME    | name of database user (**should match with strapi configuration**)                                      |
| DATABASE_PASSWORD    | password of database user (**should match with strapi configuration**)                                  |
| DATABASE_NAME        | database name (**should match with strapi configuration**)                                              |
| DATABASE_HOST_PORT   | set up host port on which postgres will be running. You can also configure interface (127.0.0.1:5432)   |
| STRAPI_HOST_PORT     | set up host port on which strapi will be running. You can also configure interface (127.0.0.1:1337)     |
| WEB_CLIENT_HOST_PORT | set up host port on which web_client will be running. You can also configure interface (127.0.0.1:3000) |

Example **.env**:

```
APP_NAME=page_security_scan

DATABASE_USERNAME=admin
DATABASE_PASSWORD=admin
DATABASE_NAME=some_db
DATABASE_HOST_PORT=127.0.0.1:5432

STRAPI_HOST_PORT=127.0.0.1:1337

WEB_CLIENT_HOST_PORT=127.0.0.1:3000
```

### Run order

1. database
2. redis
3. strapi
4. tests_runner
5. web client

### First run:

Postgres and redis data are stored in docker_volume directory. Make sure to set up proper permissions.

Create docker network. Replace APP_NAME with value from .env file.

```
docker network create APP_NAME-network
```

It is recommended to run each service manually with command like:

```
docker compose up service_name
```

After starting the strapi, you need to generate an API Token which you will then place in the .env file of tests_runner service. Instruction [here](https://docs.strapi.io/user-docs/settings/API-tokens)

### Later project run:

Command:

```
docker compose up -d
```

\*tests_runner service may restart few times because it requires strapi that need some time to run.
