from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, StringField, TextAreaField, SubmitField, IntegerField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Regexp
from app.models import User, Post

class LoginForm(FlaskForm):
    
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])

    # The below regex string was taken from a stack overflow post about the topic of strong password regex
    # Taken from Stack Overflow post by Avinash Raj 05/02/2015 and modified to suit my own needs
    # Accessed 18/01/2023
    # https://stackoverflow.com/questions/28334506/match-password-with-python-regex
    password = PasswordField('Password', validators=[DataRequired(), Length(min = 8, max = 16, message = "Your password must be between 8 and 16 characters long"), Regexp('^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$!£$%])[\w\d@#$!£$%]{8,16}$',message='Your password should be between 8 and 16 characters long, and contain at least one uppercase letter, one lowercase letter, one digit, and one of the following symbols: @#$!£$%.')])
    # End of referenced code

    password2 = PasswordField('Please retype your password', validators=[DataRequired(), EqualTo('password', message = 'Passwords do not match. Please try again.'), ])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('That username is taken. Please choose a different username')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('That email address is already registered.')

class RequestPasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email registered')

class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min = 8, max = 16, message = "Your password must be between 8 and 16 characters long"), Regexp('^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$!£$%])[\w\d@#$!£$%]{8,16}$',message='Your password should be between 8 and 16 characters long, and can contain at least one uppercase letter, one lowercase letter, one digit, and one of the following symbols: @#$!£$%.')])
    password2 = PasswordField('Please retype your new password', validators=[DataRequired(), EqualTo('password', message = 'Passwords do not match. Please try again.'), ])
    submit = SubmitField('Update Password')

class GetInTouchForm(FlaskForm):
    name = TextAreaField('Name')
    email_address = TextAreaField('Email (for reference)')
    content = TextAreaField('Message')
    submit = SubmitField('Send')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max =140)])
    submit = SubmitField('Submit')

    # Code to allow users to change their username
    # Taken from The Flask Mega-Tutorial by Miguel Grinberg
    # Accessed 18/01/2023
    # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-error-handling
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('That username is already taken. Please choose a different one.')
    # End of referenced code

class PostForm1(FlaskForm):
    post = TextAreaField('Leave a comment', validators = [DataRequired(), Length(min = 1, max = 300)])
    submit1 = SubmitField('Post comment')

class PostForm2(FlaskForm):
    post = TextAreaField('Leave a comment', validators = [DataRequired(), Length(min = 1, max = 300)])
    submit2 = SubmitField('Post comment')

class PostForm3(FlaskForm):
    post = TextAreaField('Leave a comment', validators = [DataRequired(), Length(min = 1, max = 300)])
    submit3 = SubmitField('Post comment')

class Code_example_1_form(FlaskForm):
    amount = FloatField('Please enter an amount: ', validators= [DataRequired()])
    coins = IntegerField('Please enter the amount of coins: ', validators= [DataRequired()])
    submit = SubmitField('Run')

class Code_example_2_form(FlaskForm):
    string = TextAreaField('Please enter a string of at least 5 characters with no spaces: ', validators= [DataRequired(), Length(min = 5, max= 15)])
    submit = SubmitField('Run')

class File_upload_form(FlaskForm):
    upload = FileField('File', validators=[FileRequired(), FileAllowed(['txt'], 'Invalid File Type. Must be .txt')])
    submit = SubmitField('Upload')

