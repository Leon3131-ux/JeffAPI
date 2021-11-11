from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import func

from data.models import User, Question, QuestionDto, QuestionRatingIn, QuestionRating, QuestionRatingOut
from errorresponses.error_responses import no_data_exception, forbidden_exception, bad_request
from security.auth_handler import get_current_user
from data.database import session as db

router = APIRouter()


@router.get("/api/question/get", response_model=QuestionDto)
async def get_question(current_user: User = Depends(get_current_user)):
    question = db.query(Question).order_by(func.rand()).first()
    if question is not None:
        return question
    raise no_data_exception


@router.get("/api/question/all", response_model=List[QuestionDto])
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


@router.post("/api/question/rate", response_model=QuestionRatingOut)
async def rate_question(rating_dto: QuestionRatingIn, current_user: User = Depends(get_current_user)):
    question = db.query(Question).filter(Question.id == rating_dto.question_id).first()
    if question is not None:
        question_rating = QuestionRating(question_id=rating_dto.question_id, user_id=current_user.id,
                                         rating=rating_dto.rating)
        db.add(question_rating)
        db.flush()
        db.commit()
        db.expire(question)
        return to_question_rating_out(question, current_user, question_rating)
    else:
        raise bad_request


@router.get("/api/question/rating/user/{user_id}", response_model=List[QuestionRatingOut])
async def get_ratings_by_user(user_id: int, current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        question_ratings = db.query(QuestionRating).filter(QuestionRating.user_id == user_id).all()
        question_ratings_out = []
        for question_rating in question_ratings:
            question_ratings_out.append(
                to_question_rating_out(question_rating.question, question_rating.user, question_rating))
        return question_ratings_out
    else:
        raise forbidden_exception


@router.get("/api/question/rating/question/{question_id}", response_model=List[QuestionRatingOut])
async def get_ratings_by_question(question_id: int, current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        question_ratings = db.query(QuestionRating).filter(QuestionRating.question_id == question_id).all()
        question_ratings_out = []
        for question_rating in question_ratings:
            question_ratings_out.append(
                to_question_rating_out(question_rating.question, question_rating.user, question_rating))
        return question_ratings_out
    else:
        raise forbidden_exception


@router.get("/api/question/rating/me", response_model=List[QuestionRatingOut])
async def get_ratings_by_current_user(current_user: User = Depends(get_current_user)):
    question_ratings = db.query(QuestionRating).filter(QuestionRating.user_id == current_user.id).all()
    question_ratings_out = []
    for question_rating in question_ratings:
        question_ratings_out.append(
            to_question_rating_out(question_rating.question, question_rating.user, question_rating))
    return question_ratings_out


def to_question_rating_out(question: Question, user: User, question_rating: QuestionRating):
    question_rating_out = QuestionRatingOut(
        question_id=question.id,
        question=question.question,
        user_id=user.id,
        rating=question_rating.rating
    )
    return question_rating_out
