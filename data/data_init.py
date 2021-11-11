from data.database import session as db, Base, engine
from data.models import User
from security.auth_handler import encrypt_password


def init_data():
    Base.metadata.create_all(engine)
    # init_admin()


def init_admin():
    db.add(User(
        "admin",
        encrypt_password("admin"),
        True
    ))
    db.commit()
