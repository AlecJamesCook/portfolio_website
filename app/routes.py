from flask import render_template, flash, redirect, url_for, request, abort, send_file
from app import app, db, mail
from app.forms import LoginForm, RegistrationForm, EditProfileForm, Code_example_1_form, Code_example_2_form, File_upload_form, PostForm1, PostForm2, PostForm3, PostForm4, RequestPasswordResetForm, PasswordResetForm, GetInTouchForm, Wan_wang_form
from app.models import User, Post, Work_experience, Education, Computing, Code_examples
from app.static.python.code_examples import change_please, five_letter_unscramble, document_stats, wanWang
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Message
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from datetime import datetime
import os

# Code for displaying when user was last logged in
# Taken from The Flask Mega Tutorial by Miguel Grinberg
# Accessed on 18/10/2023
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xii-dates-and-times
@app.before_request
def before_request():

    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
# End of referenced code

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():

    form = GetInTouchForm()

    def GetInTouchEmail(form):
        email = 'alecjamescook@hotmail.co.uk'
        msg = Message('Someone wants to get in touch!', sender ='aleccookportfolio@gmail.com', recipients = [email])
        msg.body = "Name: {name} - Email: {email_address} - Content: {content}".format(
        name=form.name.data,
        email_address=form.email_address.data,
        content=form.content.data
    )
        mail.send(msg)

        return render_template('index.html', title = 'Home', form = form)

    if form.validate_on_submit():
        GetInTouchEmail(form)
        flash('Email sent!')
        return redirect(url_for('index'))

    return render_template('index.html', title = 'Home', form = form)

@app.route('/download')
def download():
    path = (os.path.join(app.config['DOWNLOADS'], 'Alec_Cook_CV.pdf'))
    return send_file(path, as_attachment=True)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password. Please try again')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        # Secutiy feature to prevent linking to a malicious site by an attacker
        # Taken from The Flask Mega-Tutorial by Miguel Grinberg
        # Accessed 18/01/2023
        # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        # End of referenced code
        return redirect(url_for('index'))

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():

    logout_user()
    flash('Successfully logged out. See you next time!')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Regitstration successful!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):

    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.timestamp.desc())

    return render_template('user.html', user=user, posts = posts)

