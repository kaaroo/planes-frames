# Planes app
This is a project with ADS-B plane frames data generator. 
Generated plane frame data is saved to the database.
Scheduler is responsible for generating new dataframe every 1 second.

Read more about ADS-B data: https://dlapilota.pl/wiadomosci/dlapilota/ads-b-automatic-dependent-surveillance-broadcast

# Prerequisites
* Python 3.10+
* Poetry
* Docker
* docker-compose

# The development mode
1) Build a Docker image with the application:
```docker build -t plane-frames-gen-app .```

2) Start the application and Postgres with the docker-compose:
```docker-compose up -d```

3) Open: http://localhost:8000/docs to see the OpenAPI documentation.

# Run tests
```poetry run pytest .```
