import subprocess
import math

# Generate the byte stream of 60 seconds
def generate_array_of_byte_in_video(videoFile):
    print ('Start decode the video file. ')
    setTime = 60
    decodedByteArray = [0] * setTime
    curser = 0
    frameCount = 0
    command = ['ffprobe', '-show_entries', 'frame=pkt_size,pkt_pts_time', videoFile]
    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    decodedFrames = p.stdout.read().decode('utf-8')
    retcode = p.wait()
    
    while True:
        if decodedFrames.find('pts_time', curser) == -1:
            print ('Finish decoding ' + videoFile +' for:: ' + str(setTime) + 's')
            break
    
        frameTime = decodedFrames[decodedFrames.find('pts_time', curser) + 9 :decodedFrames.find('pkt_size', curser) - 1]
        frameSize = decodedFrames[decodedFrames.find('pkt_size', curser) + 9 :decodedFrames.find('[/FRAME]', curser) - 1]
        
        #print ("------------------------------"+ frameTime + 's:'+frameSize)
        
        frameCount += 1
        #print ('frame '+str(frameCount) + '===================\ntime = <'+frameTime + '>')
        #print ('size = <'+frameSize + '>')
        if math.floor(float(frameTime)) <= 59:
            decodedByteArray[math.floor(float(frameTime))] += int(frameSize)
        curser = decodedFrames.find('[/FRAME]', curser) + 8
        #print ('curser loaction '+str(curser))
    #print (decodedByteArray)
    return decodedByteArray

def generate_array_of_inputs_per_windowSize(cap, inputs, analysis_time, windowSize):
    """
    cap is the captured package with pyshark
    inputs is a string of either bits, 1514, or packets
    analysis_time = 60
    windowSize =
    """
    window_time =  windowSize/float(1000)
    inputscount = []
    cur_time, total_inputs = window_time, 0.0
    for pkt in cap:
        if float(pkt.time) > cur_time: #pkt is later than currTime
            if float(pkt.time) > analysis_time: #pkt is later than analysis time
                break
            
            inputscount.append(total_inputs)
            gap = int ( ( (float(pkt.time) - cur_time) / window_time ) )
            if gap > 1:
                i = 0
                while i < gap:
                    inputscount.append(0)
                    cur_time += window_time
                    i += 1
        
            cur_time += window_time
        total_inputs = 0
        if inputs == 'bits':
            total_inputs += int(pkt.length)*8
        #why 1514??
        elif inputs == '1514':
            if int(pkt.length) == 1514:
                total_inputs += 1
        elif inputs == 'packets':
            total_inputs += 1
        else:
            print ('ERROR: wrong inputs type.')
            return None
        inputscount.append(total_inputs)
        return inputscount


def main():
    jerWav = generate_array_of_byte_in_video('jeremyRecording.wav') # attacker package
    dongWav = generate_array_of_byte_in_video('dongheeRecording.wav') # protector wav
    
    generate_array_of_inputs_per_windowSize(jerWav, 'packets', 60, 2)
    
    print(jerWav)
    print(dongWav)
    
    print('bruh')

if __name__ == '__main__':
    main()
