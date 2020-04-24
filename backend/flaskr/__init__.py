import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


'''
# Supporting method to help paginate all questions after running /questions endpoint
'''
def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    current_questions = selection[start:end]
    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    db = setup_db(app)
    CORS(app, origins='http://localhost:3000', methods=['GET', 'POST', 'PATCH', 'DELETE', 'OPTIONS'], supports_credentials=True)

    '''
    # Returns all the categories list
    '''
    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.type).all()
        cat_quantity = len(categories)
        if cat_quantity == 0:
            abort(404)
        formatted_categories = [category.format() for category in categories]

        return jsonify({
            'success': True,
            'categories': formatted_categories,
            'total_categories': cat_quantity
        })

    '''
    # Returns paged questions. 10 questions per query or page.
    '''
    @app.route('/questions')
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        if len(questions) == 0:
            abort(404)
        unformatted_paged_questions = paginate_questions(request, questions)
        formatted_paged_questions = [question.format() for question in unformatted_paged_questions]
        categories = Category.query.order_by(Category.type).all()
        formatted_categories = [category.format() for category in categories]

        return jsonify({
            'success': True,
            'questions': formatted_paged_questions,
            'total_questions': len(questions),
            'categories': formatted_categories,
            'current_category': None
        })

    '''
    # Deletes the question. Accepts question id to locate the necessary question
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter_by(id=question_id).one_or_none()
            question.delete()
            return jsonify({
                'success': True,
                'message': 'Deleted'
            })
        except:
            abort(422)

    '''
    # Creates a new question and answer in the database. Accepts question, answer, category and difficulty
    '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            body = request.get_json()

            new_question = body['question']
            new_answer = body['answer']
            new_difficulty = body['difficulty']
            new_category = body['category']

            question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
            question.insert()
            return jsonify({
                'success': True,
                'message': 'Added',
                'id': question.id
            })
        except:
            abort(422)

    '''
    # Searches for a question. Accepts a search term string to search for
    '''
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        search_term = request.get_json()['searchTerm']
        questions = Question.query.filter(
            Question.question.ilike("%" + search_term + "%")).order_by(Question.question).all()

        if questions:
            formatted_questions = [question.format() for question in questions]
            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(formatted_questions),
                'current_category': None
            })
        else:
            abort(404)

    '''
    # Returns all the questions by the provided category. Accepts a category ID
    '''
    @app.route('/categories/<int:category_id>/questions')
    def questions_by_category(category_id):
        questions = Question.query.filter_by(category=category_id).all()
        if questions:
            unformatted_paged_questions = paginate_questions(request, questions)
            formatted_questions = [question.format() for question in unformatted_paged_questions]
            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(questions),
                'current_category': category_id
            })
        else:
            abort(404)

    '''
    # Returns a quiz question and an answer per chosen category. 
    it should give a random question and should not repeat questions
    '''
    @app.route('/quizzes', methods=['POST'])
    def play_trivia():
        try:
            body = request.get_json()
            if body["quiz_category"]["id"] == 0:
                questions = Question.query.with_entities(Question.id).all()
            else:
                questions = Question.query.with_entities(Question.id).filter_by(category=body["quiz_category"]["id"]).all()

            total_questions_in_category = len(questions)
            if total_questions_in_category == 0:
                abort(404)
            previous_questions = body["previous_questions"]
            if len(previous_questions) == total_questions_in_category:
                return jsonify({})
            not_asked_question_ids = [question_id for question_id in questions if question_id not in previous_questions]
            random_question_id = random.choice(not_asked_question_ids)
            random_question = Question.query.get(random_question_id)
            return jsonify({
                "success": True,
                "question": random_question.format()
            })
        except:
            abort(422)

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Server Error"
        }), 500

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource you are trying to modify is not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable data, please check your data"
        }), 422

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed. Please check the documentation"
        }), 405

    return app
