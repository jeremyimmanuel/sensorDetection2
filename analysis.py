import subprocess
import math
import pyshark
import sys

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


def generate_array_of_inputs_per_windowSize2(cap):
    '''
    cap is a captured package with pyshark
    '''
    inputsCount = [0] * 60
    for pkt in cap:
        if math.floor(float(pkt.time)) < 60:
            inputsCount[math.floor(float(pkt.time))] += int(pkt.length)
    return inputsCount
    

def normalizeArr(arr: list) -> list:
    '''
    Normalizes the given byte array
    '''
    norm_arr = []
    arrSize = 0
    
    # sums up all the bytes 
    for byteSize in arr:
        arrSize += byteSize
    
    # divide each element in array by the sum
    if (arrSize > 0):
        for i in range(len(arr)):
            norm_arr.append(arr[i] / arrSize)
    else: 
        print("The array is empty or contains no bytes")

    return norm_arr
        

  
def compareByteArrays(arr1: list, arr2: list, threshold: float) -> bool :
    '''
    Compares two byte arrays arr1 and arr2 and returns true if they're similar 
    considering the threshold passed
    ''' 
    # normalizes the byte arrays
    norm_arr1 = normalizeArr(arr1)
    norm_arr2 = normalizeArr(arr2)

    # compare the arrays considering the threshold (for now 1.0)
    # returns true if all byteSize in arrays are "similar"
    for i in range(len(60)):
        if (abs(arr1[i] - arr2[i]) > threshold) :
            return False

    return True

def analysis(filename: str):
    '''
    String filename is the name of the file to be analyzed
    '''
    print('Analyzing...')
    print('filename is: %s' % filename)
    with open(filename, "rb") as binary_file:  
        array1 = binary_file.read()  # Read the whole file at once

    # cap1 = pyshark.FileCapture(filename,only_summaries=True,keep_packets = False)
    # cap1.set_debug()
    # array1 = generate_array_of_inputs_per_windowSize2(cap1) # protector wav
    # cap1.close() 

    testFile = open('livecap.pcap', 'r') # hardcoded -- sniffed text file
    array2 = str.encode(testFile.read()) # converts to byte array
    testFile.close()

    # Compares two byte arrays and determine whether they're similar
    if(compareByteArrays(array1,array2,1.0)):
        print("Analysis: Similar")
    else:
        print("Analysis: Not similar")

if __name__ == '__main__':
    analysis(sys.argv[1])



# Functions we're not using anymore, but leaving it for reference for now

# def main():
    # jerWav = generate_array_of_byte_in_video('jeremyRecording.wav') # attacker package
    #   attcap = pyshark.FileCapture(attackerCap,only_summaries=True,keep_packets = False)
    
    # attcap = pyshark.FileCapture('Test1=10,20,30,40,50,60.pcapng',only_summaries=True,keep_packets = False)
    # attarr2 = generate_array_of_inputs_per_windowSize2(attcap) # protector wav


    # jojocap = pyshark.FileCapture('jojo.pcapng', only_summaries=True, keep_packets = False)
    # jojoArr = generate_array_of_inputs_per_windowSize2(jojocap)

    # # generate_array_of_inputs_per_windowSize('Test1=10,20,30,40,50,60.pcapng', "packets", 60, 2)

    
    # print("attarr2 : \n")
    # print(attarr2)
    
    # print("jojoArr : \n")
    # print(jojoArr)
    # print("hi")

    # if (compareByteArrays(attarr2, jojoArr, 1.0)):
    #     print("they are similar! They might be spying..")
    # else :
    #     print("they aren't similar!")


# Generate the byte stream of 60 seconds 
# def generate_array_of_byte_in_video(videoFile):
#     print ('Start decode the video file. ')
#     setTime = 60
#     decodedByteArray = [0] * setTime
#     curser = 0
#     frameCount = 0
#     command = ['ffprobe', '-show_entries', 'frame=pkt_size,pkt_pts_time', videoFile]
#     p = subprocess.Popen(command, stdout=subprocess.PIPE)
#     decodedFrames = p.stdout.read().decode('utf-8')
#     retcode = p.wait()
    
#     while True:
#         if decodedFrames.find('pts_time', curser) == -1:
#             print ('Finish decoding ' + videoFile +' for:: ' + str(setTime) + 's')
#             break
    
#         frameTime = decodedFrames[decodedFrames.find('pts_time', curser) + 9 :decodedFrames.find('pkt_size', curser) - 1]
#         frameSize = decodedFrames[decodedFrames.find('pkt_size', curser) + 9 :decodedFrames.find('[/FRAME]', curser) - 1]
        
#         #print ("------------------------------"+ frameTime + 's:'+frameSize)
        
#         frameCount += 1
#         #print ('frame '+str(frameCount) + '===================\ntime = <'+frameTime + '>')
#         #print ('size = <'+frameSize + '>')
#         if math.floor(float(frameTime)) <= 59:
#             decodedByteArray[math.floor(float(frameTime))] += int(frameSize)
#         curser = decodedFrames.find('[/FRAME]', curser) + 8
#         #print ('curser loaction '+str(curser))
#     return decodedByteArray
#    