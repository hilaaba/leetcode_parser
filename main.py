import csv
import logging
import sys

import requests

from exceptions import EndpointError, RequestError

ENDPOINT = 'https://leetcode.com/graphql'
FIELD_NAMES = ('id', 'title', 'acceptance', 'difficulty')
DEFAULT_FILENAME = 'leetcode_problems.csv'

CATEGORY = 'algorithms'
SKIP_PROBLEMS = 0
LIMIT_PROBLEMS = 2500
FILTERS = dict()

GRAPHQL_QUERY = {
    'variables': {
        'categorySlug': CATEGORY,
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
    """Sends a POST request to the endpoint.

    Returns:
        The return dict of data.

    Raises:
        EndpointError: If endpoint not available.

    """
    try:
        response = requests.post(ENDPOINT, json=GRAPHQL_QUERY)
        if response.status_code != requests.codes.ok:
            message = (
                f'Endpoint {ENDPOINT} not available.\n'
                f'Status code: {response.status_code}'
            )
            raise EndpointError(message)
        return response.json()
    except Exception as error:
        message = (
            f'Error occurred while trying to request the endpoint: {ENDPOINT}'
            f'\nError: {error}'
        )
        raise RequestError(message)


def get_problems(response: dict) -> list[dict]:
    """Get a leetcode problems list of data.

    Args:
        response: Data received from the request.

    Returns:
        The return a list of leetcode problems.

    Raises:
        KeyError: An error occurred get value of key "data" or
        "problemsetQuestionList" or "questions".
        TypeError: The value of "questions" not a list.

    """
    try:
        problems = response['data']['problemsetQuestionList']['questions']
    except KeyError as error:
        message = f'The response is missing key: {error}.'
        raise KeyError(message)
    if not isinstance(problems, list):
        raise TypeError('The value of "questions" not a list.')
    return problems


def parse_problem(problem: dict) -> tuple[str, str, float, str]:
    """Parse id, title, acceptance and difficulty of leetcode problem.

    Args:
        problem: A dict where key-value is data of leetcode problem.

    Returns:
        The return a tuple of values id, title, acceptance and difficulty.

    Raises:
        KeyError: An error occurred get value of key "frontendQuestionId",
        "title", "acRate" or "difficulty".

    """
    try:
        problem_id = problem['frontendQuestionId']
        title = problem['title']
        acceptance = round(problem['acRate'], 1)
        difficulty = problem['difficulty'].lower()
    except KeyError as error:
        message = f'The problem is missing a key: {error}.'
        raise KeyError(message)
    return problem_id, title, acceptance, difficulty


def main():
    """The main logic of the script."""
    logger.info('The script is running.')
    try:
        response = get_api_answer()
        problems = get_problems(response)
        with open(DEFAULT_FILENAME, 'w', encoding="utf-8") as file:
            logger.info('Data recording has begun.')
            writer = csv.writer(file)
            writer.writerow(FIELD_NAMES)
            for problem in problems:
                writer.writerow(parse_problem(problem))
            logger.info('The data was successfully written.')
        logger.info('The script has completed.')
    except Exception as error:
        message = f'Program crash: {error}.\nThe program has stopped.'
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
