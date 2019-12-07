import pyshark
import analysis as brenti
from flask import Flask
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import eventlet
import eventlet.wsgi

import socketio

sio = socketio.Client()

@sio.on('start collection')
def sniffy():
    print('sniffing... :)')
    #Read all the packets from jojo.pcap and filter it by the connection port i used (8090)
    cap = pyshark.LiveCapture(interface = 'en0', display_filter='tcp.port eq 8090', output_file="/Users/jzhenmbp/Desktop/School/research/sensorDetection2/packetFromPhone.pcap")
    cap.sniff(timeout = 60)
    print("end of sniffy")

   
@sio.on('do analysis')
def analysis(filename):
    print('at analysis')
    cap1 = pyshark.FileCapture(filename,only_summaries=True,keep_packets = False)
    array1 = brenti.generate_array_of_inputs_per_windowSize2(cap1) # protector wav

    cap2 = pyshark.FileCapture('packetFromPhone.pcap', only_summaries=True, keep_packets = False)
    array2 = brenti.generate_array_of_inputs_per_windowSize2(cap2)


    if(brenti.compareByteArrays(array1,array2,1.0)):
        print("similar")
    else:
        print("not similar")


if __name__ == "__main__":
    sio.connect('http://localhost:8090')