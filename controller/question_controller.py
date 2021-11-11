from fastapi import APIRouter, Depends
from sqlalchemy import func

from data.models import User, Question, QuestionDto
from errorresponses.error_responses import no_data_exception, forbidden_exception
from security.auth_handler import get_current_user
from data.database import session as db

router = APIRouter()


@router.get("/api/question/get", response_model=QuestionDto)
async def get_question(current_user: User = Depends(get_current_user)):
    question = db.query(Question).order_by(func.rand()).first()
    if question is not None:
        return question
    raise no_data_exception


@router.get("/api/question/get/all", response_model=QuestionDto)
async def get_questions(current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        questions = db.query(Question).all()
        return questions
    else:
        raise forbidden_exception


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


@router.delete("/api/question/delete/{question_id}")
async def delete_question(question_id: int, current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        question = db.query(Question).filter(Question.id == question_id).first()
        if question is not None:
            db.delete(question)
            db.commit()
    else:
        raise forbidden_exception
