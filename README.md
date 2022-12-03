# Leetcode parser

This is a test task for the company [BestPlace](https://bestplace.ai/).

Task description is [here](bestplace_leetcode.pdf).

The script parses all algorithmic problems from [Leetcode.com](https://leetcode.com/problemset/algorithms/) website and writes them in a .csv file.

An example of how the script works on the first 10 tasks can be viewed [here](leetcode_problems.csv).

## Technologies:
```
Python 3.10
Requests 2.28.1 
```

## Installation

1) Clone repo:

```console
git clone https://github.com/hilaaba/leetcode_parser
```
```console
cd leetcode_parser
```

2) Initialize and start virtual environment with:

```console
python3 -m venv venv
```
```console
source venv/bin/activate
```

3) Install dependencies:

```console
python3 -m pip install --upgrade pip
```
```console
python3 -m pip install -r requirements.txt
```

## Usage

```console
python3 main.py
```

## Testing

```console
python3 tests.py
```

Script will save parsed data in .csv file (by default called 'leetcode_problems.csv') and place it into project directory.
