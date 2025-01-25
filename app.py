from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.secret_key = 'supersecretkey'
socketio = SocketIO(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['nickname'] = request.form['nickname']
        return redirect(url_for('chat'))
    return render_template('index.html')


@app.route('/chat')
def chat():
    if 'nickname' not in session:
        return redirect(url_for('index'))
    return render_template('chat.html', nickname=session['nickname'])


@socketio.on('message')
def handle_message(msg):
    nickname = session.get('nickname', 'Анонім')
    send(f'{nickname}: {msg}', broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
