#! /usr/bin/python

import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
import time
import scipy.fftpack as ft
import filters


#%matplotlib tk

CHUNK = 1024 * 2
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)


plt.ion()
fig, (ax1, ax2) = plt.subplots(2)

x = np.arange(0, 2*CHUNK,2)
fft_x = np.linspace(0,RATE,CHUNK)

data = stream.read(CHUNK)
data_int16 = struct.unpack(str(CHUNK) + 'h', data)

line, = ax1.plot(x, data_int16)
fft_line, = ax2.semilogx(fft_x, np.random.rand(CHUNK))

ax1.set_ylim([-2**15,(2**15)-1])
ax2.set_ylim(20, CHUNK * 2)


A = filtarray('default')
T = A.build()

while True:
    data = struct.unpack(str(CHUNK) + 'h', stream.read(CHUNK))

    fft_data = ft.rfft(data)

    # FILTERING HERE on fft_data
    fft_data_filtered = np.multiply(fft_data,T)

    fft_line.set_ydata(fft_data * 2 / (CHUNK))

    if time.monotonic() % .5 == 0:
        T = A.build()

    line.set_ydata(data)
    fig.canvas.draw()
    fig.canvas.flush_events()
    stream.write(data)