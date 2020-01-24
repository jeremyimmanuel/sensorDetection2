from flask import Flask, render_template
from flask_socketio import SocketIO
import soundcard as sc
import numpy as np
import wave
from scipy.io.wavfile import read

app = Flask(__name__)
app.config['SECRET_KEY'] = 'testkey123'
socketio = SocketIO(app)

@app.route('/')
def sessions():
    return render_template('session.html')

def messageReceived(methods=['GET','POST']):
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET','POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)
    
@socketio.on('record and play')
def record_and_play(): #methods = ['GET', 'POST']):
    
    filename = 'bear_growl_y.wav'
    rb = wave.open(filename, 'rb')
    file_sr = rb.getframerate()
    wavfile = read(filename)[1]
    
    mysp = sc.default_speaker()
    mymic = sc.default_microphone()
    rate = 48000
    data = mymic.record(samplerate = rate, numframes = 10*rate)
    #mysp.play(wavfile/np.max(wavfile), samplerate = file_sr)
    mysp.play(data/np.max(data), samplerate = rate)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8090)

