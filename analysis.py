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

def main():
    print('bruh')

if __name__ = '__main__':
    main()
