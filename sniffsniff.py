import pyshark
import analysis as brenti
import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("I'm connected!")
    sio.emit('hey waddup')

@sio.on('start sniffing')
def sniffy(_):
    print('sniffing... :)')
    #Read all the packets from jojo.pcap and filter it by the connection port i used (8090)
    cap = pyshark.LiveCapture(interface = 'en0', display_filter='tcp.port eq 8090', output_file="/Users/jzhenmbp/Desktop/School/research/sensorDetection2/packetFromPhone.pcap")
    cap.sniff(timeout = 60)
    print("end of sniffy")

    #analysis()

@sio.on('do analysis')
def analysis(filename):
    print('at analysis')
    print(filename)
    
    cap1 = pyshark.FileCapture(filename,only_summaries=True,keep_packets = False)
    array1 = brenti.generate_array_of_inputs_per_windowSize2(cap1) # protector wav

    cap2 = pyshark.FileCapture('packetFromPhone.pcap', only_summaries=True, keep_packets = False)
    array2 = brenti.generate_array_of_inputs_per_windowSize2(cap2)


    if(brenti.compareByteArrays(array1,array2,1.0)):
        print("similar")
    else:
        print("not similar")

@sio.on('testMessage')
def func(_):
    print('test message recieved')

if __name__ == "__main__":
    sio.connect('http://192.168.0.54:8090')