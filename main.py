import time
import EV3Server
import threading

from flask import Flask, render_template
from flask_socketio import SocketIO

import logging


ev3_socket = EV3Server.EV3Socket()
app = Flask(__name__,static_url_path='/', static_folder='public')
app.config['SECRET_KEY'] = 'secret!'
SocketIO = SocketIO(app)


log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)




@app.route('/')
def index():
    return render_template('index.html')
@SocketIO.on('connect')
def handle_connect():
    print('Client connected')
    if len(ev3_socket.clients) > 0:
        SocketIO.emit('ev3', {'message': 'EV3 connected'})
    else:
        SocketIO.emit('ev3', {'message': 'EV3 disconnected'})
        
@SocketIO.on('message')
def handle_message(data):
    print(f"received message:{data.message}")



@SocketIO.on('keyEvent')
def handle_Event(data):
    if len(ev3_socket.clients) > 0:
        key = data['keyEvent'].encode('utf-8')
        pressed = data['type'] == 'keyDown' and True or False
        ev3_socket.send(b'keyEvent:' + key + b' ' + str(pressed).encode('utf-8'))

if __name__ == '__main__':
    try:
        server_thread = threading.Thread(target=ev3_socket.start, args=(SocketIO,))
        server_threadSecond = threading.Thread(target=SocketIO.run, args=(app,))
        
        server_thread.start()
        server_threadSecond.start()
        
        server_thread.join()
        server_threadSecond.join()
        
    except KeyboardInterrupt:
        ev3_socket.close()
        SocketIO.stop()
        print('Server terminated')