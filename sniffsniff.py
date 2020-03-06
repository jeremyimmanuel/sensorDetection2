import pyshark
import sys, os
import time

ANALYSIS_SIZE = 60  # we will analyze results after 60 seconds
BIN_SIZE = 1000  # we go to a new bin every 1000 milliseconds

start_time = None

packet_sizes = list()
src_dict = dict()

new_dict = dict()

count = 0

def packetHandler(pkt):
    global start_time
    global count
    try:
 #       source = str(pkt.ip.src)   # we won't get source IP addresses in monitor mode because of encryption
        source = str(pkt.wlan.sa)
        length = pkt.length
        timestamp = pkt.sniff_timestamp
        # print (str(timestamp) + ': ' + source + ' sent ' + str(length) + ' bytes')
#        print (source)
#        print (str(length))
#        print (str(timestamp))
        # add new data to the appropriate source
        t = (timestamp, length)
        if source in src_dict:
            src_dict[source].append(t) # src_dict[source] + length
        else:
            src_dict[source] = [t]#length
        
        # print(count)
        # count+=1
        # print(src_dict[source])

        #TODO:   Add source data to the appropriate time bin


    except Exception as e:
#        print(type(e))  
        return 

# refactor packet array  
def refactor(arr):
    start = float(arr[0][0]) #get earliest time
    curr = 1
    newDict = {}

    for p in arr:
        if float(p[0]) < start + curr:
            if(curr in newDict.keys()):
                newDict[curr] += int(p[1])
            else:
                newDict[curr] = int(p[1])
        else:
            start += 1
            curr += 1
    return newDict


def sniffy(mon_iface, channel):
    global start_time
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


#    set channel
    os.system("iwconfig " + mon_iface + " channel " + str(channel) + " > /dev/null 2>&1")
    print('set channel')
    time.sleep(1)
    # while True:
    # t_end = time.time() + 0.5
    # while time.time() < t_end:
    print('capturing...')
    capture = pyshark.LiveCapture(interface = mon_iface)
    # capture.sniff(timeout=1)
    try:
        capture.apply_on_packets(packetHandler, timeout=5)
    except:
        print("done capturing")
    start_time = time.time() * 1000   #get start time in milliseconds

#    cap.sniff(timeout = 60)


    # overwrite pcap file
    # os.system('./pcapfix-1.1.4/pcapfix -o ' + filename + ' ' + filename)
    
    # # filename = 'livecap2.pcap'
    # print('at analysis')
    # print('filename is: %s' % filename)

    # time.sleep(10)
    # os.execlp('python', 'python', 'analysis.py', 'recording.wav')


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('sniffysniffy.py networkInterface channel')
        sys.exit()
    sniffy(sys.argv[1], int(sys.argv[2]))
    # print(src_dict)

    
    for k in src_dict.keys():
        new_dict[k] = refactor(src_dict[k])

    print(new_dict)

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