@app.route('/edit_profile', methods = ['GET', 'POST'])
def edit_profile():

    form = EditProfileForm(current_user.username)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Profile updated')
        return redirect(url_for('edit_profile'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',form=form)

# Code to handle password reset requests
# Created by following The Python Flask tutorial series by Corey Schafer (Episode 10: Email and Password Reset)
# Accessed 18/01/2023
# https://www.youtube.com/watch?v=vutyTx7IaAI&t=1955s
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender ='aleccookportfolio@gmail.com', recipients = [user.email])
    msg.body = f''' To reset your password, visit the following link: {url_for('reset_token', token = token, _external = True)}

    Ignore this email if you did not make this request.
    '''
    mail.send(msg)

@app.route("/reset_password", methods = ['GET', 'POST'])
def reset_request():

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RequestPasswordResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password. Please make sure to check your spam/junk folder', 'info')
        return redirect(url_for('login'))

    return render_template('reset_request.html', title = 'Reset Password', form = form)

@app.route("/reset_password/<token>", methods = ['GET', 'POST'])
def reset_token(token):

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    user = User.verify_reset_token(token)

    if user is None:
        flash('Token is invalid or expired', 'warning')
        return redirect(url_for('reset_request'))

    form = PasswordResetForm()

    if form.validate_on_submit():

        user.set_password(form.password.data)
        db.session.commit()
        flash('Password updated!', 'success')
        return redirect(url_for('login'))

    return render_template('reset_token.html', title = 'Reset Password', form = form)

# End of referenced code

@app.route('/education')
def education():

    education_1 = Education.query.filter_by(id=1).first()
    education_2 = Education.query.filter_by(id=2).first()
    education_3 = Education.query.filter_by(id=3).first()
    education_4 = Education.query.filter_by(id=4).first()

    # Created these as separate variables so they could be used with {{ url_for.. }}
    education_1_photo = education_1.photo
    education_2_photo = education_2.photo
    education_3_photo = education_3.photo
    education_4_photo = education_4.photo

    return render_template(
        'education.html',
        title = 'Education',
        education_1 = education_1,
        education_1_photo = education_1_photo,
        education_2 = education_2,
        education_2_photo = education_2_photo,
        education_3 = education_3,
        education_3_photo = education_3_photo,
        education_4 = education_4,
        education_4_photo = education_4_photo
        )

@app.route('/work_experience')
def work_experience():

    job_1 = Work_experience.query.filter_by(id=1).first()
    job_2 = Work_experience.query.filter_by(id=2).first()
    job_3 = Work_experience.query.filter_by(id=3).first()
    job_4 = Work_experience.query.filter_by(id=4).first()
    job_5 = Work_experience.query.filter_by(id=5).first()
    job_6 = Work_experience.query.filter_by(id=6).first()
    job_7 = Work_experience.query.filter_by(id=7).first()

    # Created these as separate variables so they could be used with {{ url_for.. }}
    job_1_photo = job_1.photo
    job_2_photo = job_2.photo
    job_3_photo = job_3.photo
    job_4_photo = job_4.photo
    job_5_photo = job_5.photo


    return render_template(
        'work_experience.html',
        title = 'Work Experience',
        job_1 = job_1,
        job_1_photo = job_1_photo,
        job_2 = job_2,
        job_2_photo = job_2_photo,
        job_3 = job_3,
        job_3_photo = job_3_photo,
        job_4 = job_4,
        job_4_photo = job_4_photo,
        job_5 = job_5,
        job_5_photo = job_5_photo,
        job_6 = job_6,
        job_7 = job_7,
        )

@app.route('/computing')
def computing():

    module_1 = Computing.query.filter_by(id=1).first()
    module_2 = Computing.query.filter_by(id=2).first()
    module_3 = Computing.query.filter_by(id=3).first()
    module_4 = Computing.query.filter_by(id=4).first()
    module_5 = Computing.query.filter_by(id=5).first()
    module_6 = Computing.query.filter_by(id=6).first()

    return render_template(
        'computing.html',
        title = 'MSc Computing',
        module_1 = module_1,
        module_2 = module_2,
        module_3 = module_3,
        module_4 = module_4,
        module_5 = module_5,
        module_6 = module_6)

@app.route('/code_examples', methods = ['GET', 'POST'])
def code_examples():

    # Code example variables
    code_example_1_form = Code_example_1_form()
    code_example_2_form = Code_example_2_form()
    file_upload_form = File_upload_form()
    code_example_4_form = Wan_wang_form()

    code_example_1 = Code_examples.query.filter_by(id=1).first()
    code_example_2 = Code_examples.query.filter_by(id=2).first()
    code_example_3 = Code_examples.query.filter_by(id=3).first()
    code_example_4 = Code_examples.query.filter_by(id=4).first()

    # Comment section variables
    change_please_form = PostForm1()
    five_letter_unscramble_form = PostForm2()
    document_statistics_form = PostForm3()
    wan_wang_form = PostForm4()

    change_please_comments = Post.query.filter_by(tag = "change_please").order_by(Post.timestamp.desc()).all()
    five_letter_unscramble_comments = Post.query.filter_by(tag = "five_letter_unscramble").order_by(Post.timestamp.desc()).all()
    document_statistics_comments = Post.query.filter_by(tag = "document_unscramble").order_by(Post.timestamp.desc()).all()
    wan_wang_comments = Post.query.filter_by(tag = "wan_wang").order_by(Post.timestamp.desc()).all()

    # Handling the different forms
    if change_please_form.submit1.data and change_please_form.validate():

        if current_user.is_anonymous:

            flash('You must be logged in to leave a comment')
            return redirect(url_for('code_examples'))

        change_please_post = Post(body = change_please_form.post.data, tag = "change_please", author = current_user)
        db.session.add(change_please_post)
        db.session.commit()
        flash('Comment posted!')

        return redirect(url_for('code_examples'))

    if five_letter_unscramble_form.submit2.data and five_letter_unscramble_form.validate():

        if current_user.is_anonymous:

            flash('You must be logged in to leave a comment')
            return redirect(url_for('code_examples'))

        five_letter_unscramble_post = Post(body = five_letter_unscramble_form.post.data, tag = "five_letter_unscramble", author = current_user)
        db.session.add(five_letter_unscramble_post)
        db.session.commit()
        flash('Comment posted!')

        return redirect(url_for('code_examples'))

    if document_statistics_form.submit3.data and document_statistics_form.validate():

        if current_user.is_anonymous:

            flash('You must be logged in to leave a comment')
            return redirect(url_for('code_examples'))

        document_statistics_post = Post(body = document_statistics_form.post.data, tag = "document_unscramble", author = current_user)
        db.session.add(document_statistics_post)
        db.session.commit()
        flash('Comment posted')

        return redirect(url_for('code_examples'))

    if wan_wang_form.submit4.data and wan_wang_form.validate():

        if current_user.is_anonymous:

            flash('You must be logged in to leave a comment')
            return redirect(url_for('code_examples'))

        wan_wang_post = Post(body = wan_wang_form.post.data, tag = "wan_wang", author = current_user)
        db.session.add(wan_wang_post)
        db.session.commit()
        flash('Comment posted')

        return redirect(url_for('code_examples'))

    if code_example_1_form.validate_on_submit():

        amount = code_example_1_form.amount.data
        coins = code_example_1_form.coins.data
        code_example_1_res = change_please(amount, coins)
        flash('Computed! Please scroll down to see your results')

        return render_template(
        'code_examples.html',
        title = 'Code Examples',
        code_example_1_form = code_example_1_form,
        code_example_2_form = code_example_2_form,
        file_upload_form = file_upload_form,
        code_example_4_form = code_example_4_form,
        change_please_form = change_please_form,
        change_please_comments = change_please_comments,
        five_letter_unscramble_form = five_letter_unscramble_form,
        five_letter_unscramble_comments = five_letter_unscramble_comments,
        document_statistics_form = document_statistics_form,
        document_statistics_comments = document_statistics_comments,
        wan_wang_form = wan_wang_form,
        wan_wang_comments = wan_wang_comments,
        code_example_1 = code_example_1,
        code_example_2 = code_example_2,
        code_example_3 = code_example_3,
        code_example_4 = code_example_4,
        code_example_1_res = code_example_1_res,
        amount = amount,
        coins = coins
        )

    if code_example_2_form.validate_on_submit():

        string = code_example_2_form.string.data
        code_example_2_res = five_letter_unscramble(string)
        number_matching_words = 0

        for i in code_example_2_res:
            number_matching_words += 1

        flash('Search completed! Please scroll down to see your results')

        return render_template(
        'code_examples.html',
        title = 'Code Examples',
        code_example_1_form = code_example_1_form,
        code_example_2_form = code_example_2_form,
        file_upload_form = file_upload_form,
        code_example_4_form = code_example_4_form,
        change_please_form = change_please_form,
        change_please_comments = change_please_comments,
        five_letter_unscramble_form = five_letter_unscramble_form,
        five_letter_unscramble_comments = five_letter_unscramble_comments,
        document_statistics_form = document_statistics_form,
        document_statistics_comments = document_statistics_comments,
        wan_wang_form = wan_wang_form,
        wan_wang_comments = wan_wang_comments,
        code_example_1 = code_example_1,
        code_example_2 = code_example_2,
        code_example_3 = code_example_3,
        code_example_4 = code_example_4,
        code_example_2_res = code_example_2_res,
        number_matching_words = number_matching_words
        )

    if file_upload_form.validate_on_submit():

        uploaded_file = file_upload_form.upload.data
        filename = secure_filename(uploaded_file.filename)

        if filename != '':

            file_ext = os.path.splitext(filename)[1]
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            flash('File successfully uploaded! Please scroll down to see your results')
            current_file = (os.path.join(app.config['UPLOAD_PATH'], filename))
            code_example_3_res = document_stats(current_file)

            number_letters = code_example_3_res[0]
            number_numbers = code_example_3_res[1]
            number_symbols = code_example_3_res[2]
            number_words = code_example_3_res[3]
            number_sentences = code_example_3_res[4]
            number_paragraphs = code_example_3_res[5]

            return render_template(
            'code_examples.html',
            title = 'Code Examples',
            code_example_1_form = code_example_1_form,
            code_example_2_form = code_example_2_form,
            file_upload_form = file_upload_form,
            code_example_4_form = code_example_4_form,
            change_please_form = change_please_form,
            change_please_comments = change_please_comments,
            five_letter_unscramble_form = five_letter_unscramble_form,
            five_letter_unscramble_comments = five_letter_unscramble_comments,
            document_statistics_form = document_statistics_form,
            document_statistics_comments = document_statistics_comments,
            wan_wang_form = wan_wang_form,
            wan_wang_comments = wan_wang_comments,
            code_example_1 = code_example_1,
            code_example_2 = code_example_2,
            code_example_3 = code_example_3,
            code_example_4 = code_example_4,
            number_letters = number_letters,
            number_numbers = number_numbers,
            number_symbols = number_symbols,
            number_words = number_words,
            number_sentences = number_sentences,
            number_paragraphs = number_paragraphs
            )

    if code_example_4_form.validate_on_submit():

        number = code_example_4_form.arabicNumber.data
        code_example_4_res = wanWang(number)

        arabic_number = code_example_4_res[0]
        pinyin_number = code_example_4_res[1]
        character_number = code_example_4_res[2]

        flash('Number successfully converted! Please scroll down to see your results')


        return render_template(
        'code_examples.html',
        title = 'Code Examples',
        code_example_1_form = code_example_1_form,
        code_example_2_form = code_example_2_form,
        file_upload_form = file_upload_form,
        code_example_4_form = code_example_4_form,
        change_please_form = change_please_form,
        change_please_comments = change_please_comments,
        five_letter_unscramble_form = five_letter_unscramble_form,
        five_letter_unscramble_comments = five_letter_unscramble_comments,
        document_statistics_form = document_statistics_form,
        document_statistics_comments = document_statistics_comments,
        wan_wang_form = wan_wang_form,
        wan_wang_comments = wan_wang_comments,
        code_example_1 = code_example_1,
        code_example_2 = code_example_2,
        code_example_3 = code_example_3,
        code_example_4 = code_example_4,
        arabic_number = arabic_number,
        pinyin_number = pinyin_number,
        character_number = character_number
        )

    return render_template(
    'code_examples.html',
    title = 'Code Examples',
    code_example_1_form = code_example_1_form,
    code_example_2_form = code_example_2_form,
    code_example_4_form = code_example_4_form,
    file_upload_form = file_upload_form,
    change_please_form = change_please_form,
    change_please_comments = change_please_comments,
    five_letter_unscramble_form = five_letter_unscramble_form,
    five_letter_unscramble_comments = five_letter_unscramble_comments,
    document_statistics_form = document_statistics_form,
    document_statistics_comments = document_statistics_comments,
    wan_wang_form = wan_wang_form,
    wan_wang_comments = wan_wang_comments,
    code_example_1 = code_example_1,
    code_example_2 = code_example_2,
    code_example_3 = code_example_3,
    code_example_4 = code_example_4,
    )