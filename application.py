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
messages = []


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    if session.get('username') == None:
        session['username'] = None
    if request.method == "POST":
        if request.form.get('display_name'):
            session['username'] = request.form.get('display_name')
            flash(f'You\'re now logged in as {session["username"]}', 'success')
        elif request.form.get('channel'):
            if request.form.get('channel') in channels_name:
                flash(f'This channel name already exists, please try again!!', 'danger')
                return render_template('home.html', display_name=session['username'], channels=channels)
            session['channel'] = request.form.get('channel')
            flash(f'Channel {session["channel"]} successfully created', 'success')
            channels.append({'name': session['channel'], 'messages': []})
            channels_name.append(request.form.get('channel'))
    return render_template('home.html', display_name=session['username'], channels=channels)


@app.route('/<channel>', methods=["GET", "POST"])
def messages(channel):
    if session.get('username') == None:
        session['username'] = None
        session['channel'] = None
    if session.get('channel') == None:
        session['channel'] = None
    if request.method == "POST":
        if request.form.get('display_name'):
            session['username'] = request.form.get('display_name')
            flash(f'You\'re now logged in as {session["username"]}', 'success')
        elif request.form.get('channel'):
            if request.form.get('channel') in channels_name:
                flash(f'This channel name already exists, please try again!!', 'danger')
                return render_template('home.html', display_name=session['username'], channels=channels)
            session['channel'] = request.form.get('channel')
            flash(f'Channel {session["channel"]} successfully created', 'success')
            channels.append({'name': session['channel'], 'messages': []})
            channels_name.append(request.form.get('channel'))
    for i in channels:
        if i['name'] == channel:
            messages = i['messages']
    return render_template('messages.html', messages=messages, display_name=session['username'], channels=channels, heading=channel)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session['username'] = None
    flash(f'You\'re now logged out', 'primary')
    return redirect('home')


@socketio.on('store message')
def store_message(data):
    for i in channels:
        if i['name'] == data['channel']:
            i['messages'].append(data['message'])
            if len(i['messages']) >= 100:
                i['messages'].remove(i['messages'][0])
    emit('display message', {'message': data['message']}, broadcast=True)