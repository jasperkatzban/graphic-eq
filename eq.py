# @author: Aydin O'Leary (@zbwrm), Jasper Katzban (@jasperkatzban)
# Top-level graphic equalizer

import pyaudio
import numpy as np
import wave
import time
import sys

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

wf = wave.open(sys.argv[1], 'rb') # open wav file in read only mode

# instantiate PyAudio (1)
p = pyaudio.PyAudio()



def mycallback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    # data = wf.readframes(500)
    # print(data.hex()) 
    return (data, pyaudio.paContinue)



# define callback (2)
def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    # data = wf.readframes(500)
    # print(data.hex()) 
    return (data, pyaudio.paContinue)

# open stream using callback (3)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)

# start the stream (4)
stream.start_stream()

# wait for stream to finish (5)
while stream.is_active():
    time.sleep(0.1)

# stop stream (6)
stream.stop_stream()
stream.close()
wf.close()

# close PyAudio (7)
p.terminate()

def fft(self, parameter_list):
       """
       docstring
       """
       pass

def ifft(self, parameter_list):
       """
       docstring
       """
       pass

def fitersample(self, parameter_list):
       """
       docstring
       """
       pass