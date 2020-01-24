# Sensor Detection App Data Collection app

This app was used as a data collection method for a research project led by Dr. Brent Lagesse Ph.D.

The app is an implementation of a flask and flask-socketio in Python as the server while having multiple android apps as clients which was written in Java

Contributors: Anwar Aminuddin, Jun Zhen, Donghee Lee, Jeremy Tandjung

Check their github repo at:<br>
https://github.com/jeremyimmanuel <br>
https://github.com/heedong0612 <br>
https://github.com/anwara96 <br>
https://github.com/jpzhen <br>

# Dependencies 
## Python
* flask
* flask-socketio
* evenlet 
* pyshark
* tshark 

# Citation
* Nkazawa socket io client for java
https://github.com/socketio/socket.io-client-java

# Instruction
## Setup
### Server
1. Check your ip address, put it on a note
2. Run androidRecordPlayServer.py on a computer

### Client
1. Run android studio and open 'SensorDetectionApp'  
2. Go to app/java/Constants
3. Change the ip address to the noted ip address 

### Execution
1. Open all devices that's installed with the app
2. You're going to have two options; PLAYER or RECORDER
3. There can only be <b>ONE</b> PLAYER at a time 
4. Set one device to be PLAYER and the rest to be RECORDER
5. Connect PLAYER first, then all the RECORDERs
6. Press start button on PLAYER, RECORDER will show 'recording' page and <b>start recording</b>
7. To stop recording, press the <b>stop</b> button on PLAYER
8. All recording will be saved in a folder in the directory of the python server.
9. sniffsniff.py will be executed along with the recording in sync, producing a pcapSniff.txt
10. Server will also run analysis.py to compare audio recording and pcapSniff
11. Server will output if the bytearrays are similar or not

# Future 
1. Setup GUI for server
2. Make a Desktop, iOS client?
3. Give client ability to set server address
