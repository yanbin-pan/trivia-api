# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## API Reference
**GET** `\categories` </br>

Fetches a JSON of available categories in the database.
- Input args: None
- Returns: JSON dict of categories with respective ID </br>
Sample response:
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}
```
**GET** `/questions` </br>
Fetches all availabe questions in the database
- Input args: None
- Returns: JSON dict of cateories available and a list of dicts for each question.
Sample response:
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": null,
    "questions": [
        {
            "answer": "Toronto",
            "category": 3,
            "difficulty": 1,
            "id": 25,
            "question": "What is the capital of Canada?"
        },
```

**DELETE** `/questions/<questions_id>`
Delete a question bt its id </br>
- Input args: (Int) question_id
- Returns: Deleted question_id
Sample response:
```
{
  "deleted": "16", 
  "success": true
}
```

**POST** `/questions`
Adds a new question to the databse 
- Input: (dict) dictionary as {question:str, answer:str, difficulty:int, category:string}
- Returns: (Int) new created ID question
Sample Response:
```
{
  "created": 18, 
  "success": true
}
```
**POST** `/questions/search`
Fetch all questions that match the search term (case insenstitive)
- Input: (str) {searchTerm:str}
- Returns: (List) List of questions matching the search string
Sample Response:
```
Input:
{
    "searchTerm": "What"
}

Output

{
  "current_category": null, 
  "questions": [
    {
      "answer": "3.1415", 
      "category": 2, 
      "difficulty": 1, 
      "id": 10, 
      "question": "What is the number PI?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

**GET** `/categories/<category_id>/questions` </br>
Fetches a dictionary of questions for the specified category
- Input: (Int) Category_id
- Returns: (List)
Sample Response:
```
{
  "current_category": 1, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
  ], 
  "success": true, 
  "total_questions": 2
}
```

**POST** `/quizzes` 
POST /quizzes Fetches one random question within a specified category. Previously asked questions are not asked again.
- Input: {previous_questions: list, quiz_category: {id:Int, type:str}}
- Returns: Question
Sample Response:
```
{
  "question": {
    "answer": "The Liver", 
    "category": 1, 
    "difficulty": 4, 
    "id": 20, 
    "question": "What is the heaviest organ in the human body?"
  }, 
  "success": true
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```