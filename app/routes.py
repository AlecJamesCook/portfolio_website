from flask import render_template, flash, redirect, url_for, request, abort
from app import app, db, mail
from app.forms import LoginForm, RegistrationForm, EditProfileForm, Code_example_1_form, Code_example_2_form, File_upload_form, PostForm1, PostForm2, PostForm3, RequestPasswordResetForm, PasswordResetForm
from app.models import User, Post, Work_experience, Education, Computing, Code_examples
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
@login_required
def index():

    return render_template('index.html', title = 'Home')

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
@login_required
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
 
@login_required
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

@login_required
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

@login_required
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

@login_required
@app.route('/code_examples', methods = ['GET', 'POST'])
def code_examples():

    def change_please(amount,coins):

        """
        Determines whether a particular amount can be reached by using only a specified amount of coins

        :param amount: The desired amount to reach.
        :type: int/float

        :param coins: The number of coins that need to be used to reach the desired amount.
        :type: int
        
        :rtype: bool
        :return: Whether or not you can reach the amount using the specified number of coins.

        """

        # Times the amount by 100 to avoid floating point number shenanigans.
        amount *= 100
        coin_list = [200, 100, 50, 20, 10, 5, 2, 1]

        if coins < 1:
            return False

        def recursive_loop(amount, coins, coin_list):

            """
            The largest coin that is <= amount is subtracted from the amount until one of the base cases is reached. If a false base case is reach, the for loop moves on to the next smaller coin. This continues until the for loop has iterated over every element in the coinList, or if the amount and the number of coins both reach 0.

            :param amount: The desired amount to reach.
            :type: int/float
        
            :param coins: The number of coins that need to be used to reach the desired amount.
            :type: int

            :param coinList: The different coins that can be subtracted from the amount.
            :type: array (every element is an int).
            
            :rtype: bool
            :return: Whether or not you can reach the amount using the specified number of coins.

            """

            # The basecases for the recursive loop.
            if amount == 0 and coins == 0:
                return True
            elif amount == coins:
                return True
            elif amount != 0 and coins == 0:
                return False
            elif amount == 0 and coins != 0:
                return False

            for element in coin_list:
                if element <= amount:

                    # Recurses the function until it finds a basecase. 
                    # If it hits a false basecase, the for loop continues.
                    if recursive_loop((amount - element), (coins-1), coin_list):
                        return True

            #returns false if the for loop reaches the end before hitting a true basecase.
            return False

        return recursive_loop(amount, coins, coin_list)

    def five_letter_unscramble(string):

        """
        
        When given a string, this function determines how many unique five-letter words can be made out of
        the letters in the string. Uses a set of wordle words as the source of these five-letter words.

        :param s: Contains the letters to be used when looking for unique five-letter words. Each letter can only be used once.
        :type: string

        :rtype: int
        :return: The number of unique five-letter words found in the wordle list that contain only the letters given in the parameter s.

        """

        def histogram_builder(string):

            """ 
            Creates a dictionary with the letters of the string as keys and the number of times the letters appear in the string as their values. This function appeared in the lecture notes from the Python course, namely the dictionary lesson. Many thanks to Federico!
            """
            
            histogram_dictionary = dict()
            
            for letter in string:
                if letter not in histogram_dictionary:
                    histogram_dictionary[letter] = 1
                else:
                    histogram_dictionary[letter] += 1     
                    
            return histogram_dictionary
        
        input_word_histogram = histogram_builder(string)

        with open('wordle.txt') as fin:
            contents = fin.readlines()
            words_list = []
            for line in contents:
                word = line.strip("\n")
                words_list.append(word)

        counter = 0
        no_of_matching_words = 0
        matching_words = []

        for word in words_list:
            words_list_histogram = histogram_builder(word) 
            for letter in word:

                # This loop creates a histogram dictionary out of each word in the wordle list. 
                # It then compares it's keys to the input string histogram's keys.
                # If the keys are in both of the dictionary and the value the other value,the counter is incremented.
                if letter in input_word_histogram and words_list_histogram[letter] <= input_word_histogram[letter]:
                    counter += 1
                
                # If the counter reaches 5, it has found a unique five-letter word.
                if counter == 5:
                    matching_words.append(word)
                    
            counter = 0

        return matching_words

    def document_stats(filename):
        """

        Reads a document and returns several statistics about the makeup of the file.
    
        :param filename: The name of the file to be read.
        :type: file
        
        :rtype: tuple
        :return: Contains (in order) the number of letters, the number of numeric characters, the number of symbols characters, the number of words, the number of sentences, and the number os paragraphs in the file.

        """

        num_letters = num_numbers = num_symbols = num_words = num_sentences = 0
        num_paragraphs = 1
        
        # Creates a list with all of the printable characters in the file as elements. It provides the number of words a base value. It will need to be added to later on.
        fin = open(filename)
        data = fin.read()
        word_length_file = data.split()
        num_words += len(word_length_file)
        fin.close()

        # This places the file into one string to make it easier to iterate over.
        fin_2 = open(filename)
        line_list = fin_2.readlines()
        text = ''.join(line_list)
        fin_2.close()

        for char in range(0, len(text)):
            # The next three statements use inbuilt functions to find the number of letters, numeric characters, and symbols in the string.
            num_letters += text[char].isalpha()
            num_numbers += text[char].isnumeric()
            num_symbols += text[char].isprintable() and not text[char].isalnum() and not text[char].isspace()

            # These two statements find sentences according to different puncuation symbols. The second conditional is there in case of floats.
            if text[char] == "." or text[char] == "!" or text[char] == "?":
                num_sentences += 1
            if text[char] == "." and text[char-1].isnumeric() and text[char+1].isnumeric():
                num_sentences -= 1

            # This adds to the base value of the number of words by checking for grammatical or puncuation errors in the source file. It checks whether the character is a symbol and if this symbol does not have a space following it (which indicates a typo in the source file). 
            try:
                num_words += text[char].isprintable() and not text[char].isalnum() and not text[char].isspace() and text[char+1].isalpha() and not text[char-1].isspace()
            except:
                continue
            
            # Finds the number of paragraphs by finding a printable character and checking whether two new lines precede it.
            if text[char].isprintable() and text[char-1] == "\n" and text[char -2] == "\n":
                num_paragraphs += 1

        output_tuple = (num_letters, num_numbers, num_symbols, num_words, num_sentences, num_paragraphs)

        return output_tuple

    # Code example variables
    code_example_1_form = Code_example_1_form()
    code_example_2_form = Code_example_2_form()
    file_upload_form = File_upload_form()

    code_example_1 = Code_examples.query.filter_by(id=1).first()
    code_example_2 = Code_examples.query.filter_by(id=2).first()
    code_example_3 = Code_examples.query.filter_by(id=3).first()

    # Comment section variables
    change_please_form = PostForm1()
    five_letter_unscramble_form = PostForm2()
    document_statistics_form = PostForm3()

    change_please_comments = Post.query.filter_by(tag = "change_please").order_by(Post.timestamp.desc()).all()
    five_letter_unscramble_comments = Post.query.filter_by(tag = "five_letter_unscramble").order_by(Post.timestamp.desc()).all()
    document_statistics_comments = Post.query.filter_by(tag = "document_unscramble").order_by(Post.timestamp.desc()).all()

    # Handling the different forms
    if change_please_form.submit1.data and change_please_form.validate():

        change_please_post = Post(body = change_please_form.post.data, tag = "change_please", author = current_user)
        db.session.add(change_please_post)
        db.session.commit()
        flash('Comment posted!')

        return redirect(url_for('code_examples'))

    if five_letter_unscramble_form.submit2.data and five_letter_unscramble_form.validate():

        five_letter_unscramble_post = Post(body = five_letter_unscramble_form.post.data, tag = "five_letter_unscramble", author = current_user)
        db.session.add(five_letter_unscramble_post)
        db.session.commit()
        flash('Comment posted!')

        return redirect(url_for('code_examples'))
    
    if document_statistics_form.submit3.data and document_statistics_form.validate():

        document_statistics_post = Post(body = document_statistics_form.post.data, tag = "document_unscramble", author = current_user)
        db.session.add(document_statistics_post)
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
        change_please_form = change_please_form, 
        change_please_comments = change_please_comments,
        five_letter_unscramble_form = five_letter_unscramble_form,
        five_letter_unscramble_comments = five_letter_unscramble_comments,
        document_statistics_form = document_statistics_form,
        document_statistics_comments = document_statistics_comments,
        code_example_1 = code_example_1, 
        code_example_2 = code_example_2, 
        code_example_3 = code_example_3, 
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
        change_please_form = change_please_form, 
        change_please_comments = change_please_comments,
        five_letter_unscramble_form = five_letter_unscramble_form,
        five_letter_unscramble_comments = five_letter_unscramble_comments,
        document_statistics_form = document_statistics_form,
        document_statistics_comments = document_statistics_comments,
        code_example_1 = code_example_1, 
        code_example_2 = code_example_2, 
        code_example_3 = code_example_3, 
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
            change_please_form = change_please_form, 
            change_please_comments = change_please_comments,
            five_letter_unscramble_form = five_letter_unscramble_form,
            five_letter_unscramble_comments = five_letter_unscramble_comments,
            document_statistics_form = document_statistics_form,
            document_statistics_comments = document_statistics_comments,
            code_example_1 = code_example_1, 
            code_example_2 = code_example_2, 
            code_example_3 = code_example_3, 
            number_letters = number_letters, 
            number_numbers = number_numbers, 
            number_symbols = number_symbols, 
            number_words = number_words, 
            number_sentences = number_sentences, 
            number_paragraphs = number_paragraphs
            )

    return render_template(
    'code_examples.html', 
    title = 'Code Examples', 
    code_example_1_form = code_example_1_form,
    code_example_2_form = code_example_2_form, 
    file_upload_form = file_upload_form,
    change_please_form = change_please_form, 
    change_please_comments = change_please_comments,
    five_letter_unscramble_form = five_letter_unscramble_form,
    five_letter_unscramble_comments = five_letter_unscramble_comments,
    document_statistics_form = document_statistics_form,
    document_statistics_comments = document_statistics_comments,
    code_example_1 = code_example_1, 
    code_example_2 = code_example_2, 
    code_example_3 = code_example_3
    )