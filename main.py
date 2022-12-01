import csv
import logging
import sys

import requests

from exceptions import EndpointError, RequestError

ENDPOINT = 'https://leetcode.com/graphql'
FIELD_NAMES = ('id', 'title', 'acceptance', 'difficulty')
DEFAULT_FILENAME = 'leetcode_problems.csv'

SKIP_PROBLEMS = 0
LIMIT_PROBLEMS = 2500
FILTERS = {}

PAYLOAD = {
    'variables': {
        'categorySlug': 'algorithms',
        'skip': SKIP_PROBLEMS,
        'limit': LIMIT_PROBLEMS,
        'filters': FILTERS,
    },
    'query': '''query problemsetQuestionList(
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
                frontendQuestionId: questionFrontendId
                title
                acRate
                difficulty
            }
        }
    }''',
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_api_answer() -> dict:
    try:
        response = requests.post(ENDPOINT, json=PAYLOAD)
        if response.status_code != requests.codes.ok:
            message = (
                f'Эндпоинт {ENDPOINT} недоступен.\n'
                f'Код ответа: {response.status_code}.'
            )
            raise EndpointError(message)
        return response.json()
    except Exception as error:
        message = (
            f'Произошёл сбой при запросе к эндпоинту {ENDPOINT}\n'
            f'Ошибка: {error}'
        )
        raise RequestError(message)


def get_problems(response: dict) -> list[dict]:
    try:
        problems = response['data']['problemsetQuestionList']['questions']
    except KeyError as error:
        message = f'В response отсутствует ключ: {error}.'
        raise KeyError(message)
    if not isinstance(problems, list):
        raise TypeError('questions не является списком.')
    return problems


def parse_problem(problem: dict) -> tuple[str, str, float, str]:
    try:
        problem_id = problem['frontendQuestionId']
        title = problem['title']
        acceptance = round(problem['acRate'], 1)
        difficulty = problem['difficulty'].lower()
    except KeyError as error:
        message = f'В problem отсутствует ключ: {error}.'
        raise KeyError(message)
    return problem_id, title, acceptance, difficulty


def main():
    logger.info('Скрипт запущен.')
    try:
        response = get_api_answer()
        problems = get_problems(response)
        with open(DEFAULT_FILENAME, 'w', encoding="utf-8") as file:
            logger.info('Началась запись данных.')
            writer = csv.writer(file)
            writer.writerow(FIELD_NAMES)
            for problem in problems:
                writer.writerow(parse_problem(problem))
            logger.info('Данные успешно записаны.')
        logger.info('Скрипт завершил работу.')
    except Exception as error:
        message = f'Сбой в работе программы: {error}.\n Программа остановлена.'
        logger.error(message)
        sys.exit()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        filename='parser.log',
        filemode='a',
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%d-%b-%y %H:%M:%S',
        encoding='utf-8',
    )
    main()
