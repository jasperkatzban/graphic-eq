import numpy as np
import matplotlib.pyplot as plt

RATE = 44100
CHUNK = 2048
FFT_X = np.linspace(0,RATE,CHUNK)

class filter:
    """
    Filter class, including lowpass, bandpass, and high pass options.
    """

    def __init__(self, mode, f, g=0, m=1, q=1, w=1):
        """
        Init function
        """
        self.width = len(FFT_X) # width of spectrum
        self.mode = mode # filtering mode
        self.f = f # cutoff or center frequency depending on mode
        self.g = g # filter band gain
        self.q = q # q factor
        self.m = m # slope of filter response
        self.w = w # width of filter region for bandpass and block filters

    def getProps(self):
        """
        Get filter properties
        """
        print('Filter Properties:')
        print('------------------')
        print('Spectrum Width: ', self.width)
        print('Mode: ', self.mode)
        print('Freq: ', self.f)
        print('Gain: ', self.g)
        print('Q Factor: ', self.q)
        print('Slope: ', self.m)
        print('Band Width: ', self.w)

    def update(self):
        """
        Update filter
        """
        pass

    def lowpass(self):
        """
        Lowpass filter
        """
        r = np.empty(self.width) # initialize transformation vector

        f_lo = self.f-self.w/2
        f_hi = self.f+self.w/2
        f_0 = np.sqrt(f_lo*f_hi)

        for i in range(self.width):
            r[i] = self.g/(np.sqrt(1 + self.q**2 * ((FFT_X[i]/(f_0+1)))**2)) - self.g

        # for i in range(self.width):
        #     r[i] = self.m * np.log(self.f) - np.log(FFT_X[i])
        #     # t[i] = self.m * self.f/FFT_X[i]

        return r
    
    def bandpass(self):
        """
        Bandpass filter
        """
        r = np.empty(self.width) # initialize transformation vector

        f_lo = self.f-self.w/2
        f_hi = self.f+self.w/2
        f_0 = np.sqrt(f_lo*f_hi)

        for i in range(self.width):
            r[i] = self.g/(np.sqrt(1 + self.q**2 * ((FFT_X[i]/(f_0+1)) - (f_0/(FFT_X[i]+1)))**2))

        return r
    
    def highpass(self):
        """
        Highpass filter
        """
        r = np.empty(self.width) # initialize transformation vector

        f_lo = self.f-self.w/2
        f_hi = self.f+self.w/2
        f_0 = np.sqrt(f_lo*f_hi)

        for i in range(self.width):
            r[i] = (self.g/(np.sqrt(1 + self.q**2 * ((f_0/(FFT_X[i]+1)))**2))) - self.g

        return r

    def block(self):
        """
        Block band filter
        """

        f_lo_i = int((self.f-self.w/2)/CHUNK)
        f_hi_i = int((self.f+self.w/2)/CHUNK)
        
        print(f_lo_i, f_hi_i)
        r = np.zeros((self.width)) # initialize freq response vector
        r[f_lo_i:f_hi_i] = self.g
        return r
    
    def passthrough(self):
        """
        docstring
        """
        r = np.zeros((self.width), dtype=np.int32)
        return r

    def get(self):
        if self.mode == 'lp':
            return filter.lowpass(self)
        elif self.mode == 'bp':
            return filter.bandpass(self)
        elif self.mode == 'hp':
            return filter.highpass(self)
        elif self.mode == 'b':
            return filter.block(self)
        elif self.mode == 'p':
            return filter.passthrough(self)



class filtarray():
    """
    Filter array class
    """

    def assemble(self, filters):
        """
        docstring
        """
        self.filters = filters

        w = np.empty(self.width)

        for filter in filters:



        return w # return array of spectrum weights




w = 1
g = 10
m = 100
q = [.1, .5, 1, 3, 5, 10, 20, 40]
for i in range(len(q)):
    BP = filter('bp', f=1000, w=w, m=m, g=g, q=q[i])
    plt.plot(FFT_X, BP.get())

HP = filter('hp', f=1000, w=w, m=m, g=g, q=1) 
LP = filter('lp', f=1000, w=w, m=m, g=g, q=1)
plt.plot(FFT_X, HP.get())
plt.plot(FFT_X, LP.get())

B = filter('b', f=10000, w=4000,g=1)
# plt.plot(FFT_X, B.get())

plt.xscale('log')
plt.xlim([0,RATE/2])
plt.grid()
# plt.yscale('log')
# plt.xlim(0,len(FFT_X))
# plt.ylim(-inf)
plt.show()

# sp_bands = bands.get_weights() # get eq bands into matrix?
# sp_weights = sp_bands.sum(axis=0) # sum eq band spectrums by column