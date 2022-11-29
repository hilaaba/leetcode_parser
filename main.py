import requests
from bs4 import BeautifulSoup

URL = 'https://leetcode.com/problemset/algorithms/'
FIELD_NAMES = ['id', 'title', 'acceptance', 'difficulty']
DEFAULT_FILENAME = 'leetcode_problems.csv'

