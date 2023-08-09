# Klonowanie

## Sposób 1 - przy pierwszej instalacji

```
git clone --recurse-submodules https://github.com/AddCubeDev/strapi_betterize.git
```

## Sposób 2 - gdy pobrany jest już główny projekt i chcemy dodać submodule

```
git submodule init
git submodule update
```

---

Aby zapewnić prawidłowe działanie, konieczne jest ustawienie EditorJS na odpowiednim branchu i pobranie najnowszych zmian.
Podane poniżej komendy należy uruchamiać z głównego poziomu projektu.

```
cd src/extensions/strapi-plugin-react-editorjs/
git checkout -b custom
git branch --set-upstream-to=origin/custom custom
git pull
```

# Push

Działa, jeżeli wszystkie zmiany z submodules zostały wypchnięte. Należy uruchamiać z głównego poziomu projektu.

```
git push --recurse-submodules=check
```

# Pull

Należy uruchamiać z głównego poziomu projektu.

```
git submodule update --remote
```

# Commit

Commity mogą być wykonywane "zwyczajnie". Poleca się dodawać osobne commity z poziomu podmodułu i osobne z poziomu głównego.
Zmiana w submodules wymaga zmiany na głównym poziomie projektu.

# Komendy

Opis akcji, które należy wykonać po pierwszym uruchomieniu, aby wszystko na frontendzie działało poprawnie: https://www.notion.so/Pierwsze-kroki-a3b2a9ac26664dad92225911dd0f3913

## `first run`

Dodaj plik .env z poniższymi zmiennymi do głównego katalogu projektu. Pamiętaj o tym, żeby każdej zmiennej przypisać odpowiednią wartość! Dokładny opis zmiennych znajduje się [tutaj](https://www.notion.so/Zmienne-rodowiskowe-5291ca28b7f1423f88f72d88fc9187be)

```
# docker setup
APP_NAME=
DATABASE_HOST_PORT=

# strapi setup
HOST=
PORT=
APP_KEYS=
API_TOKEN_SALT=
ADMIN_JWT_SECRET=
TRANSFER_TOKEN_SALT=
JWT_SECRET=

# email setup
EMAIL_FROM=
EMAIL_TO=
EMAIL_ADDRESS=
EMAIL_PASSWORD=

# notyfy astro
PUBLISH_URL=
REFRESH_DEV_URL=

# database setup
DATABASE_CLIENT=
DATABASE_HOST=
DATABASE_USERNAME=
DATABASE_PASSWORD=
DATABASE_NAME=
DATABASE_PORT=
```

Następnie wykonaj poniższe polecenie:

```
npm install
```

## `develop mode`

Uruchom z włączonym autoReload

```
npm run develop
```

## `start mode`

Uruchom bez autoReload

```
npm run start
```

## Generowanie typów typescript

```
npm run strapi ts:generate-types
```

# Docker

## network

Aby kontenery mogły się prawidłowo komunikować należy mieć utworzoną sieć o nazwie APP_NAME-networks, gdzie APP_NAME powinno być takie jak wartość, która została ustawiona w pliku .env. Jeśli ustawioną wartością jest betterize to sieć powinna nazywać się betterize-network.

Możesz sprawdzić, czy taka sieć już istnieje poleceniem:

```
docker network ls
```

Jeśli sieć nie istnieje i chcesz ją dodać, to możesz to zrobić przy pomocy poniższego polecenia. Pamiętaj, aby zamienić APP_NAME wartością ustawioną w .env

```
docker network create APP_NAME-network
```

## develop mode

```
docker compose up -d
```

## production mode

```
docker compose -f docker-compose.production.yaml up -d
```

---
