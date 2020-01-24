import pyshark
import analysis as brenti
from flask import Flask
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import eventlet
import eventlet.wsgi

import socketio

sio = socketio.Client()

if __name__ == '__main__':
    sio.connect('http://localhost:8090')
    emit('hey waddup')