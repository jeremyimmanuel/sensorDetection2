import pyshark, os
from time import sleep

# output = open('dummyFile.pcap','w')
#Read all the packets from jojo.pcap and filter it by the connection port i used (8090)
cap = pyshark.LiveCapture(interface = 'en0')
print('cap object created')


f = open('dummyFile.txt', 'w')
cap.sniff(packet_count = 5)
for pkt in cap:
    try:
        if pkt.tcp != None:
            if pkt.tcp.payload != None:
                a = pkt.tcp.payload.split(':')
                for b in a:
                    f.write(b + ' ')
    except AttributeError:
        print('bruh')

f.close()




#cap.apply_on_packets(print, timeout = 5)
print("end of sniffy")
# output.close()
# cap.close()
# os.rename('dummyFile.txt', 'dummyFile.pcap')

# jojocap = pyshark.FileCapture('dummyFile.pcap', only_summaries=True, keep_packets = False)
# print(jojocap)