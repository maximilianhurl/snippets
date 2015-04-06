#Snippets

[![Build Status](https://travis-ci.org/maximilianhurl/snippets.svg)](https://travis-ci.org/maximilianhurl/snippets)

A webapp to store markdown code snippets (In development)

## To do:

- add snippet models and api (hypermedia)
- add travis/coverage support
- add deployment scripts

##Setup
	
	brew install python3
	virtualenv env -ppython3.4
	source env/bin/activate
	pip3 install -r requirements.txt

    //install postgres
    brew install postgress
    initdb /usr/local/var/postgres -E utf8
    postgres -D /usr/local/var/postgres  // start postgres

    //create a new user and database
    createuser -d -P postgres  // set password to 'password'
    psql -d postgres
    create database snippets;

    //check the port number
    psql -U postgres -h localhost
    select inet_server_port();

    env/bin/python3 manage.py migrate
    env/bin/python3 manage.py runserver