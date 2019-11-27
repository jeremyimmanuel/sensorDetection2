import subprocess
import math
import pyshark

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


def generate_array_of_inputs_per_windowSize2( cap):
    inputsCount = [0] * 60
    for pkt in cap:
        if math.floor(float(pkt.time)) < 60:
            inputsCount[math.floor(float(pkt.time))] += int(pkt.length)
    return inputsCount

#def calculate_cross_correlation(self,windowSize,inputType):
#    print ('start cross correlation:: Window Size:', windowSize," ms")
#
#    analysis_time = 60  #60 seconds
#    cap = pyshark.FileCapture(self.newFile,only_summaries=True,keep_packets = False)
#    testCapWindows = self.generate_array_of_inputs_per_windowSize(cap,inputType,analysis_time, windowSize)
#
#    flash_pattern = [0]*len(testCapWindows)
#    # test files from camera contained the flash numbers
#    if '=' in self.newFile:
#        flash = self.newFile[self.newFile.index('=')+1:]
#        fl = []
#        x = 0
#        for i in range(1, len(flash)):
#            if flash[i] == ',' or flash[i] == '.':
#                fl.append(int(flash[x:i]))
#                x = (i+1)
#
#    # test files generated from non-signal, create dummy peak for testing data
#    else:
#        print ('no input time soecific, use auto-gen time slot')
#        fl = [5,14,23,32,41,50,59]
#
#for i in range(len(flash_pattern)):
#    if i in fl:
#        flash_pattern[i] = 1
#        print ('time of interaction::')
#        print (fl)
#
#        #NORMALIZES based on sd
#        std = np.std(testCapWindows)
#        if self.USE_MEDIAN:
#            valbase = np.median(testCapWindows)
#    else:
#        valbase = np.mean(testCapWindows)
#
#        if self.FILTER_TROUGHS:
#            print ('-----------filtering the troughs---------------')
#            for i, val in enumerate(testCapWindows):
#                if val < (valbase - self.trough_mult * std):
#                    testCapWindows[i] = valbase
#
#if self.FILTER_PEAK:
#    print ('-----------filtering the peaks---------------')
#    for i, val in enumerate(testCapWindows):
#        if val > (valbase + self.trough_mult * std):
#            testCapWindows[i] = max(testCapWindows)
#
#        if (max(testCapWindows) - min(testCapWindows)) != 0:
#            normalized_data = [round((input-min(testCapWindows))/float((max(testCapWindows) - min(testCapWindows))),5)
#                               for input in testCapWindows]
#        else:
#            print ('ERROR::::Array does not contain any input data')
#            print ('::Correlation Coefficient:: N/A \n')
#            return 'N/A'
#
#        # plt.figure()
#        # plt.plot([v for v in xrange(len(normalized_data))], normalized_data,'r')
#        # plt.xlim(0, len(normalized_data) - 1)
#        # plt.title('Bits / s')
#        # plt.show()
#
#
#        print ('::Correlation Coefficient:: \n',np.corrcoef(flash_pattern,normalized_data)[0][1])
#        return np.corrcoef(flash_pattern,normalized_data)[0][1]

    
# normalize arr
def normalizeArr(arr: list):
    arrSize = 0
    #count up all the bytes 
    for byteSize in arr:
        arrSize += byteSize
    
    #divide each element in array by the size
    for i in range(len(arr)):
        arr[i] = arr[i] / arrSize

    return arr
        
def compareByteArrays(arr1: list, arr2: list, threshold: float) -> bool :
    
    # normalize the given byte arrays
    norm_arr1 = normalizeArr(arr1)
    norm_arr2 = normalizeArr(arr2)

    # compare the arrays considering the threshold (for now 1.0)
    # returns true if all byteSize in arrays are "close enough"
    for i in range(len(arr1)):
        if (abs(arr1[i] - arr2[i]) > threshold) :
            return false

def main():
    # jerWav = generate_array_of_byte_in_video('jeremyRecording.wav') # attacker package
    #   attcap = pyshark.FileCapture(attackerCap,only_summaries=True,keep_packets = False)
    
    attcap = pyshark.FileCapture('Test1=10,20,30,40,50,60.pcapng',only_summaries=True,keep_packets = False)
    attarr2 = generate_array_of_inputs_per_windowSize2(attcap) # protector wav


    jojocap = pyshark.FileCapture('jojo.pcapng', only_summaries=True, keep_packets = False)
    jojoArr = generate_array_of_inputs_per_windowSize2(jojocap)

    # generate_array_of_inputs_per_windowSize('Test1=10,20,30,40,50,60.pcapng', "packets", 60, 2)

    
    print("attarr2 : \n")
    print(attarr2)
    
    print("jojoArr : \n")
    print(jojoArr)

    if (compareByteArrays(attarr2, jojoArr, 1.0)):
        print("they are similar!")
    else :
        print("they aren't similar!")
        
if __name__ == '__main__':
    main()
