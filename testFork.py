import os
import time

tsharkPID = ''

pid = os.fork()
if pid == 0:
    tsharkPID = os.getpid
    print(tsharkPID)
    # os.system('tshark -w livecap.pcap')
    p = os.system('pidof tshark')
    print(p)

else:
    time.sleep(5)
    os.system('kill ' + tsharkPID)