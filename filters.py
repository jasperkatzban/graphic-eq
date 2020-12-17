class filter:
    """
    Filter class, including lowpass, bandpass, and high pass options.
    """

    def __init__(self, arr, mode, f, g=0, q=1, m=1, w=1):
        """
        Init function
        """
        self.mode = mode # filtering mode
        self.f = f # cutoff or center frequency depending on mode
        self.g = g # filter band gain
        self.q = q # q factor
        self.m = m # slope of filter response
        self.w = w # width of filter region for bandpass and block filters
        
        if mode == 'lp' or 0:
            return lowpass(arr, f, g, q, m)
        elif mode == 'bp' or 1:
            return bandpass(arr, f, g, q, m, w)
        elif mode == 'hp' or 2:
            return highpass(arr, f, g, q, m)
        elif mode == None or 'p' -1:
            return arr

    def update(self)
        """
        Update filter
        """
        pass

    def lowpass(self, f, g, q, m):
        """
        Lowpass filter
        """
        t = np.zeroes_like(arr) # initialize transformation vector
        pass
    
    def bandpass(self, f, g, q, m, w):
        """
        Bandpass filter
        """
        
        pass
    
    def highpass(self, f, g, q, m):
        """
        Highpass filter
        """

        pass

    def block(self, f, g, w):
        """
        Block band filter
        """
        f_lo = int(f-w/2)
        f_hi = int(f+w/2)

        t = np.zeroes_like(arr) # initialize transformation vector
        t[f_lo, f_hi] = g
        return t


sp_bands = bands.get_weights() # get eq bands into matrix?
sp_weights = sp_bands.sum(axis=0) # sum eq band spectrums by column