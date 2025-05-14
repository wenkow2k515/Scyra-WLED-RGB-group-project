from app import db
from app.models import User
from app.forms import RegisterForm, LoginForm
from werkzeug.security import check_password_hash, generate_password_hash

def try_to_login(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return user
    return None

def try_to_register(email, password, fname, lname, secret_question=None, secret_answer=None):
    if User.query.filter_by(email=email).first():
        return None  # User already exists
    hashed_password = generate_password_hash(password)
    user = User(
        email=email,
        password=hashed_password,
        fname=fname,
        lname=lname,
        secret_question=secret_question,
        secret_answer=secret_answer
    )
    db.session.add(user)
    db.session.commit()
    return user
