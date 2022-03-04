from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from startingbusiness_app.config import Config
from startingbusiness_app import db
from jose import jws
from json import loads

from startingbusiness_app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    # user_name = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    account_type = db.Column(db.Text, nullable=False)
    posts = db.relationship('Blog', backref='author', lazy=True)
    #profile_image =db.column(db.) ??? store in string?

    def __repr__(self):
        return f"{self.id} {self.first_name} {self.last_name} {self.email} {self.password} {self.account_type}"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_token(self):
        secret = Config.SECRET_KEY
        to_decode = {'user_id': self.id}
        token = jws.sign(to_decode, secret, algorithm='HS256')
        return token

    @staticmethod
    def verify_token(token):
        secret = Config.SECRET_KEY
        try:
            token_result = jws.verify(token, secret, algorithms=['HS256'])
            user_id = loads(token_result)['user_id']
        except:
            return None
        return User.query.get(user_id)



class Blog(db.Model):
    __tablename__ = "blog"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return f"{self.title} {self.date_posted} "
