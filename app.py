from flask import Flask,render_template,url_for

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')    

@app.route('/login')
def log_in():
    return render_template('login.html')

@app.route('/register')
@app.route('/sign-up')
@app.route('/signup')
def register():
    return render_template('sign-up.html')

if __name__ == '__main__':
    app.run(debug=True)