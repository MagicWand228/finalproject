from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.secret_key = 'supersecretkey'
socketio = SocketIO(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['nickname'] = request.form['nickname']
        return redirect(url_for('home'))
    return render_template('index.html')


@app.route('/home')
def home():
    if 'nickname' not in session:
        return redirect(url_for('index'))
    return render_template('home.html', nickname=session['nickname'])


@app.route('/chat')
def chat():
    if 'nickname' not in session:
        return redirect(url_for('index'))
    return render_template('chat.html', nickname=session['nickname'])


@app.route('/stories', methods=['GET', 'POST'])
def stories():
    if 'nickname' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        story = request.form['story']
        if len(story) >= 24:
            with open('stories.txt', 'a') as file:
                file.write(f'{session["nickname"]}: {story}\n')
    with open('stories.txt', 'r') as file:
        stories_list = file.readlines()
    return render_template('stories.html', nickname=session['nickname'], stories=stories_list)


@socketio.on('message')
def handle_message(msg):
    nickname = session.get('nickname', 'Анонім')
    send(f'<b style="color: blue;">{nickname}</b>: <span style="color: black;">{msg}</span>', broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
