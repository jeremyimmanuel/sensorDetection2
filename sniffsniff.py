import pyshark

def sniffy():
    print('sniffing... :)')
    #Read all the packets from jojo.pcap and filter it by the connection port i used (8090)
    cap = pyshark.LiveCapture(interface = 'en0') #,display_filter='tcp.port eq 8090')
    cap.sniff(timeout = 3)
    print(cap)
    print("end of sniffy")

if __name__ == "__main__":
    sniffy()