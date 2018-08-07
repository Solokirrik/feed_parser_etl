# Feed parser ETL

## Service's Responsibility

Base implementation of Extract/Transform/Load pipeline:
- parser

Source-oriented implementation of Transform and Load using Django ORM
- target_harb
- target_reddit

## Installation

### Using

- [Python](https://www.python.org/) 3.7 or later
- [Docker](https://www.docker.com/get-docker)
- docker-compose

### Settings

- basic: ```.env```
- tests: ```.envtest```

### Create or recreate all containers and start Django ###

```bash
$ ./recreate.sh
```

## Run

### Start app
```bash
$ ./docker-compose up
```

### Load data

- [reddit.com/r/news/.rss](http://localhost:8000/reddit/get_data)
- [habrahabr.ru/rss/hubs/all](http://localhost:8000/habr/get_data)

### Check loaded data 
Using ```DJANGO_SU_NAME``` and ```DJANGO_SU_PASS``` from ```.env```

[Django admin](http://localhost:8000/admin)

#### Running unit tests and codestyle check ###

```bash
$ ./test.sh
```
