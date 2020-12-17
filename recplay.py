import pyaudio
import numpy as np
import time
import sys
import wave
import matplotlib.pyplot as plt
import scipy.fftpack
# import math


CHANNELS = 1
RATE = 44100 # sample rate
CHUNK = 2**10 # buffer size
FFT_RES = RATE
NUM_BANDS = 8
BAND_VALS = [0, 0, 0, 1, 0, 0, 0, 0]

live = True # switch between live or prerecoreded input

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
        # sample = str(wf.readframes(frame_count), 'windows-1252')  # bytes type # maybe try ISO-8859-1?
        # sample = wf.readframes(frame_count)
        data = np.fromstring(sample.hex(' ', -4), dtype=np.float32) 

    # try:
    #     spectrum = np.abs(np.fft.rfft(data)[1:])
    # except:
    #     spectrum = np.fft.fft(data)
    #     left, right = np.split(np.abs(FFT), 2)
    #     spectrum = np.add(left, right[::-1])

    # print(wf.readframes(frame_count))
    # print(sample)

    # print(data, "\n")

    # spectrum = np.fft.fft(data, n=FFT_RES)
    # spectrum = np.fft.fftshift(np.fft.rfft(data))
    spectrum = np.fft.rfft(data, n=10)

    spectrum_filt = spectrum                                            # FILTERING STAGE HERE
    print(len(spectrum))
    # print(spectrum[0])

    n = data.size
    # freq = np.fft.rfftfreq(n, 1/RATE)

    # plt.plot(freq, np.abs(spectrum))
    plt.plot(np.abs(spectrum))
    plt.show

    # data_filt = np.fft.irfft(np.fft.ifftshift(spectrum_filt))
    data_filt = np.fft.irfft(spectrum_filt)

    
    # data_filt = np.fft.ifft(spectrum, n=FFT_RES)
    # data_filt = np.fft.rifft(spectrum)

    plt.show()
    
    # for sample in data_filt:
    #     if np.isnan(sample):
    #     # if sample == 'nan':
    #         data_filt = ([np.float(0)] * len(data_filt)).to_bytes()

    return data_filt, pyaudio.paContinue

if live: # live audio stream setup
    stream = p.open(format=pyaudio.paFloat32,
                    channels=CHANNELS,
                    rate=RATE,
                    output=False,
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