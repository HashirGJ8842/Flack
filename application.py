from flask import Flask, render_template, request, flash, session, url_for, redirect
from flask_session import Session
from flask_socketio import SocketIO, emit, send


app = Flask(__name__)
app.config['SECRET_KEY'] = 'POP'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
socketio = SocketIO(app)
channels = []
channels_name = []


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    if session.get('channel') == None:
        session['channel'] = None
    if session.get('username') == None:
        session['username'] = None
        session['channel'] = None
    if request.method == "POST":
        if request.form.get('display_name'):
            session['username'] = request.form.get('display_name')
            flash(f'You\'re now logged in as {session["username"]}', 'success')
        elif request.form.get("channel"):
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


@socketio.on('channel select')
def func(data):
    print('Came from JS')
    channel = data['channel']
    for i in channels:
        if i['name'] == channel:
            break
    try:
        i['messaeges']
    except KeyError:
        i['messages'] = None

    emit('show channel', {'name': i['name']}, broadcast=True)
