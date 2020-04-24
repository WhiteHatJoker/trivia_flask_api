import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

new_question_id = None


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('postgres:postgres@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        """Tests the GET /categories API endpoint to gets all categories"""
        api = self.client.get('/categories')
        self.assertEqual(api.status_code, 200)
        expected_response = {
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
            "success": True,
            "total_categories": 6
        }
        data = json.loads(api.data)
        self.assertEqual(data, expected_response)

    def test_get_questions(self):
        """ Tests the GET /questions API endpoint which is expected to be paginated at 10 questions / page """
        expected_response = {
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
            ]
        }
        res = self.client.get('/questions?page=1')
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.data)
        self.assertEqual(body["questions"][0]["answer"], expected_response["questions"][0]["answer"])
        self.assertEqual(body["questions"][0]["category"], expected_response["questions"][0]["category"])
        self.assertEqual(body["questions"][0]["difficulty"], expected_response["questions"][0]["difficulty"])
        self.assertEqual(body["questions"][0]["id"], expected_response["questions"][0]["id"])
        self.assertEqual(body["questions"][0]["question"], expected_response["questions"][0]["question"])
        self.assertEqual(body["questions"][1]["answer"], expected_response["questions"][1]["answer"])
        self.assertEqual(body["questions"][1]["category"], expected_response["questions"][1]["category"])
        self.assertEqual(body["questions"][1]["difficulty"], expected_response["questions"][1]["difficulty"])
        self.assertEqual(body["questions"][1]["id"], expected_response["questions"][1]["id"])
        self.assertEqual(body["questions"][1]["question"], expected_response["questions"][1]["question"])
        self.assertEqual(body["questions"][2]["answer"], expected_response["questions"][2]["answer"])
        self.assertEqual(body["questions"][2]["category"], expected_response["questions"][2]["category"])
        self.assertEqual(body["questions"][2]["difficulty"], expected_response["questions"][2]["difficulty"])
        self.assertEqual(body["questions"][2]["id"], expected_response["questions"][2]["id"])
        self.assertEqual(body["questions"][2]["question"], expected_response["questions"][2]["question"])

    def test_get_questions_fail(self):
        """ Tests the GET /questions API endpoint when providing a non-existent page """
        expected_response = {
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
            "current_category": None,
            "questions": [],
            "success": True,
            "total_questions": 19
        }
        api = self.client.get('/questions?page=100')
        self.assertEqual(api.status_code, 200)
        data = json.loads(api.data)
        self.assertEqual(data, expected_response)

    def test_add_question(self):
        """ Test the POST /questions endpoint which creates a new question """
        global new_question_id
        question = {
            "answer": "Tashkent",
            "category": 3,
            "difficulty": 2,
            "question": "What is the capital of Uzbekistan?"
        }
        headers = {
            'Content-Type': 'application/json'
        }
        api = self.client.post('/questions', data=json.dumps(question), headers=headers)
        self.assertEqual(api.status_code, 200)
        body = json.loads(api.data)
        self.assertEqual(body["success"], True)
        self.assertEqual(body["message"], "Added")
        new_question_id = body.get("id")

    def test_delete_question(self):
        """ Tests the DELETE /questions/<question_id> endpoint which deletes a specific question """
        global new_question_id
        expected_response = {
            "success": True,
            "message": "Deleted"
        }
        api = self.client.delete(f'/questions/{new_question_id}')
        self.assertEqual(api.status_code, 200)
        body = json.loads(api.data)
        self.assertEqual(body, expected_response)

    def test_add_question_fail(self):
        """ Tests the POST /questions API endpoint by sending incomplete data """
        question = {
            "category": 4,
            "difficulty": 2,
            "question": "What does acronym DOTA stand for?"
        }
        headers = {
            'Content-Type': 'application/json'
        }
        api = self.client.post('/questions', data=json.dumps(question), headers=headers)
        self.assertEqual(api.status_code, 422)
        data = json.loads(api.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable data, please check your data")

    def test_delete_question_fail(self):
        """ Tests the DELETE /questions/question_id endpoint by providing a non-existent question ID to delete"""
        api = self.client.delete(f'/questions/2000')
        self.assertEqual(api.status_code, 422)
        data = json.loads(api.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable data, please check your data")

    def test_questions_by_category(self):
        """ Tests the GET /categories/category_id/questions/ endpoint which returns all questions of that category"""
        expected_response = {
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
                {
                    "answer": "Blood",
                    "category": 1,
                    "difficulty": 4,
                    "id": 22,
                    "question": "Hematology is a branch of medicine involving the study of what?"
                }
            ],
            "success": True,
            "total_questions": 3
        }
        api = self.client.get('/categories/1/questions')
        self.assertEqual(api.status_code, 200)
        data = json.loads(api.data)
        self.assertEqual(data["questions"][0]["answer"], expected_response["questions"][0]["answer"])
        self.assertEqual(data["questions"][0]["category"], expected_response["questions"][0]["category"])
        self.assertEqual(data["questions"][0]["difficulty"], expected_response["questions"][0]["difficulty"])
        self.assertEqual(data["questions"][0]["id"], expected_response["questions"][0]["id"])
        self.assertEqual(data["questions"][0]["question"], expected_response["questions"][0]["question"])
        self.assertEqual(data["questions"][1]["answer"], expected_response["questions"][1]["answer"])
        self.assertEqual(data["questions"][1]["category"], expected_response["questions"][1]["category"])
        self.assertEqual(data["questions"][1]["difficulty"], expected_response["questions"][1]["difficulty"])
        self.assertEqual(data["questions"][1]["id"], expected_response["questions"][1]["id"])
        self.assertEqual(data["questions"][1]["question"], expected_response["questions"][1]["question"])
        self.assertEqual(data["questions"][2]["answer"], expected_response["questions"][2]["answer"])
        self.assertEqual(data["questions"][2]["category"], expected_response["questions"][2]["category"])
        self.assertEqual(data["questions"][2]["difficulty"], expected_response["questions"][2]["difficulty"])
        self.assertEqual(data["questions"][2]["id"], expected_response["questions"][2]["id"])
        self.assertEqual(data["questions"][2]["question"], expected_response["questions"][2]["question"])

    def test_questions_by_category_fail(self):
        """ Tests the GET /categories/category_id/questions/ endpoint with non-existent category ID"""
        api = self.client.get('/categories/1000/questions')
        self.assertEqual(api.status_code, 404)
        data = json.loads(api.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource you are trying to modify is not found")

    def test_search_questions(self):
        """ Tests the POST /questions/search endpoint for looking up questions by the search term """
        expected_response = {
            "current_category": None,
            "questions": [
                {
                    "answer": "Alexander Fleming",
                    "category": 1,
                    "difficulty": 3,
                    "id": 21,
                    "question": "Who discovered penicillin?"
                }
            ],
            "success": True,
            "total_questions": 1
        }
        search_term = {
            "searchTerm": "penicillin"
        }
        headers = {
            'Content-Type': 'application/json'
        }
        api = self.client.post('/questions/search', data=json.dumps(search_term), headers=headers)
        self.assertEqual(api.status_code, 200)
        data = json.loads(api.data)
        self.assertEqual(data, expected_response)

    def test_search_questions_fail(self):
        """ Tests the POST /questions/search endpoint with a search term that doesn't return anything """
        search_term = {
            "searchTerm": "hola"
        }
        headers = {
            'Content-Type': 'application/json'
        }
        api = self.client.post('/questions/search', data=json.dumps(search_term), headers=headers)
        self.assertEqual(api.status_code, 404)
        data = json.loads(api.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource you are trying to modify is not found")

    def test_quizzes(self):
        """
        Tests the POST /quizzes endpoint that plays the trivia game
        it should give a random question and should not repeat questions
        """
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "previous_questions": [],
            "quiz_category": {
                "type": "Entertainment",
                "id": "5"
            }
        }
        res = self.client.post('/quizzes', data=json.dumps(data), headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_fail_quizzes(self):
        """
        Test the POST /quizzes endpoint that plays the trivia game by sending incomplete quiz data
        """
        headers = {
            'Content-Type': 'application/json'
        }
        # missing quiz body in the test
        body = {
            "previous_questions": []
        }
        api = self.client.post('/quizzes', data=json.dumps(body), headers=headers)
        self.assertEqual(api.status_code, 422)
        data = json.loads(api.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable data, please check your data")


if __name__ == "__main__":
    unittest.main()
