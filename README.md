# BucketList-REST-API
[![Build Status](https://travis-ci.org/Descartess/BucketList-REST-API.svg?branch=master)](https://travis-ci.org/Descartess/BucketList-REST-API)
[![Coverage Status](https://coveralls.io/repos/github/Descartess/BucketList-REST-API/badge.svg?branch=master)](https://coveralls.io/github/Descartess/BucketList-REST-API?branch=master)


**BucketList** is a web application designed to help one to record, edit, update activities one desires to accomplish before reaching a certain age. This application exposes a rest API which can be consumed

This is deployed on heroku with a base url http://descartes-bucketlist.herokuapp.com/

## Technologies
1. Python 3.8+
2. Flask 2.1.2
3. Nosetests
4. Postgresql
5. Swagger


## Getting Started
These are instructions on how to set up the application on a local development machine.

1. Clone the repository
```
git clone https://github.com/hoangtuananh97/flaskdemo.git
```
2. Install the dependencies
```
pip install -r requirements.txt
```
3. Set up environment variables `DATABASE_URL`  and  `DATABASE_TEST_URL`
3. Run the application
```
python manage.py runserver
```
4. Create database
```
# This is done for only the initial installation
python manage.py recreate_db
```

## Documentation
The API documentation can be found at http://descartes-bucketlist.herokuapp.com/apidocs/
```
http://127.0.0.1:5000/apidocs/
```
## Features
* Users can create accounts
* Users can sigin and signout of application
* Users can create,edit,view and delete bucket lists
* Users can create,edit,view and delete bucket list items
* Users can search bucketlists
* Users can use pagination
* Users can reset passwords

## Testing
To run tests
1. Run tests
```
# in root directory

nosetests tests
```
