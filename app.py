from flask import Flask,render_template,url_for

app = Flask(__name__)

@app.route('/home')
@app.route('/')
def home():
    return render_template('index.html',title='Home')    

@app.route('/login')
def login():
    return render_template('login.html',title='Log In')

@app.route('/register')
@app.route('/sign-up')
@app.route('/signup')
def register():
    return render_template('sign-up.html',title='Sign Up')

if __name__ == '__main__':
    app.run(debug=True)
