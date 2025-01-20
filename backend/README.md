# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## API Reference

### Getting Started

- Base URL: This app can only be run locally, hosted at the default `http://127.0.0.1:5000`, which is set as a proxy 
in the frontend configuration.
- Authentication: This version of the application does not require
authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```json
{
  "success": false,
  "error": 405,
  "message": "Method not allowed"
}
```
The API will return four error types when requests fail:

- 400: Method not allowed
- 404: Not found
- 422: Unprocessable resource
- 500: Internal server error

### Endpoints

`GET '/categories'`

#### General
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

#### Sample 

`curl http://127.0.0.1:5000/categories`


```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

`GET '/categories/<int:id>/questions'`

#### General

- Fetches a dictionary containing a list of questions that 
correspond to the request argument for `<int:id>`
- Results are paginated in groups or 10 questions. Include a request argument 
to choose the page number, starting from 1.

#### Sample

`curl http://127.0.0.1:5000/categories/3/questions?page=1`

```json
{
  "current_category":"Geography",
  "questions":[
    {"answer":"Lake Victoria",
      "category":3,
      "difficulty":2,
      "id":13,
      "question":"What is the largest lake in Africa?"},
    {"answer":"The Palace of Versailles",
      "category":3,
      "difficulty":3,
      "id":14,
      "question":"In which royal palace would you find the Hall of Mirrors?"},
    {"answer":"Agra",
      "category":3,
      "difficulty":2,
      "id":15,
      "question":"The Taj Mahal is located in which Indian city?"}
  ],
  "success":true,
  "total_questions":3
}
```
`GET /questions`

#### General

- Fetches a dictionary containing a list of all questions
- Results are paginated in groups of 10. Include a request argument 
to choose the page number, starting from 1.

#### Sample

`curl http://127.0.0.1:5000/questions?page=2`

```json
{
  "categories": [
    {"id":1,"type":"Science"},
    {"id":2,"type":"Art"},
    {"id":3,"type":"Geography"},
    {"id":4,"type":"History"},
    {"id":5,"type":"Entertainment"},
    {"id":6,"type":"Sports"}],
  "current_category":
  {"id":1,"type":"Science"},
  "questions":[
    {"answer":"Escher",
      "category":2,
      "difficulty":1,
      "id":16,
      "question":"Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"},
    {"answer":"Mona Lisa",
      "category":2,
      "difficulty":3,
      "id":17,
      "question":"La Giaconda is better known as what?"},
    {"answer":"One",
      "category":2,
      "difficulty":4,
      "id":18,
      "question":"How many paintings did Van Gogh sell in his lifetime?"},
    {"answer":"Jackson Pollock",
      "category":2,
      "difficulty":2,
      "id":19,
      "question":"Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?",
    },{"answer":"The Liver",
      "category":1,
      "difficulty":4,
      "id":20,
      "question":"What is the heaviest organ in the human body?"},
    {"answer":"Alexander Fleming",
      "category":1,
      "difficulty":3,
      "id":21,
      "question":"Who discovered penicillin?"},
    {"answer":"Blood",
      "category":1,
      "difficulty":4,
      "id":22,
      "question":"Hematology is a branch of medicine involving the study of what?"},
    {"answer":"Scarab",
      "category":4,
      "difficulty":4,
      "id":23,
      "question":"Which dung beetle was worshipped by the ancient Egyptians?"}
  ],"success":true,
  "total_questions":30
}
```

` DELETE /questions/<int: id>`

#### General

- Deletes the question of the given id, if it exits. 

#### Sample

`curl -X DELETE http://127.0.0.01:5000/questions/5`

```json
{
  "success": true
}
```

`POST /questions`

#### General

- Creates a new question using submitted request body 
arguments of question, answer, difficulty and category.

#### Sample

`curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" 
-d '{"question": "Is documenting your API boring but important to do", 
"answer": "Yes", "difficulty": 1, "category": "1"}'`

```json
{
  "success": true
}
```
`POST /questions/search`

#### General

- Searches for and returns a dictionary containing
a list of questions that match the request argument `searchTerm`

#### Sample

`curl -X POST http://127.0.0.1:5000/questions/search -H "Content-Type: application/json"
-d '{"searchTerm": "title"}'`

```json
{
  "questions":[
  {"answer":"Edward Scissorhands", 
    "category":5,
    "difficulty":3,
    "id":6,
    "question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"}
],"success":true,
  "total_questions":1
}

```

`POST /quizzes`

#### General

- Returns a list of questions that are not in the request body argument
`previous_questions`.
- If a request argument `quiz_category` is provided, the questions returned will
be confined to that category. If not, all question categories will be returned.
- If there are no further questions, `question` will be null

#### Sample

`curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json"
-d '{"previous_questions": [4, 2], "quiz_category": {"id": 5, "type": "Entertainment"}}'`

```json
{
  "previous_questions":[4, 2],
  "question":
  {"answer":"Edward Scissorhands",
    "category":5,
    "difficulty":3,
    "id":6,
    "question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"},
  "success":true
}

```
## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
