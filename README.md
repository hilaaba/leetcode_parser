# Leetcode parser

This is a test task for the company [BestPlace](https://bestplace.ai/).
Task description is [here](bestplace_leetcode.pdf).
Parses code tasks from leetcode.com website and writes them in a .csv file.

## Installation

1) Clone repo:

`$ git clone https://github.com/hilaaba/leetcode_parser`
`$ cd leetcode_parser`

2) Initialize and start virtual environment with:

`$ python3 -m venv venv`
`$ source venv/bin/activate`

3) Install dependencies:

`$ python3 -m pip install --upgrade pip`
`$ python3 -m pip install -r requirements.txt`

## Usage

`$ python3 main.py`

***

Script will save parsed data in .csv file (by default called 'leetcode_problems.csv') and place it into project directory.