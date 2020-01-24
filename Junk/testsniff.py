import pyshark

cap = pyshark.LiveCapture(interface = 'en0')
print('cap object created')
cap.sniff(timeout = 4)
print("end of sniffy")