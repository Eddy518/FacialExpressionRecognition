from flask import render_template,url_for, flash, redirect, request
from facial import app,bcrypt, db
from facial.form import RegistrationForm,LoginForm, UpdateAccountForm
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
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('login'))
    return render_template('sign-up.html',title='Sign Up',forgot = False,form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html',title='Dashboard')

@app.route('/account',methods=('GET','POST'))
@app.route('/settings',methods=('GET','POST'))
@app.route('/profile',methods=('GET','POST'))
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():    
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!",'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html',title='Profile',form=form)    

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
