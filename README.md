# Socrates Project


## Setup

- Create the file `app/.env_local` with the following content:
```txt
DATABASE_HOST=127.0.0.1
DATABASE_PORT=3306
DATABASE_NAME=dbsocrates
DATABASE_USER=root
DATABASE_PASSWORD=c5402da14d24
```

- Start Databases:
```sh
docker-compose up -d db
docker-compose up -d chromadb
```

- Start Backend:
```sh
cd api
source venv/bin/activate
uvicorn app.main:app --reload
```

- Access to http://localhost:8000/docs#/
