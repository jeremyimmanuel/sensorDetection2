import pyshark
import sys, os
import time

def sniffy():
    '''
    Version 1
    filename = "pcapSniff.pcap"
    File name to save the pcap file in.
    Live capture from wireless and port 8090, and store in a file
    cap = pyshark.LiveCapture(interface = 'en0', display_filter='tcp.port eq 8090', output_file=filename)
    FIXME : for some reason captured packets are not saved in
    
    -------
    
    Version 2 - Captures the packets and then go through all the packets and extract all the playloads
    and then write out to a txt file.
    '''
    # display_filter='tcp.port eq 80'
    filename = 'livecap.pcap'
    print('cap object created')
    cap = pyshark.LiveCapture(interface = 'en0', output_file=filename) # bpf_filter='ip.addr == 10.156.7.37'
    cap.sniff(timeout = 60)

    # overwrite pcap file
    os.system('./pcapfix-1.1.4/pcapfix -o ' + filename + ' ' + filename)
    
    # filename = 'livecap2.pcap'
    print('at analysis')
    print('filename is: %s' % filename)

    time.sleep(10)
    os.execlp('python', 'python', 'analysis.py', 'recording.wav')


if __name__ == "__main__":
    sniffy()


#Junks

    # cap1 = pyshark.FileCapture(filename)
    # for pkt in cap1:
    #    try:
    #        if pkt.tcp != None:
    #            if pkt.tcp.payload != None:
    #                print(pkt.tcp.payload)

    #    except AttributeError:
    #        pass


#    filename = "pcapSniff.txt"
#    cap = pyshark.LiveCapture(interface = 'en0', display_filter='tcp.port eq 8090')
#    f = open(filename, 'w')
#    print('sniffing...')
#    cap.sniff(timeout = 5) #5 second for quick testing
#    print(cap)
#
#    # Go through the captured packets and only write out the payloads
#    for pkt in cap:
#        try:
#            if pkt.tcp != None:
#                if pkt.tcp.payload != None:
#                    a = pkt.tcp.payload
#                    f.write(a)
#
#        except AttributeError:
#            pass
#
#    print("we here")
#    f.close()
#    print("end of sniffy")

    # cap.set_debug(True)
    # print('cap object created')
    # cap.sniff(timeout = 60)
    
    # print(cap)
    # cap.close()
    # output.close()

    # analysis()

# def analysis(filename):
#     print('at analysis')
#     print('filename is: %s' % filename)

#     cap1 = pyshark.FileCapture(filename,only_summaries=True,keep_packets = False)
#     array1 = brenti.generate_array_of_inputs_per_windowSize2(cap1) # protector wav

#     cap2 = pyshark.FileCapture('packetFromPhone.pcap', only_summaries=True, keep_packets = False)
#     array2 = brenti.generate_array_of_inputs_per_windowSize2(cap2)


#     if(brenti.compareByteArrays(array1,array2,1.0)):
#         print("similar")
#     else:
#         print("not similar")

# os.execlp('python', 'python', 'analysis.py', 'recording.wav') 
