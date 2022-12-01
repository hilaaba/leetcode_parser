from enum import Enum
from decimal import Decimal

from main import get_api_answer


from pydantic import BaseModel, Field


class Difficulty(str, Enum):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'


class Question(BaseModel):
    id: int = Field(..., alias='frontendQuestionId')
    title: str
    acceptance: Decimal = Field(..., alias='acRate')
    difficulty: Difficulty


class ProblemsetQuestionList(BaseModel):
    questions: list[Question] = Field(..., alias='problemsetQuestionList')


class DataModel(BaseModel):
    data: dict


if __name__ == '__main__':
    response = get_api_answer()
    print(response)
    data = DataModel(**response)
    data.dict()
    print(data.dict())
