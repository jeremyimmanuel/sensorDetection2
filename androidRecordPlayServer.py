from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import eventlet
import eventlet.wsgi

# import soundcard as sc
import numpy as np
# import waveflask
from scipy.io.wavfile import read, write

app = Flask(__name__)
app.config['SECRET_KEY'] = 'testkey123'
socketio = SocketIO(app)

# recorderConnected = False

deviceArr = []

@app.route('/')
def sessions():
    return render_template('session.html')

@socketio.on('join recorder') #recieves a 'join recorder' event (emit) from android device
def on_join_record(deviceName):
    room = 'recorder'
    join_room(room)
    # recorderConnected = True
    emit('enable button', room='player')
    #from ActivateRecorder.java (80-81); emits 'join recorder' with an argument of deviceName 
    #deviceName = #what ever this is supposed to be
    
    print(deviceName + ' recorder registered')

@socketio.on('join player')
def on_join_player(deviceName):
    room = 'player'
    join_room(room)
    # send('entered the player room', room=room)
    print(deviceName + ' registered as player')

#@socketio.on('ask for button')
#def on_ask_for_button():
#    roomPopulation = len(socketio.sockets.adapter.rooms['recorder'])
#    print(roomPopulation)
#    if roomPopulation > 0:
#        emit('enable button', room='player')

@socketio.on('start collection')
def on_start_collection():
    print('data collection started')
    emit('start record', room='recorder')
    print('recording')
    emit('start play', room='player')
    print('playing')

@socketio.on('stop collection')
def on_stop_collection():
    emit('stop record', room='recorder')
    print('stop recording')

@socketio.on('hey waddup')
def on_waduup():
    print('i\'m fine bro')


@socketio.on('Send File')
def convert_file_to_wav(byteArr):
    #print('type: ')
    #print(type(byteArr[0]))
    #music = []
        #for stuff in byteArr:
#music.append(stuff)
    #print(byteArr[0])
    #binData  = ''.join(map(lambda x: chr(x % 256), music))
#print(binData)


#print(byteArr)
    with open("recording.wav", "wb") as binary_file:
    # Write text or bytes to the file
        binary_file.write("".encode('utf8'))
        num_bytes_written = binary_file.write(byteArr)
    print("Wrote %d bytes." % num_bytes_written)
#
#    music = []
#    for i in range(len(byteArr)):
#        music.append(int.from_bytes(byteArr[i], 'big'))
#
#    print(music)

#music_np = np.array(music)
#print(music_np)
#    fs =  40000
#    write('whatever.wav', fs, music_np)

@socketio.on('ask for button')
def on_ask_for_button():
    # roomPopulation = len(socketio.sockets.adapter.rooms['recorder'])
    roomPopulation = len(socketio.adapter.rooms['recorder'])
    print(roomPopulation)
    if roomPopulation > 0:
        emit('enable button', room='player')


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8090)
#    app = socketio.Middleware(socketio, app)
#    eventlet.wsgi.server(eventlet.listen(('', 8090)), app)


