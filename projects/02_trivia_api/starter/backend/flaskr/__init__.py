import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category
import random

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS"
        )
        return response

    # this endpoint is used to handle all the GET request to the category database
    @app.route("/categories", methods=["GET"])
    def get_categories():
        categories = Category.query.order_by(Category.type).all()
        if len(categories) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "categories": {category.id: category.type for category in categories},
            }
        )

    """ 
    this end point loads the questions from the database as well as the total 
    number of questions, categories all paginated in 10 questions pp
    """

    @app.route("/questions", methods=["GET"])
    def get_questions():
        quest_list = Question.query.order_by(Question.difficulty).all()
        categories = Category.query.order_by(Category.type).all()

        current_questions = paginate_questions(request, quest_list)

        if len(quest_list) == 0:
            abort(404)
        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(quest_list),
                "categories": {category.id: category.type for category in categories},
                "current_category": None,
            }
        )

    # this endpoint is used to delete a question bt its id
    @app.route("/questions/<int:id>", methods=["DELETE"])
    def delete_questions(id):
        try:
            question = Question.query.filter_by(id=id).one_or_none()
            if question is None:
                abort(404)
            question.delete()
            return jsonify({"success": True, "deleted": id})

        except:
            abort(422)

    """ 
    this endpoint posts a new question, answer, difficulty, category to the database
    The new question can then be found in the list of questions
    """

    @app.route("/questions", methods=["POST"])
    def post_questions():
        try:
            body = request.get_json()
            if not (
                "question" in body
                and "answer" in body
                and "difficulty" in body
                and "category" in body
            ):
                abort(422)

            new_question = body["question"]
            new_answer = body["answer"]
            new_difficulty = body["difficulty"]
            new_category = body["category"]

            new_question = Question(
                question=new_question,
                answer=new_answer,
                category=new_category,
                difficulty=new_difficulty,
            )
            new_question.insert()
            return jsonify({"success": True, "created": new_question.id})

        except:
            abort(422)

    """
    This endpoint is used to make a search query across the questions list
    It is case insensitive and will return a list of questions that match the search word
    """

    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        body = request.get_json()
        search_word = body.get("searchTerm", None)
        if search_word:
            search_result = Question.query.filter(
                Question.question.ilike(f"%{search_word}%")
            ).all()

            return jsonify(
                {
                    "success": True,
                    "questions": [question.format() for question in search_result],
                    "total_questions": len(search_result),
                    "current_category": None,
                }
            )

        abort(404)

    """
    This enpoint filters the questions by category
    """

    @app.route("/categories/<int:id>/questions", methods=["GET"])
    def get_category_questions(id):
        try:
            questions_per_category = Question.query.filter(
                Question.category == str(id)
            ).all()
            return jsonify(
                {
                    "success": True,
                    "questions": [
                        question.format() for question in questions_per_category
                    ],
                    "totalQuestions": len(questions_per_category),
                    "currentCategory": id,
                }
            )

        except:
            abort(422)

    """
    this endpoint is used to play the game. it retrieves a question according to a selected category
    as well as accounting the prevuous questions viewed.
    """

    @app.route("/quizzes", methods=["POST"])
    def play_quiz():
        try:
            body = request.get_json()
            if not ("previous_questions" in body and "quiz_category" in body):
                abort(422)

            quiz_category = body.get("quiz_category")
            previous_questions = body.get("previous_questions")

            if quiz_category["type"] == "click":
                available_questions = Question.query.filter(
                    Question.id.notin_(previous_questions)
                ).all()
            else:
                available_questions = (
                    Question.query.filter_by(category=quiz_category["id"])
                    .filter(Question.id.notin_(previous_questions))
                    .all()
                )

            new_question = (
                available_questions[
                    random.randrange(0, len(available_questions))
                ].format()
                if len(available_questions) > 0
                else None
            )

            return jsonify({"success": True, "question": new_question})
        except:
            abort(422)

    """
    error handlers for all expected errors 
    including 404 and 422. 
    """

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    return app
