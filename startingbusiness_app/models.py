from werkzeug.security import generate_password_hash, check_password_hash
from startingbusiness_app import login_manager
from startingbusiness_app import db
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    account_type = db.Column(db.Text, nullable=False)
    profile_image = db.Column(db.String(60), nullable=False, default='startingbusiness_app/user/static/default.jpg')

    def __repr__(self):
        return f"{self.id} {self.first_name} {self.last_name} {self.email} {self.password} {self.account_type} {self.profile_image}"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

