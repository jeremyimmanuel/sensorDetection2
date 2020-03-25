import pyshark
import sys, os
import time
import analysis

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
    start = float(arr[0][0]) #get earliest time #0.7
    curr = 1
    newDict = {}

    for p in arr:
        begInterval = float(p[0]) #0.36
        endInterval = start + curr #0.36 + 0.5 = 0.61 0.86 
        # print(("begin interval %s, end interval %s") % (begInterval, endInterval))
        if begInterval < endInterval:
            if(curr in newDict.keys()):
                newDict[curr] += int(p[1])
            else:
                newDict[curr] = int(p[1])
        else:
            start += 1
            curr += 1
            if(curr in newDict.keys()):
                newDict[curr] += int(p[1])
            else:
                newDict[curr] = int(p[1])
    return newDict


def sniffy(mon_iface, channel):
    print("in sniffy method")
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
        capture.apply_on_packets(packetHandler, timeout=65)
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
    # sumSRC80 = 0
 # sumSRC68 = 0
    # for key in src_dict.keys():
    #     if key == "80:a5:89:ae:c6:5b":
    #         print("---------------------",key,"---------------------")
    #         print(src_dict[key])
    #         for tup in src_dict[key]:
    #             sumSRC80 += int(tup[1])
    #     if key == "68:c4:4d:92:ac:0a":
    #         print("---------------------",key,"---------------------")
    #         print(src_dict[key])
    #         for tup in src_dict[key]:
    #             sumSRC68 += int(tup[1])

    # print("*******************",sumSRC80,"*******************")
    # print("*******************",sumSRC68,"*******************")
    
    # sumSRC68R = refactor([('1584511350.902847449', '158'), ('1584511350.923037555', '158'), ('1584511371.744648014', '86'), ('1584511371.819352186', '154'), ('1584511372.021639118', '86')])

    # print(sumSRC68R)


    for k in src_dict.keys():
        new_dict[k] = refactor(src_dict[k])

    print("src_dict: \n", src_dict)
    # for k in src_dict.keys():
    #     # print(k)
    #     if k == "80:a5:89:ae:c6:5b" or k == "68:c4:4d:92:ac:0a":
    #         print("---------------------",k,"---------------------")
    #         print(src_dict[k])
           
    print("new_dict: \n", new_dict)
    arr1 = analysis.analysis('recording.aac')

    for k in new_dict.keys():
        # print(k)
        # if k == "80:a5:89:ae:c6:5b" or k == "68:c4:4d:92:ac:0a":
            # print("---------------------",k,"---------------------")
            # print(new_dict[k])
        # arr2 = new_dict[k]
        barr = []
        for k2 in new_dict[k]:
            barr.append(new_dict[k][k2])
            
        new_dict[k] = barr
        print('analyzing ', k)
        if (len(arr1) == len(barr)) :
            analysis.compareByteArrays(arr1, barr, 50)
        else: 
            print('not the same size')

        sniffedIndex = k

    # system call to compare two Byte Arrays
    # get array
    # arr1 = analysis.analysis('recording.aac')
    
    # analysis.compareByteArrays(arr1, arr2, 50)

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
