# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/). Once you install a virtual environment create and run a virtual environment within the `/backend` folder.

```bash
virtualenv env
source env/Scripts/activate
```

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, create a database called `trivia` by using:
```bash
createdb trivia
```

Now, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

Finally, make sure that your Postgres user and password credentials are correct in `database_path` on line 7 of [`models.py`](./models.py)

## Setting up CORS

On line 27 of [`__init__.py`](./flaskr/__init__.py) you would need to update the origins URL to the one where your website URL will be located, so that CORS policy won't block front website from accessing data from the API.

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

At this point, your API endpoint is running and ready to receive queries. Don't forget that you still need to perform  `frontend` instructions.

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Testing
To make sure that the API is working, you would need to run tests. First, head to line 20 of [`test_flaskr.py`](./test_flaskr.py) and update the Postgres user and password credentials the way you did previously.
Make sure that your environment is running and input the following terminal commands:
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
After running all the commands you should see that 13 tests were successfully run. If not, you must have missed something on your way to running the backend.


REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

## API Documentation

### `All Endpoints`
1. `GET /categories`
2. `GET /questions`
3. `DELETE /questions/<int:question_id>`
4. `POST /questions`
5. `POST /questions/search`
6. `POST /categories/<int:category_id>/questions`
7. `POST /quizzes`

### `GET /categories`

Returns all the categories with their corresponding IDs

##### Response
```
{
  "categories": [
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    {
      "id": 4, 
      "type": "History"
    }, 
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 6, 
      "type": "Sports"
    }
  ], 
  "success": true, 
  "total_categories": 6
}
```

### `GET /questions`

Gets paginated questions. It is restricted to 10 questions per page. Use page parameter for the page number. 

##### Arguments

Parameters: `page`

Eg: `GET http://localhost:5000/questions?page=1`

##### Response
```
{
  "categories": [
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }
  ], 
  "current_category": null, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
  ], 
  "success": True, 
  "total_questions": 19
}
```

### `DELETE /questions/<int:question_id>`

Deletes a specific question using the question ID

##### Request

Eg: `DELETE http://localhost:5000/questions/1`

##### Response
```
{   
    "success": True,
    "message": "Deleted"
}
```

### `POST /questions`

Creates a new question with the given details as part of the body

##### Arguments

Required Fields:
| Fields     |      Type    |
|----------  |:------------:|
| answer     |   string     |
| category   |   integer    |
| difficulty |   integer    |
| question   |   string     |

```
{
    "answer": "Tashkent",
    "category": 4,
    "difficulty": 2,
    "question": "What is the capital of Uzbekistan?"
}
```

##### Response

```
{
    "success": True,
    "message": "Added",
    "id": 1
}
```

### `POST /questions/search`

It searches and displays all the questions that have a substring equal to the given search string

##### Arguments

Required Fields:
| Fields     |      Type   |
|------------|:-----------:|
| searchTerm |    string   |

```
{
    "searchTerm" : "penicillin"
}
```

##### Response
```
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}

```

### `GET /categories/<int:category_id>/questions`

Get all the questions for a particular category

##### Request

Eg: `GET http://localhost:3000/categories/1/questions`

##### Response
```
{
  "current_category": 3, 
  "questions": [
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}
```

### `POST /quizzes`

This is the trivia quiz which gives the next question for a particular category in a randomized and unique way. Questions do not repeat.

##### Arguments

Provide the previous question id so that we know which questions were asked and they are not repeated. 
`quiz_category` is a category object. 

Required Fields:
| Fields             |      Type    |
|--------------------|:------------:|
| previous_questions |      List    |
| quiz_category      |     object   |

```
{
    "previous_questions":[],
    "quiz_category":{
        "type":"Science",
        "id":1
    }
}
```

##### Response
Eg:
```
{
    "question": {
        "answer": "Mona Lisa", 
        "category": 2, 
        "difficulty": 3, 
        "id": 17, 
        "question": "La Giaconda is better known as what?"
  }
}
``` 


### Errors

##### `422 - Unprocessable`

Response
```
{
    "success": False,
    "error": 422,
    "message": "Unprocessable data, please check your data"
}
```

##### `500 - Server Error`

Response
```
{
    "success": False,
    "error": 500,
    "message": "Server Error"
}
```


##### `404 - Resource not found`

Response
```
{
    "success": False,
    "error": 404,
    "message": "Resource you are trying to modify is not found"
}
```

##### `405 - Method Not Allowed`

Response
```
{
    "success": False,
    "error": 405,
    "message": "Method not allowed. Please check documentation"
}
```