from fastapi import APIRouter, Depends
from sqlalchemy import func

from data.models import User, Question, QuestionDto
from errorresponses.error_responses import no_data_exception, forbidden_exception
from security.auth_handler import get_current_user
from data.database import session as db

router = APIRouter()


@router.get("/api/question", response_model=QuestionDto)
async def get_question(current_user: User = Depends(get_current_user)):
    question = db.query(Question).order_by(func.rand()).first()
    if question is not None:
        return question
    raise no_data_exception


@router.post("/api/question/save", response_model=QuestionDto)
async def save_question(question_dto: QuestionDto, current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        question = db.query(Question).filter(Question.id == question_dto.id).first()
        if question is not None:
            question.question = question_dto.question
        else:
            question = Question(question=question_dto.question)
            db.add(question)
        db.flush()
        db.commit()
        return question
    else:
        raise forbidden_exception
