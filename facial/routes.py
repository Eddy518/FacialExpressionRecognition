from flask import render_template,url_for, flash, redirect, request
from flask_mail import Message
from facial import app,bcrypt, db, mail
from facial.form import RegistrationForm,LoginForm, RequestResetForm, ResetPasswordForm, UpdateAccountForm, UpdatePasswordForm
from facial.models import User
from flask_login import login_user, current_user, logout_user, login_required

forgot = False

@app.route('/home')
@app.route('/')
def home():
    return render_template('index.html',title='Home')

@app.route('/login',methods=('GET','POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login failed! Invalid credentials!','fail')
    return render_template('login.html',title='Log In',forgot = True,form=form)

@app.route('/register',methods=('GET','POST'))
@app.route('/sign-up',methods=('GET','POST'))
@app.route('/signup',methods=('GET','POST'))
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('login'))
    return render_template('sign-up.html',title='Sign Up',forgot = False,form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html',title='Dashboard')

def print_user_data(form):
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

@app.route('/account',methods=('GET','POST'))
@app.route('/settings',methods=('GET','POST'))
@app.route('/profile',methods=('GET','POST'))
@login_required
def account():
    form = UpdateAccountForm()
    print_user_data(form)
    password_form = UpdatePasswordForm()
    if form.validate_on_submit():    
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        # flash("Your account has been updated!",'success')
        print("test if in profile")
        return redirect(url_for('account'))

    if password_form.validate_on_submit():    
        hashed_password=bcrypt.generate_password_hash(password_form.password.data)
        current_user.password = hashed_password
        db.session.commit()
        print("test if in password")

        return redirect(url_for('account'))
    else:
        print("test else in password")
        render_template('account.html',title='Profile',form=form,password_form=password_form)


    return render_template('account.html',title='Profile',form=form,password_form=password_form)    

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',sender='noreply@demo.com',recipients=[user.email])

    msg.body = f'''Visit the following link to reset your password:
{url_for('reset_token',token=token,_external= True)}
If you did not make this request then simply ignore this email and no changes will be made
     '''
    mail.send(msg)

@app.route('/reset_password',methods=('GET','POST'))
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        # flash('An email has been sent to you with the instructions','info')
        return redirect(url_for('login'))
    return render_template('request_reset.html',title='Reset Password',form=form)

@app.route('/reset_password/<token>',methods=('GET','POST'))
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    user = User.verify_reset_token(token)
    if not user:
        # flash('That is an invalid or expired token','warning')
        return redirect(url_for('request_reset'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        # flash('Password successfully updated! You can now log in','success')
        return redirect(url_for('login'))
    return render_template('reset_token.html',title='Reset Password',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
