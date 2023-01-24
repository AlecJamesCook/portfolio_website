from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import db, login, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default = datetime.utcnow)
    is_admin = db.Column(db.Boolean, nullable = False, default = False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Code to automatically generate user profile pictures
    # Taken from The Flask Mega-Tutorial by Miguel Grinberg
    # Accessed 18/01/2023
    # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vi-profile-page-and-avatars
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)
    # End of referenced code

    # Code to create reset password tokens
    # Created by following The Python Flask tutorial series by Corey Schafer (Episode 10: Email and Password Reset)
    # Accessed 18/01/2023
    # https://www.youtube.com/watch?v=vutyTx7IaAI&t=1955s
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    # End of referenced code

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    tag = db.Column(db.String(32))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Education(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    time_period = db.Column(db.String(16))
    school_name = db.Column(db.String(32))
    qualifications = db.Column(db.String(64))
    subject_1 = db.Column(db.String(32))
    subject_1_desc = db.Column(db.String(1000))
    subject_2 = db.Column(db.String(32))
    subject_2_desc = db.Column(db.String(1000))
    subject_3 = db.Column(db.String(32))
    subject_3_desc = db.Column(db.String(1000))
    subject_4 = db.Column(db.String(32))
    subject_5 = db.Column(db.String(32))
    subject_6 = db.Column(db.String(32))
    subject_7 = db.Column(db.String(32))
    subject_8 = db.Column(db.String(32))
    subject_9 = db.Column(db.String(32))
    subject_10 = db.Column(db.String(32))
    photo = db.Column(db.String(32))

    def __repr__(self):
        return '<Education {}>'.format(self.school_name)

class Work_experience(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    company_name = db.Column(db.String(32))
    job_title = db.Column(db.String(64))
    time_period = db.Column(db.String(32))
    location = db.Column(db.String(16))
    body_1 = db.Column(db.String(500))
    body_2 = db.Column(db.String(500))
    body_3 = db.Column(db.String(500))
    body_4 = db.Column(db.String(500))
    skill_1 = db.Column(db.String(64))
    skill_2 = db.Column(db.String(64))
    skill_3 = db.Column(db.String(64))
    skill_4 = db.Column(db.String(64))
    photo = db.Column(db.String(32))

    def __repr__(self):
        return '<Work Experience {}>'.format(self.company_name)

class Computing(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    module_code = db.Column(db.String(16))
    module_name = db.Column(db.String(100))
    module_leader = db.Column(db.String(32))
    module_description = db.Column(db.String(700))
    skill_1 = db.Column(db.String(100))
    skill_2 = db.Column(db.String(100))
    skill_3 = db.Column(db.String(100))
    assessment_1 = db.Column(db.String(500))
    assessment_2 = db.Column(db.String(500))
    link = db.Column(db.String(100))

    def __repr__(self):
        return '<Computing {}>'.format(self.module_name)

class Code_examples(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    function_name = db.Column(db.String(64))
    function_desc = db.Column(db.String(300))
    param_1_name =  db.Column(db.String(64))
    param_1_desc = db.Column(db.String(200))
    param_2_name = db.Column(db.String(64))
    param_2_desc = db.Column(db.String(200))
    return_type_name = db.Column(db.String(64))
    return_type_desc = db.Column(db.String(200))

    def __repr__(self):
        return '<Code Examples {}>'.format(self.function_name)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

