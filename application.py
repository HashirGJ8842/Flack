from flask import Flask, render_template, request, flash, session, url_for, redirect
from flask_session import Session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'POP'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
channels = []
channels_name = []
for i in channels:
    channels_name.append(i['name'])


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    if session.get('channel') == None:
        session['channel'] = None
    if session.get('username') == None:
        session['username'] = None
    if request.method == "POST":
        if session['username'] == None:
            session['username'] = request.form.get('display_name')
            flash(f'You\'re now logged in as {session["username"]}', 'success')
        else:
            if request.form.get("channel") in channels_name:
                flash(f'Channel name {request.form.get("channel")} already exists, please take a different name', 'danger')
                return render_template('home.html', display_name=session['username'], channel=session['channel'], channels=channels, channels_name=channels_name)
            session['channel'] = request.form.get('channel')
            channels.append({'name': request.form.get('channel')})
            channels_name.append(request.form.get('channel'))
    return render_template('home.html', display_name=session['username'], channel=session['channel'], channels=channels, channels_name=channels_name)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session['username'] = None
    flash(f'You\'re now logged out', 'primary')
    return redirect('home')