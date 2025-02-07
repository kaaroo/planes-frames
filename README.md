# Planes app
This is a project with ADS-B plane frames data generator. 
Generated plane frame data is saved to the database.
Scheduler is responsible for generating new dataframe every 1 second.

Read more about ADS-B data: https://dlapilota.pl/wiadomosci/dlapilota/ads-b-automatic-dependent-surveillance-broadcast


# The development mode:
0) Build docker image:
```docker build -t plane-frames-gen-app .```

1) Start the FastAPI app with the command:
```uvicorn app.main:app --reload --env-file .env```

2) Start PostgreSQL with the docker compose
```docker-compose up -d```

# TODO tests & how to run them
# TODO autoformatting

