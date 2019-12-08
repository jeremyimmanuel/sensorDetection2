from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import eventlet
import eventlet.wsgi #flask uses it, makes it secure
import datetime
import os
import subprocess
import math
from _thread import *
import threading
import pyshark
import analysis as brenti
from threading import Thread
#import numpy as np
#from scipy.io.pcapfile import read, write

#we need socket to make real time and supaaaa fastttttttt vroom vroom


app = Flask(__name__)
app.config['SECRET_KEY'] = 'testkey123'
socketio = SocketIO(app)
timeStamp = None # time recorded when player tells recorders to start recording,
# and used to make a new directory (name) for each experiment

recordPopulation = 0    # number of recorders in the room
playerPopulation = 0    # number of players in the room

deviceArr = []

@app.route('/') #we definately need this
def sessions():
    return render_template('session.html')

@socketio.on('join recorder')
def on_join_record(deviceName):
    '''
    recieves a 'join recorder' event from android device
    with the recorder device name (e.g. Lenovo)
    '''
    join_room('recorder')
    global recordPopulation
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
    '''
    global recordPopulation
    recordPopulation -= 1
    recordPopulation = recordPopulation if recordPopulation > 0 else 0
    
    leave_room('recorder')
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
    global playerPopulation
    playerPopulation += 1
    
    emit('update recorder number', recordPopulation, room='player')
    
    print(deviceName + ' registered as player')
    print('total player: ', playerPopulation)


@socketio.on('leave player')
def on_leave_player():
    '''
    receives a 'leave player' event from android device
    player device leaves the room and player population is updated
    '''
    global playerPopulation
    playerPopulation -= 1
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
    if recordPopulation > 0:
        emit('enable button', room='player')

@socketio.on('join sniffer')
def on_join_sniffer():
    '''
    receive a join sniffer event from the sniffer script
    '''
    print('sniffer joined')
    join_room('sniffer')


@socketio.on('start collection')
def on_start_collection():
    '''
    receives a 'start collection' event from android device and start recording
    on all of connected recorder devices
    '''
    emit('start sniffing', room = 'sniffer') # send broadcast to sniffer
    
    dt_obj= datetime.datetime.now() # when the experiment is started
    global timeStamp
    timeStamp = str(dt_obj.year) + '_' + str(dt_obj.month) + '_' + str(dt_obj.day) + '_' + str(dt_obj.hour) + '_' + str(dt_obj.minute) + '_' + str(dt_obj.second)
    print('data collection started')
    emit('start record', room='recorder')
    print('recording')
    emit('start play', room='player')
    print('playing')
    os.mkdir('recordings_' + timeStamp) # make directory for this experiment
    

# receives a 'stop collection' event from android device and stops recording
# on all of connected recorder devices
@socketio.on('stop collection')
def on_stop_collection():
    emit('stop record', room='recorder')
    print('stop recording')

# hey Brent! -from Anwar, Jeremy, and Donghee :D
@socketio.on('hey waddup')
def on_waduup():
    print('i\'m fine bro')
    #emit('testMessage') # this works, go to on_start_collection for other emit testMessage

# receives a 'Send File' event from android device along with
# byteArr(recording files saved in recorder devicess transformed into a byte array)
# and the unique deviceName of the recorder (a portion of FINGERPRINT)
@socketio.on('Send File')
def convert_file_to_pcap(byteArr, deviceName):
    global timeStamp
    fileName = deviceName.split(".")[0] +".pcap" #get name by getting rid of '.3gp'
    # fileName = "recordingFromPhone.pcap"
    # saves in a directory for this experiment
    filePath = "recordings_" + timeStamp + '/' + fileName
    print(filePath)
    with open(fileName, "wb") as binary_file:
        # Write text or bytes to the file
        binary_file.write("".encode('utf8')) #don't added any string to the empty string, it will added that string to whateevver file you writing onto 
        num_bytes_written = binary_file.write(byteArr)
    print("Wrote %d bytes." % num_bytes_written)
    
    emit('do analysis', fileName, room = 'sniffer')
    #analysis(fileName)


    

if __name__ == '__main__':
    
    socketio.run(app, debug=True, host='0.0.0.0', port=8090) #we definately need this
    #0.0.0.0 means listening to any device that submits to that port

