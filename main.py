import csv
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

URL = 'https://leetcode.com/problemset/algorithms/?page=42/'
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
    # driver = webdriver.Chrome()
    # driver.implicitly_wait(15)
    # driver.get(URL)
    # WebDriverWait(driver, 15)3
    session = HTMLSession()
    response = session.get(url=URL)
    response.html.render()
    print(response.html.raw_html)

    # response = requests.get(URL, timeout=(5, 15), stream=True)
    # soup = BeautifulSoup(response.html.raw_html, features='html.parser')
    # table = soup.find(role='rowgroup')
    # rows = parse_rows(table)
    # print(rows)


    # with open(DEFAULT_FILENAME, 'w') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(FIELD_NAMES)
    #     writer.writerows(rows)


if __name__ == '__main__':
    main()
