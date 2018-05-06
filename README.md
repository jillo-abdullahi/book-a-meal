[![Build Status](https://travis-ci.org/jillo-abdullahi/book-a-meal.svg?branch=ft-auth-endpoints)](https://travis-ci.org/jillo-abdullahi/book-a-meal)
[![Coverage Status](https://coveralls.io/repos/github/jillo-abdullahi/book-a-meal/badge.svg?branch=ft-auth-endpoints)](https://coveralls.io/github/jillo-abdullahi/book-a-meal?branch=ft-auth-endpoints)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5bb5177276e94516bd936a2abeb672f2)](https://www.codacy.com/app/jillo-abdullahi/book-a-meal?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=jillo-abdullahi/book-a-meal&amp;utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/295fb323b44119118c01/maintainability)](https://codeclimate.com/github/jillo-abdullahi/book-a-meal/maintainability)



# Book-A-Meal
Book-A-Meal is an application that allows customers to make food orders and helps the food vendor know what the customers want to eat.

# Installation - UI
To get a view of the front-end UI, do the following:&nbsp;

Clone the repository into your local environment: &nbsp;
`git clone https://github.com/jillo-abdullahi/book-a-meal`&nbsp;

Switch to book-a-meal directory you just cloned:&nbsp;
`cd book-a-meal/UI`&nbsp;

Run `index.html` file in your browser.&nbsp;

#### UI link to gh-pages:

https://jillo-abdullahi.github.io/book-a-meal/UI/ &nbsp;

# Installation - API
Use the following guide the get the API up and running.&nbsp;
#### Requirements
It is recommended that you have the following set up on your local environment before getting started

1. [python 3.x](https://www.python.org/downloads/)
2. [Git](https://git-scm.com)
3. Working browser or [Postman](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?utm_source=chrome-app-launcher-info-dialog)
4. [virtualenv](http://www.pythonforbeginners.com/basics/how-to-use-python-virtualenv) for an isolated working environment.&nbsp;

Do the following:

1. Clone the repo into a folder of your choice:
`git clone https://github.com/jillo-abdullahi/book-a-meal`
2. Navigate to the cloned folder
`cd book-a-meal`
3. Create a virtual environment
`virtualenv venv`
4. Activate the virtual environment you just created
`source venv/bin/activate`
5. Install all dependencies into your virtual environment
`pip install -r requirements.txt`
6. Confirm you have all packages installed
`pip freeze`
7. Set environment variables for `APP_SETTINGS`
`export APP_SETTINGS="development"`
8. Set the entry point for the app
`export FLASK_APP="run.py"`
9. Set up migration by running `python manage.py db migrate`
10. Populate the db with tables by running `python manage.py db upgrade`

#### Run the API
Get the app running by typing
`flask run`

#### Run tests
To run all tests type
`nosetests --with-coverage --cover-package=app`

#### Test API endpoints
Fire up [Postman](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?utm_source=chrome-app-launcher-info-dialog) to test the endpoints.&nbsp;

**EndPoint** | **Functionality**
--- | ---
POST `/api/v1/auth/signup` | Creates a user account.
POST `/api/v1/auth/login` | Logs in a user.
POST  `/api/v1/meals` | Add a meal option. Only admin caterers can do this.
GET `api/v1/meals`| Get all meal options. Only admin caterers can do this.
PUT `api/v1/meals/<mealid>`| Update the information of a meal option.
DELETE `api/v1/meals/<mealid>` | Remove a meal option.
POST `api/v1/menu`| Set up the menu for the day.
GET `api/v1/menu`| Get the menu for the day.
POST `api/v1/orders`| Select the meal option from the menu.
PUT `api/v1/orders/<orderid>`| Modify an order.
GET `api/v1/orders`| Get all the orders.

#### API Documentation
Go to the link below to view api documentation

[Book-A-Meal on Apiary.io](https://bookameal8.docs.apiary.io)

## View the app on Heroku
Click on the following link to view the app on Heroku

[Book-A-Meal on Heroku](https://bookameal-api-heroku.herokuapp.com/)







