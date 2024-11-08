# Tracker Mom Server

## Dev

`docker compose build --build-arg userid=$(id -u) --build-arg groupid=$(id -g)`

```
docker compose run -P django /bin/bash
pdm install
pdm manage migrate
pdm run dev
```
