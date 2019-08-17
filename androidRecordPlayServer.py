from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import eventlet
import eventlet.wsgi
import datetime
import os

# import soundcard as sc
import numpy as np
# import waveflask
from scipy.io.wavfile import read, write

app = Flask(__name__)
app.config['SECRET_KEY'] = 'testkey123'
socketio = SocketIO(app)
timeStamp = None

recordPopulation = 0
playerPopulation = 0

deviceArr = []

@app.route('/')
def sessions():
    return render_template('session.html')

@socketio.on('join recorder') # recieves a 'join recorder' event (emit) from android device
def on_join_record(deviceName):
    join_room('recorder')
    global recordPopulation
    recordPopulation += 1
    emit('enable button', room='player')
    emit('update recorder number', recordPopulation, room='player')

    print(deviceName + ' recorder registered')
    print('total recorder: ', recordPopulation)

@socketio.on('leave recorder')
def on_leave_record():
    global recordPopulation
    recordPopulation -= 1
    recordPopulation = recordPopulation if recordPopulation > 0 else 0
    leave_room('recorder')
    emit('update recorder number', recordPopulation, room='player')

    if recordPopulation == 0:
        emit('disable button', room='player')
    print('after leaving, recorder: ', recordPopulation)

@socketio.on('join player')
def on_join_player(deviceName):
    room = 'player'
    join_room(room)
    global playerPopulation
    playerPopulation += 1

    emit('update recorder number', recordPopulation, room='player')

    print(deviceName + ' registered as player')
    print('total player: ', playerPopulation)

@socketio.on('leave player')
def on_leave_player():
    global playerPopulation
    playerPopulation -= 1
    playerPopulation = playerPopulation if playerPopulation > 0 else 0
    leave_room('player')
    print('after leaving, player: ', playerPopulation)

@socketio.on('ask for button')
def on_ask_for_button():
    global recordPopulation
    if recordPopulation > 0:
        emit('enable button', room='player')

@socketio.on('start collection')
def on_start_collection():
    dt_obj= datetime.datetime.now() #make datetime object
    global timeStamp
    timeStamp = str(dt_obj.year) + '_' + str(dt_obj.month) + '_' + str(dt_obj.day) + '_' + str(dt_obj.hour) + '_' + str(dt_obj.minute) + '_' + str(dt_obj.second)
    print('data collection started')
    emit('start record', room='recorder')
    print('recording')
    emit('start play', room='player')
    print('playing')
    os.mkdir('recordings_' + timeStamp) #make folder


@socketio.on('stop collection')
def on_stop_collection():
    emit('stop record', room='recorder')
    print('stop recording')

@socketio.on('hey waddup')
def on_waduup():
    print('i\'m fine bro')


@socketio.on('Send File')
def convert_file_to_wav(byteArr, deviceName):
    global timeStamp
    fileName = deviceName.split(".")[0] +".wav"
    filePath = "recordings_" + timeStamp + '/' + fileName
    print(filePath)
    with open(filePath, "wb") as binary_file:
        # Write text or bytes to the file
        binary_file.write("".encode('utf8'))
        num_bytes_written = binary_file.write(byteArr)
    print("Wrote %d bytes." % num_bytes_written)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8090)
#    app = socketio.Middleware(socketio, app)
#    eventlet.wsgi.server(eventlet.listen(('', 8090)), app)


