from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import eventlet
import eventlet.wsgi
import datetime
import os, pyshark
import math
from time import sleep
import sniffsniff

'''
server file
- hosts a server at localhost:8090 
- all phones will connect to this server
- calls sniffsniff.py to sniff on network
- calls analysis.py to compare bytearrays
'''

# Flask server syntax
app = Flask(__name__)
app.config['SECRET_KEY'] = 'testkey123'
socketio = SocketIO(app)

timeStamp = None    # time recorded when player tells recorders to start recording,
                    # and used to make a new directory (name) for each experiment

recordPopulation = 0    # number of recorders in the room
playerPopulation = 0    # number of players in the room

deviceArr = []

# Flask server default route (optional webpage for browsers)
@app.route('/') 
def sessions():
    return render_template('session.html')


@socketio.on('join recorder')
def on_join_record(deviceName):
    '''
    recieves a 'join recorder' event from android device
    with the recorder device name (e.g. Lenovo)
    '''
    join_room('recorder')
    global recordPopulation # records population of recorders
    recordPopulation += 1
    
    emit('enable button', room='player')
    emit('update recorder number', recordPopulation, room='player')
    
    # shown on terminal that hosts the server by running this file
    print(deviceName + ' recorder registered')
    print('total recorder: ', recordPopulation)


@socketio.on('leave recorder')
def on_leave_record():
    '''
    recieves a 'leave recorder' event from android device
    recorder device leaves the room and recorder population is updated
    - only happens if user "backs" out of recorder page in app
    '''
    global recordPopulation
    recordPopulation -= 1   # reduces population of recorders
    recordPopulation = recordPopulation if recordPopulation > 0 else 0
    
    leave_room('recorder')
    # update player of number of recorders left
    emit('update recorder number', recordPopulation, room='player')
    
    # disable 'start' button on player's screen if there is no recorder ready
    # in the room
    if recordPopulation == 0:
        emit('disable button', room='player')
    
    print('after leaving, recorder: ', recordPopulation)


@socketio.on('join player')
def on_join_player(deviceName):
    '''
    recieves a 'join player' event from android device
    with the player device name (e.g. Lenovo)
    '''
    join_room('player')
    global playerPopulation # record number of players
    playerPopulation += 1   # update number of players +1
    
    emit('update recorder number', recordPopulation, room='player')
    
    print(deviceName + ' registered as player')
    print('total player: ', playerPopulation)


@socketio.on('leave player')
def on_leave_player():
    '''
    receives a 'leave player' event from android device
    player device leaves the room and player population is updated
    '''
    global playerPopulation # record number of players
    playerPopulation -= 1   # update number of players -1
    playerPopulation = playerPopulation if playerPopulation > 0 else 0
    leave_room('player')
    print('after leaving, player: ', playerPopulation)


@socketio.on('ask for button')
def on_ask_for_button():
    '''
    receives an 'ask for button' event from android device
    allows the 'start' button on player's screen if there's at least
    one recorder ready in the room
    '''
    global recordPopulation 
    if recordPopulation > 0:                    # if there are more than one recorders
        emit('enable button', room='player')    # enable player button to start recording


@socketio.on('start collection')
def on_start_collection():
    '''
    receives a 'start collection' event from android device and start recording
    on all of connected recorder devices for 60s
    1. calls recorders to start recording audio
    2. calls sniffsniff to start sniffing on network
    '''

    pid = os.fork()
    if (pid == 0):
        # os.execlp('/home/sensor/anaconda3/bin/python', 'python', 'sniffsniff.py', 'wlp4s0mon', '6')
        # os.system('startSniff 1')
        # os.system('sudo /home/sensor/anaconda3/bin/python sniffsniff.py wlp4s0mon 6')
        os.system('sudo tshark -a duration:60 -w test1.pcap')
        
    else:    
        # emit('start sniffing', room = 'sniffer') # send broadcast to sniffer
        
        # dt_obj= datetime.datetime.now() # when the experiment is started
        # global timeStamp
        # timeStamp = str(dt_obj.year) + '_' + str(dt_obj.month) + '_' + str(dt_obj.day) + '_' + str(dt_obj.hour) + '_' + str(dt_obj.minute) + '_' + str(dt_obj.second)
        print('data collection started')
        emit('start record', room='recorder')
        print('recording')
        # emit('start play', room='player')
        # print('playing')
        # os.mkdir('recordings_' + timeStamp) # make directory for this experiment
        

@socketio.on('stop collection')
def on_stop_collection():
    '''
    receives a 'stop collection' event from android device and stops recording
    on all of connected recorder devices
    '''
    emit('stop record', room='recorder')
    print('stop recording')

    
# hey Brent! -from Anwar, Jeremy, Donghee & Jun :D
# easter egg
@socketio.on('hey waddup')
def on_waduup():
    print('i\'m fine bro')


@socketio.on('Send File')
def convert_file_to_wav(byteArr, deviceName):
    '''
    receives a 'Send File' event from android device along with
    byteArr(recording files saved in recorder devicess transformed into a byte array)
    and the unique deviceName of the recorder (a portion of FINGERPRINT)
    '''
    
    global timeStamp
    print('converting to audio file')
    # fileName = deviceName.split(".")[0] +".wav"
    # saves in a directory for this experiment
    # filePath = "recordings_" + timeStamp + '/' + fileName
    # print(filePath)
    fileName = 'recording.aac'
    with open(fileName, "wb") as binary_file:
        # Write text or bytes to the file
        binary_file.write("".encode('utf8')) 
        num_bytes_written = binary_file.write(byteArr)
    print("Wrote %d bytes." % num_bytes_written)

    # new_dict = {}
    # with open('new_dict.txt') as f:


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8090) 
    #0.0.0.0 means listening to any device that submits to that port
