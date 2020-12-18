import numpy as np
import matplotlib.pyplot as plt

RATE = 44100
CHUNK = 2048
FFT_X = np.linspace(0,RATE,CHUNK)

class filter:
    """
    Filter class, including lowpass, bandpass, and high pass options.
    """

    def __init__(self, mode, f, g=0, q=1):
        """
        Init function
        """
        self.width = len(FFT_X) # width of spectrum
        self.mode = mode # filtering mode
        self.f = f # cutoff or center frequency depending on mode
        self.g = g # filter band gain
        self.q = q # q factor
        # self.m = m # slope of filter response
        self.w = 10 # width of filter region for bandpass and block filters

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
        # print('Slope: ', self.m)
        print('Band Width: ', self.w)

    def update(self,mode,f,g,q):
        """
        Update filter
        """
        # self.mode = m
        return self

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

        return r
    
    def bandpass(self):
        """
        Bandpass filter
        """
        r = np.empty(self.width) # initialize transformation vector

        f_lo = (self.f-self.w/2)
        f_hi = (self.f+self.w/2)
        f_0 = np.sqrt(f_lo*f_hi)

        for i in range(self.width):
            r[i] = self.g/(np.sqrt(1 + self.q**2 * ((FFT_X[i]/(f_0)) - (f_0/(FFT_X[i])))**2))

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



class filtarray:
    """
    Filter array class
    """

    def __init__(self, n=8, preset=None):
        """
        Init function
        """
        self.n = n # num of filter bands
        self.preset = preset
        self.filters = []
        self.array = filtarray.load(self)
        self.width = len(FFT_X)
        

    def load(self):
        """
        load filter from preset or default
        """        

        if self.preset == 'default' or self.preset == None:
            self.n = 8
            self.f = np.logspace(1, np.log10(RATE/2-1000), num=self.n)
            for i in range(self.n):
                self.filters.append(filter('bp', f=self.f[i], g=1, q=20))
        return self.filters

    def build(self):
        """
        docstring
        """        
        # w = np.empty((self.n, self.width))
        comp = np.empty((self.n,self.width))
        for i in range(self.n):
            comp[i] = self.filters[i].get()
        
        w = comp.sum(axis=0)
        return w # return array of spectrum weights


# A = filtarray('default')
# T = A.build()
# print(T)
# print(A.f)
# plt.plot(FFT_X, T) 

# plt.xscale('log')
# # plt.xlim([0,RATE/2])
# plt.grid()

# # plt.yscale('log')
# # plt.xlim(0,len(FFT_X))
# # plt.ylim(-inf)

# plt.show()