import requests
import csv

URL = 'https://leetcode.com/graphql'
FIELD_NAMES = ('id', 'title', 'acceptance', 'difficulty')
DEFAULT_FILENAME = 'leetcode_problems.csv'

data = {
    "variables": {
        "categorySlug": "algorithms",
        "skip": 0,
        "limit": 10,
        "filters": {},
    },
    "query": "query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {problemsetQuestionList: questionList(categorySlug: $categorySlug limit: $limit skip: $skip filters: $filters) {total: totalNum questions: data {acRate difficulty freqBar frontendQuestionId: questionFrontendId isFavor paidOnly: isPaidOnly status title titleSlug topicTags {name id slug} hasSolution hasVideoSolution}}}",
}

response = requests.post(URL, json=data).json()

problems_list = response.get('data').get('problemsetQuestionList').get('questions')

result = []
for problem in problems_list:
    id = problem.get('frontendQuestionId')
    title = problem.get('title')
    acceptance = round(problem.get('acRate'), 1)
    difficulty = problem.get('difficulty').lower()
    result.append((id, title, acceptance, difficulty))

with open(DEFAULT_FILENAME, 'w') as file:
    writer = csv.writer(file)
    writer.writerow(FIELD_NAMES)
    writer.writerows(result)




if __name__ == '__main__':
    pass
