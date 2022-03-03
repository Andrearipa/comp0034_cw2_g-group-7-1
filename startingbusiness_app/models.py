from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from startingbusiness_app import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(12), nullable=False)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    account_type = db.Column(db.String, nullable=False)
    posts = db.relationship('Blog', backref='author', lazy=True)
    #profile_image =db.column(db.) ??? store in string?

    def __repr__(self):
        return f"{self.id} {self.first_name} {self.last_name} {self.user_name} {self.email} {self.password} {self.account_type}"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Blog(db.Model):
    __tablename__ = "blog"
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return f"{self.title} {self.date_posted} "
