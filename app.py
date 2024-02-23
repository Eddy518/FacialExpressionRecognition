from flask import Flask,render_template,url_for, flash, redirect
from form import RegistrationForm,LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] ='927af1257ba908bea162f42b2011047f'

forgot = False

@app.route('/home')
@app.route('/')
def home():
    return render_template('index.html',title='Home')

@app.route('/login',methods=('GET','POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == "password":
            flash('You have been logged in!','success')
            return redirect(url_for('home'))
        else:
            flash('Login failed! Invalid credentials!','fail')
    return render_template('login.html',title='Log In',forgot = True,form=form)

@app.route('/register',methods=('GET','POST'))
@app.route('/sign-up',methods=('GET','POST'))
@app.route('/signup',methods=('GET','POST'))
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))
    return render_template('sign-up.html',title='Sign Up',forgot = False,form=form)

if __name__ == '__main__':
    app.run(debug=True)
