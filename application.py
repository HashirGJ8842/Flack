from flask import Flask, render_template, request, flash, session, url_for, redirect
from flask_session import Session
from flask_socketio import SocketIO, emit


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
    if session.get('username') == None:
        session['username'] = None
    if request.method == "POST":
        if request.form.get('display_name'):
            session['username'] = request.form.get('display_name')
            flash(f'You\'re now logged in as {session["username"]}', 'success')
    return render_template('home.html', display_name=session['username'], channels_name=channels_name, channels=channels)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session['username'] = None
    flash(f'You\'re now logged out', 'primary')
    return redirect('home')


@socketio.on('new channel')
def new_channel(data):
    session['channel'] = data['channel']
    channel = data['channel']
    new = False
    if channel not in channels_name:
        channels_name.append(channel)
        new = True
    channels.append({'name': channel, 'messages': []})
    emit('create channel', {'name': channel,'new': new}, broadcast=True)


@socketio.on('channel select')
def channel_select(data):
    print('Came from JS')
    session['channel'] = data['channel']
    channel = data['channel']
    for i in channels:
        if i['name'] == channel:
            break

    emit('show channel', {'name': i['name'], 'messages': i['messages'], 'new': False}, broadcast=False)


@socketio.on('store message')
def store_message(data):
    print("TEST")
    for i in channels:
        if i['name']==data['channel']:
            i['messages'].append(data['message'])
    emit('display message', {'message': data['message']}, broadcast=True)