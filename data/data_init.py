from sqlalchemy import DDL, event, text
from sqlalchemy.exc import IntegrityError

from data.database import session as db, Base, engine
from data.models import User
from security.auth_handler import encrypt_password


def init_data():
    Base.metadata.create_all(engine)
    try:
        init_admin()
    except IntegrityError:
        db.rollback()
    init_stored_procedures()
    init_triggers()


def init_admin():
    db.add(User(
        "admin",
        encrypt_password("admin"),
        True
    ))
    db.commit()


def init_stored_procedures():
    save_question_log_sp = text(
        """CREATE PROCEDURE sp_saveQuestionLog(
                IN $questionId INT,
                IN $question VARCHAR(255),
                IN $method VARCHAR(255)
            )
            
            BEGIN
            
                INSERT INTO QUESTION_LOG(
                    question_id,
                    question,
                    method
                )
                VALUES(
                    $questionId,
                    $question,
                    $method
                );
                
            END""")
    save_user_log_sp = text(
        """CREATE PROCEDURE sp_saveUserLog(
                IN $userId INT,
                IN $username VARCHAR(255),
                IN $method VARCHAR(255)
            )

            BEGIN

                INSERT INTO USER_LOG(
                    user_id,
                    username,
                    method
                )
                VALUES(
                    $userId,
                    $username,
                    $method
                );

            END""")
    db.execute(text("DROP PROCEDURE IF EXISTS sp_saveQuestionLog;"))
    db.execute(text("DROP PROCEDURE IF EXISTS sp_saveUserLog;"))
    db.execute(save_question_log_sp)
    db.execute(save_user_log_sp)
    db.commit()


def init_triggers():
    question_insert_trigger = text(
        """CREATE TRIGGER t_saveQuestion
        AFTER INSERT ON QUESTION FOR EACH ROW	
            BEGIN
                CALL sp_saveQuestionLog(
                    NEW.ID, 
                    NEW.QUESTION, 
                    'INSERT'
                );
            END
                    """)
    question_update_trigger = text(
        """CREATE TRIGGER t_updateQuestion
            AFTER UPDATE ON QUESTION FOR EACH ROW	
            BEGIN
                CALL sp_saveQuestionLog(
                    NEW.ID, 
                    NEW.QUESTION, 
                    'UPDATE'
                );
            END
        """
    )
    question_delete_trigger = text(
        """
        CREATE TRIGGER t_deleteQuestion
        BEFORE DELETE ON QUESTION FOR EACH ROW	
        BEGIN
            CALL sp_saveQuestionLog(
                OLD.ID, 
                OLD.QUESTION, 
                'DELETE'
            );
        END"""
    )
    user_insert_trigger = text(
        """
        CREATE TRIGGER t_saveUser
        AFTER INSERT ON USER FOR EACH ROW	
        BEGIN
            CALL sp_saveUserLog(
                NEW.ID, 
                NEW.USERNAME, 
                'INSERT'
            );
        END
        """
    )
    user_update_trigger = text(
        """
        CREATE TRIGGER t_updateUser
        AFTER UPDATE ON USER FOR EACH ROW	
        BEGIN
            CALL sp_saveUserLog(
                NEW.ID, 
                NEW.USERNAME, 
                'UPDATE'
            );
        END
        """
    )
    user_delete_trigger = text(
        """
        CREATE TRIGGER t_deleteUser
        BEFORE DELETE ON USER FOR EACH ROW	
        BEGIN
            CALL sp_saveUserLog(
                OLD.ID, 
                OLD.USERNAME, 
                'DELETE'
            );
        END"""
    )
    db.execute(text("DROP TRIGGER IF EXISTS t_saveQuestion;"))
    db.execute(text("DROP TRIGGER IF EXISTS t_updateQuestion;"))
    db.execute(text("DROP TRIGGER IF EXISTS t_deleteQuestion;"))
    db.execute(text("DROP TRIGGER IF EXISTS t_saveUser;"))
    db.execute(text("DROP TRIGGER IF EXISTS t_updateUser;"))
    db.execute(text("DROP TRIGGER IF EXISTS t_deleteUser;"))
    db.commit()
    db.execute(question_insert_trigger)
    db.execute(question_update_trigger)
    db.execute(question_delete_trigger)
    db.execute(user_insert_trigger)
    db.execute(user_update_trigger)
    db.execute(user_delete_trigger)
    db.commit()
