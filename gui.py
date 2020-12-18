import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import filters as f
import matplotlib.pyplot as plt
import struct
import numpy as np

CHUNK = 1024 * 2
RATE = 44100
FFT_X = np.linspace(0,RATE,CHUNK)
DEFAULT_BANDS = 8

PLOTTING = True

class App:

    def __init__(self, master):

        self.master = master

        self.n = DEFAULT_BANDS
        self.gain = [0] * self.n
        self.gen_bands()

    def gen_bands(self):
        self.band = []
        for i in range(self.n):
            self.band.append(tk.Scale(orient='vertical', from_=1, to=-1, resolution=.01, command=self.update_spectrum, width=15))
            self.band[i].pack(fill=tk.Y, side=tk.LEFT, expand=True, padx=5, pady=5)

        self.A = f.filtarray(n=self.n, preset='default') # todo: implement n-band

        # Create a container
        frame = tk.Frame(self.master)

        # # Create 2 buttons
        # self.button_left = tk.Button(frame,text="< Decrease Slope",
        #                                 command=self.decrease)
        # self.button_left.pack(side="left")
        # self.button_right = tk.Button(frame,text="Increase Slope >",
        #                                 command=self.increase)
        # self.button_right.pack(side="left")

        fig = Figure()
        ax = fig.add_subplot(111)
        self.line, = ax.semilogx(FFT_X, [1] * len(FFT_X))
        ax.set_ylim([0,2])
        # ax.xscale('log')
        ax.grid()
        
        self.canvas = FigureCanvasTkAgg(fig,master=self.master)  
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        frame.pack()

    def update_spectrum(self, val):
        for i in range(self.n):
            self.gain[i] = self.band[i].get()
            self.A.filters[i].g = self.gain[i]
        self.T = self.A.build()
        if PLOTTING:
            self.line.set_ydata(self.T)
            self.canvas.draw()
        return

    def decrease(self):
        self.n -= 1
        self.gen_bands()

    def increase(self):
        self.n += 1
        self.gen_bands()

root = tk.Tk()
app = App(root)
root.mainloop()