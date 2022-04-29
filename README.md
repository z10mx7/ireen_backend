# x

IREEN API


:License: MIT


###### 3 Simple user and their passwords : 
    `mohammad:mohammad`
    `reza:reza`
    `mohammadreza:mohammadreza`
 

## Setup

#### 1 - clone the repo

    $ git clone https://github.com/z10mx7/ireen_backend.git

##### 2 - go inside project directory

    $ cd ireen_backend

##### 3 - how to run this ? :

    $ docker-compose up


##### 5 - view the docs

    http://localhost:8000/docs

##### 6 - use it from postman

    import postman collection and test the api

## Directory Structure

```

├─── docker-compose.yml => setup container's for :
│     backend api, database, database management, ...
│
├─── Dockerfile => you know that, blah blah blah.
│
├─── entrypoint.sh => runs inside docker container when container is running.
│     contains some simple bash script for pre-run stuff
│
├─── main.py =>   Main File 
├─── requirements.txt => requirements for web api code that must be installed by pip
└─── README.md => You Are Looking at This right now
```

## Adresses and credentials for both server and local

##### A : Backend API and API Documentation

    $ http://localhost:8000/docs


##### C : Database Administration

    $ http://localhost:8083

###### System:MongoDB

###### Server:mongo

###### Username:mongo_user

###### Password:mongo_password




### TODO

- [x] docker compose
- [ ] sentry
