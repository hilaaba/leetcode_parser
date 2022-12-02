import unittest
from main import get_problems, parse_problem


class TestGetProblems(unittest.TestCase):
    """Testing get_problems() function."""

    def test_valid_data(self):
        excepted_list = [
            {
                'acRate': 49.09302801005822,
                'difficulty': "Easy",
                'frontendQuestionId': "1",
                'title': "Two Sum"
            },
            {
                'acRate': 39.87096664461644,
                'difficulty': "Medium",
                'frontendQuestionId': "2",
                'title': "Add Two Numbers"
            },
        ]
        valid_data = {
            'data': {
                'problemsetQuestionList': {
                    'questions': excepted_list
                }
            }
        }
        problems_list = get_problems(valid_data)
        self.assertEqual(problems_list, excepted_list)

    def test_invalid_data(self):
        invalid_data = [
            {},
            {'data': {}},
            {'data': {'problemsetQuestionList': {}}},
            {'data': {'problemsetQuestionList': {'questions123': []}}}
        ]
        for data in invalid_data:
            with self.subTest(data=data):
                with self.assertRaises(KeyError):
                    get_problems(data)
        problems_not_list = {
            'data': {
                'problemsetQuestionList': {
                    'questions': {}
                }
            }
        }
        with self.assertRaises(TypeError):
            get_problems(problems_not_list)


class TestParseProblem(unittest.TestCase):
    """Testing parse_problem() function."""

    def setUp(self):
        self.problem_data = {
            'acRate': 33.80323087015701,
            'difficulty': 'Medium',
            'frontendQuestionId': '3',
            'title': 'Longest Substring Without Repeating Characters',
        }

    def test_valid_problem_data(self):
        excepted_tuple = (
            '3',
            'Longest Substring Without Repeating Characters',
            33.8,
            'medium',
        )
        data = parse_problem(self.problem_data)
        self.assertEqual(data, excepted_tuple)

    def test_invalid_problem_id(self):
        invalid_ids = (123, [], {})
        for problem_id in invalid_ids:
            with self.subTest(data=problem_id):
                self.problem_data['frontendQuestionId'] = problem_id
                with self.assertRaises(TypeError):
                    parse_problem(self.problem_data)
        invalid_id = 'asd'
        self.problem_data['frontendQuestionId'] = invalid_id
        with self.assertRaises(ValueError):
            parse_problem(self.problem_data)

    def test_invalid_problem_title(self):
        invalid_titlies = (123, [], {})
        for title in invalid_titlies:
            with self.subTest(data=title):
                self.problem_data['title'] = title
                with self.assertRaises(TypeError):
                    parse_problem(self.problem_data)

    def test_invalid_problem_acceptance(self):
        invalid_acceptances = ('asdf', [], {})
        for acceptance in invalid_acceptances:
            with self.subTest(data=acceptance):
                self.problem_data['acRate'] = acceptance
                with self.assertRaises(TypeError):
                    parse_problem(self.problem_data)

    def test_invalid_problem_difficulty(self):
        invalid_difficulties = (123, {}, [])
        for difficulty in invalid_difficulties:
            with self.subTest(data=difficulty):
                self.problem_data['difficulty'] = difficulty
                with self.assertRaises(TypeError):
                    parse_problem(self.problem_data)
        invalid_difficulty = 'asd'
        self.problem_data['difficulty'] = invalid_difficulty
        with self.assertRaises(ValueError):
            parse_problem(self.problem_data)


if __name__ == '__main__':
    unittest.main()
