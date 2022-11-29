import csv
import re

import requests
from bs4 import BeautifulSoup

URL = 'https://leetcode.com/problemset/algorithms/?page=2/'
FIELD_NAMES = ('id', 'title', 'acceptance', 'difficulty')
DEFAULT_FILENAME = 'leetcode_problems.csv'


def parse_rows(table: BeautifulSoup) -> list:
    rows = []
    for row in table.contents:
        tmp = []
        for cell in row.contents:
            if not cell.text:
                continue
            elif re.match(r'\d+\. \w', cell.text):
                id, title = cell.text.split('. ')
                tmp.append(int(id))
                tmp.append(title)
            elif re.match(r'\d+\.\d%', cell.text):
                tmp.append(float(cell.text[:-1]))
            else:
                tmp.append(cell.text.lower())
        rows.append(tmp)
    return rows


def main():
    page = 42
    response = requests.get(URL, params={'page': page}, allow_redirects=True)
    print(response.status_code)
    soup = BeautifulSoup(response.text, features='html.parser')
    table = soup.find(role='rowgroup')
    rows = parse_rows(table)
    print(rows)
    with open(DEFAULT_FILENAME, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(FIELD_NAMES)
        writer.writerows(rows)


if __name__ == '__main__':
    main()
