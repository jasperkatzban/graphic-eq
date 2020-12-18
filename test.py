#! /usr/bin/python

import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
import time
import scipy.fftpack as ft
import filters as f
import gui as g
import tkinter as tk


CHUNK = 1024 * 1
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
PLOTTING = True
DEBUG = False

p = pyaudio.PyAudio()


# instantiate filter
# A = f.filtarray(preset='band')
# T = A.build()

# launch GUI
root = tk.Tk()
gui = g.App(root)
root.mainloop()

# funky function defs
def callback(in_data, frame_count, time_info, status):   
    global data, fft_data, fft_data_filtered, filt_data_out, filt_data_plot

    data = struct.unpack(str(CHUNK) + 'h', in_stream.read(CHUNK))
    fft_data = ft.rfft(data)
    T = gui.get_spectrum()
    print(T)
    fft_data_filtered = np.multiply(fft_data,T)
    filt_data_plot = ft.irfft(fft_data_filtered)
    np.clip(filt_data_plot,-30000, 30000)
    filt_data_out = tuple([int(i) for i in filt_data_plot])

    if DEBUG:
        
        print('In/Out: \t', in_stream.read(CHUNK)[0], '\t', struct.pack(str(CHUNK) + 'l', *filt_data_out)[0])
    return (struct.pack(str(CHUNK) + 'h', *filt_data_out), pyaudio.paContinue)

# define input and output audio streams
in_stream = p.open(format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=False,
    frames_per_buffer=CHUNK
)

out_stream = p.open(format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=False,
    output=True,
    frames_per_buffer=CHUNK,
    stream_callback=callback
)

# set up active plotting
if PLOTTING:
    plt.ion()
    fig1, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)

x = np.arange(0, 2*CHUNK,2)
fft_x = np.linspace(0,RATE,CHUNK)

data = in_stream.read(CHUNK)
data_int16 = struct.unpack(str(CHUNK) + 'h', data)

if PLOTTING:
    line, = ax1.plot(x, data_int16)
    filt_line, = ax3.plot(x, data_int16, 'r')

    fft_line, = ax2.semilogx(fft_x, np.random.rand(CHUNK))
    filt_fft_line, = ax4.semilogx(fft_x, np.random.rand(CHUNK), 'r')

    ax1.set_ylim([-2**15,(2**15)-1])
    ax1.set_title('Unfiltered Audio')

    ax3.set_ylim([-2**15,(2**15)-1])
    ax3.set_title('Filtered Audio')

    ax2.set_ylim(20, CHUNK * 2)
    ax2.set_title('Unfiltered FFT')
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Amplitude')

    ax4.set_ylim(20, CHUNK * 2)
    ax4.set_title('Filtered FFT')
    ax4.set_xlabel('Frequency (Hz)')
    ax4.set_ylabel('Amplitude')


# begin streaming
out_stream.start_stream()

if DEBUG:
    print(type(data), 'made it')

time.sleep(1)
# root = tk.Tk()
# gui = g.App(root)
# root.mainloop()

while out_stream.is_active():
    # T = gui.get_spectrum()
    # print(T)
    if PLOTTING:
        fft_line.set_ydata(fft_data * 2 / (CHUNK))
        filt_fft_line.set_ydata(fft_data_filtered * 2 / (CHUNK))
        if DEBUG:
            print('finish setting fft data')
        # if time.monotonic() % .5 == 0:
        #     T = A.build()

        line.set_ydata(data)
        filt_line.set_ydata(filt_data_out)
        if DEBUG:
            print('finish setting line data')
        fig1.canvas.draw()
        fig1.canvas.flush_events()
        if DEBUG:
            print('finish flush')
    else:
        time.sleep(0.01)