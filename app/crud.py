import datetime

from sqlalchemy import update, MetaData
from typing import Dict, Any

from app.schema import Logs, Feedbacks
from app.models import Log, Feedback
from app.database import SessionLocal, engine


db = SessionLocal()


def add_logs(log: Logs):
    new_log = Log(
        timestamp=datetime.datetime.now(),
        question=log.question,
        question_id=log.question_id,
        context_id=log.context_id,
        context_source=log.context_source
    )
    db.add(new_log)
    try:
        db.commit()
    except:
        db.rollback()


def add_feedback(feedback: Feedbacks):
    feed_back = Feedback(
        timestamp=datetime.datetime.now(),
        question_id=feedback.question_id,
        question=feedback.question,
        person=feedback.person,
        answer=feedback.answer,
        feedback=feedback.feedback,
    )
    db.add(feed_back)
    try:
        db.commit()
    except:
        db.rollback()


def update_feedback(feedback: Dict[Any, Any]):
    db.query(Feedback).filter(Feedback.question_id ==
                              feedback.question_id).update({'feedback': feedback.feedback})
    try:
        db.commit()
    except:
        db.rollback()



