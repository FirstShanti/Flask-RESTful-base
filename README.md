# RESTfull application
A template and environment for building a RESTful application for anything you can think of.
# Features:
- Python
- Docker
- MySQL
- Flask
- Gunicorn
# Description:
#### Users ENDPOINT:
- GET:
    -    `http://localhost:<port>/api/v1/users` - list of users
    -	 `http://localhost:<port>/api/v1/users/<user_id>` - single user
    -    `response: 200, 404`
- POST:
    -    `http://localhost:<port>/api/v1/users` - create user
    -    `response: 201, 404`
    > *json body: {field: value, ...} 

- PUT:
    -    `http://localhost:<port>/api/v1/users/<user_id>` -  update user
    -    `response: 200, 400, 404`
    > *json body: {field: value, ...}

- DELETE:
    -    `http://localhost:<port>/api/v1/users/<user_id>` -  delete user
    -    `response: 204, 400, 404`
 
        
# Getting Started

## Preparing Environment

### For first clone this repository:

` git clone https://github.com/FirstShanti/Flask-RESTful-vs-MySQL `

### Install Docker:

Docker
[Docker](https://docs.docker.com/get-docker/)

### Create .env file with credentials and parameters:

- MYSQL_USER=`<username>`
- MYSQL_ROOT_PASSWORD=`<userpassword>`
- MYSQL_HOST=database
- MYSQL_PORT=3306
- MYSQL_DB=`<db_name>`

- APP_SERVER_HOST=0.0.0.0
- APP_SERVER_PORT=`<port>`
- ENVIRONMENT=`<Development or Production>` 
- SECRET_KEY=`<secret key>`

# All is done

### Run docker containers:

~<project path>$ docker-compose up
