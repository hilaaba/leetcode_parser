import requests
import csv

URL = 'https://leetcode.com/graphql'
FIELD_NAMES = ('id', 'title', 'acceptance', 'difficulty')
DEFAULT_FILENAME = 'leetcode_problems.csv'

payload = {
    "variables": {
        "categorySlug": "algorithms",
        "skip": 0,
        "limit": 10,
        "filters": {},
    },
    "query": """query problemsetQuestionList(
        $categorySlug: String,
        $limit: Int,
        $skip: Int,
        $filters: QuestionListFilterInput
        ) {
        problemsetQuestionList: questionList(
            categorySlug: $categorySlug
            limit: $limit
            skip: $skip
            filters: $filters
            ) {
            questions: data {
                acRate
                difficulty
                frontendQuestionId: questionFrontendId 
                title
            }
        }
    }""",
}

response = requests.post(URL, json=payload).json()

questions = response.get('data').get('problemsetQuestionList').get('questions')

result = []
for question in questions:
    id = question.get('frontendQuestionId')
    title = question.get('title')
    acceptance = round(question.get('acRate'), 1)
    difficulty = question.get('difficulty').lower()
    result.append((id, title, acceptance, difficulty))

with open(DEFAULT_FILENAME, 'w') as file:
    writer = csv.writer(file)
    writer.writerow(FIELD_NAMES)
    writer.writerows(result)

if __name__ == '__main__':
    pass
