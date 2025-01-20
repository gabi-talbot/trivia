import random
from os import abort

from flask import Flask, jsonify, abort, request
from flask_cors import CORS

from models import setup_db, db, Category, Question

# constant for pagination
NUMBER_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)

    # with app.app_context():
    #     db.create_all()

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route('/categories')
    def get_categories():
        try:
            categories = Category.query.all()

            # formatted_categories = [cat.format() for cat in categories]
            formatted_categories = {category.id: category.type for category in categories}

            return jsonify(
                {
                    'success': True,
                    'categories': formatted_categories,
                }
            )

        except Exception as e:
            print(e)
            abort(404)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions')
    def get_questions():

        try:
            # retrieve questions and paginate
            pagination_obj = Question.query.paginate(per_page=NUMBER_PER_PAGE,
                                                     page=request.args.get('page', 1, type=int))
            # format items in paginate object
            current_questions = [question.format() for question in pagination_obj.items]

            # retrieve and format categories
            categories = Category.query.all()
            formatted_categories = [cat.format() for cat in categories]


            # current_category unknowable???
            return jsonify(
                {
                    'success': True,
                    'questions': current_questions,
                    'categories': formatted_categories,
                    'current_category': categories[0].format(),
                    'total_questions': pagination_obj.total,
                }
            )
        except Exception as e:
            print(e)
            abort(404)


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):

        try:
            question = Question.query.get(id)

            question.delete()

            return jsonify({
                'success': True,
            })
        except Exception as e:
            print(e)
            abort(404)


    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/questions', methods=['POST'])
    def post_question():


        try:
            body = request.get_json()
            # test body for inputs
            question = body.get('question')
            answer = body.get('answer')
            difficulty = body.get('difficulty')
            category = body.get('category')

            # create object
            try:
                question = Question(
                question=question,
                answer=answer,
                difficulty=difficulty,
                category=category
            )
                if question.question == "" or question.answer == "":
                    raise ValueError("Empty string")
            except ValueError as err:
                print(err)
                abort(422)

            question.insert()

            return jsonify({
                'success': True,

            }), 201
        except ValueError as value_error:
            print(value_error)
            abort(422)
        except Exception as e:
            print(e)
            abort(422)


    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/questions/search', methods=['GET', 'POST'])
    def search_questions():


        try:
            body = request.get_json()
            search_term = body.get('searchTerm')

            questions = Question.query.filter(Question.question.ilike('%' + search_term + '%')).all()

            if not questions:
                abort(404)

            formatted_questions = [question.format() for question in questions]

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(formatted_questions)
            })
        except Exception as e:
            print(e)
            abort(422)


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:id>/questions')
    def questions_in_category(id):

        category = Category.query.get_or_404(id)

        try:
            # retrive all questions in a category, paginate and format
            questions = (Question.query.filter_by(category=str(id))
                         .paginate(per_page=NUMBER_PER_PAGE, page=request.args.get('page', 1, type=int)))
            formatted_questions = [question.format() for question in questions.items]

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': questions.total,
                'current_category': category.type
            })
        except Exception as e:
            print(e)
            abort(404)
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.
    
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/quizzes', methods=['POST'])
    def quiz():


        try:

            body = request.get_json()
            quiz_category = body.get('quiz_category')
            previous_question = body.get('previous_questions')


            # if no category is provided, retrieve all questions, else filter by category id.
            if quiz_category['id'] == 0:
                query = (Question.query
                         .filter(Question.id.not_in(previous_question)))
            else:
                query = (Question.query.filter_by(category=quiz_category['id'])
                        .filter(Question.id.not_in(previous_question)))

           # return filtered questions
            questions = query.all()

            # if filtered_questions is empty this will return a null value for the front-end forceEnd state
            next_question = None

            if len(questions) > 0:
                # select a random index between 0 and end of array
                index = random.randint(0, len(questions) - 1)
                # retrieve the corresponding question
                question = questions[index]
                next_question = {
                    'answer': question.answer,
                    'category': question.category,
                    'difficulty': question.difficulty,
                    'id': question.id,
                    'question': question.question
                }

            return jsonify({
                'success': True,
                'question': next_question,
                'previous_questions': previous_question
            })



        except Exception as e:
            print(e)
            abort(404)


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable_resource(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable resource'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method not allowed'
        }), 405

    return app
