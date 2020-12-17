import pyaudio
import numpy as np
import time
import sys
import wave
import matplotlib.pyplot as plt
# import math


CHANNELS = 2 
RATE = 44100 # sample rate
CHUNK = 2**5 # buffer size

live = False # switch between live or prerecoreded input

if not live:
    if len(sys.argv) < 2:
        print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
        sys.exit(-1)
    
    wf = wave.open(sys.argv[1], 'rb') # open wav file in read only mode

p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, flag):
    if live:
        data = np.fromstring(in_data, dtype=np.float32) # using Numpy to convert to array for processing
    else:
        sample = wf.readframes(frame_count)
        data = np.frombuffer(sample, dtype=np.float32) 
        # data = wf.readframes(frame_count)

    # try:
    #     spectrum = np.abs(np.fft.rfft(data)[1:])
    # except:
    #     spectrum = np.fft.fft(data)
    #     left, right = np.split(np.abs(FFT), 2)
    #     spectrum = np.add(left, right[::-1])
    
    spectrum = np.fft.rfft(data)
    data_filt = np.fft.irfft(spectrum)
    
    for sample in data_filt:
        if np.isnan(sample):
        if sample == 'nan':
            data_filt = [np.float(0)] * len(data_filt)

    # spectrum = np.fft.fft(data)
    # freq = np.fft.fftfreq(data.shape[-1])

    # raw_filt = np.fft.ifft(spectrum)
    # # data_filt = np.frombuffer(raw_filt, dtype=np.float32) 
    # data_filt = raw_filt.real
    
    # print(data[0], "\t", data_filt[0])
    print(data_filt.shape)
    print(type(data_filt[0]))
    # print(data_filt)

    # print(len(data), data)
    # print(wf.getsampwidth())
    # print(data[0])
    return data_filt, pyaudio.paContinue


if live: # live audio stream setup
    stream = p.open(format=pyaudio.paFloat32,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    input=True,
                    stream_callback=callback,
                    frames_per_buffer=CHUNK)
    
else: # file audio stream
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback,
                    frames_per_buffer=CHUNK)

stream.start_stream()

while stream.is_active():
    time.sleep(0.1)
#     stream.stop_stream()
#     print("Stream is stopped")

# stop stream
stream.stop_stream()
stream.close()
# wf.close()