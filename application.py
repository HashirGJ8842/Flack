from flask import Flask, render_template, request, flash, session, url_for
from flask_session import Session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'POP'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    if session.get('username') == None:
        session['username'] = None
    if request.method == "POST":
        session['username'] = request.form.get('display_name')
        flash(f'You\'re now logged in as {session["username"]}', 'success')
    return render_template('home.html', display_name=session['username'])


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session['username'] = None
    flash(f'You\'re now logged out', 'primary')
    return render_template('home.html', display_name=session['username'])