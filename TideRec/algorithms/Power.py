import numpy as np
from TideRec.algorithms.Cal.CalSource import CalSource

class Power(CalSource):
    """
    This class provides the algorithm to calculate the power spectrum.

    Parameters
    ----------
    """

    def __init__(self, mode = 'Rec', Dim = '1D', *args, **kwargs):
        super(Power, self).__init__(*args, **kwargs)

    def Compute(self, mode = 'Rec', Dim = '1D'):
        """
        Available modes:
        1) Rec
            Calculate the power spectrum of Reconstructed density field.
        2) DM
            Calculate the power spectrum of dark matter field.
        3) Cross
            Calculate the cross power spectrum of dark matter field and reconstructed field.
        
        Available Dim:
        1) 1D
        2) 2D
        """
        self.rank_print('=' * 80)
        self.rank_print('Power parameters:')
        self.rank_print('mode: %s, Dim: %s' % (mode, Dim))
        self.rank_print('Power computing ...')

        if mode == 'Rec':
            deltak = self.fft(self.delta_re)
            pk = ((deltak*np.conjugate(deltak))*self.BoxSize**3).real

        elif mode == 'DM':
            try:
                self.delta
            except:
                raise ValueError('Please input dark matter density field!')
            deltak = self.fft(self.delta)
            pk = ((deltak*np.conjugate(deltak))*self.BoxSize**3).real

        elif mode == 'Cross':
            try:
                self.delta
            except:
                raise ValueError('Please input dark matter density field!')
            deltak1 = self.fft(self.delta)
            deltak2 = self.fft(self.delta_re)
            pk = ((deltak1*np.conjugate(deltak2))*self.BoxSize**3).real

        else:
            raise ValueError('Power Mode is not available!')

        if Dim == '1D':
            n, k, pk = self.UniDimension(pk)

        elif Dim == '2D':
            n, k, pk = self.BiDimensionBin(pk, Nmu = 5)

        else:
            raise ValueError('Dim mode is not available!')

        self.rank_print('Power compute completed.')
        self.rank_print('=' * 80)

        if self.rank == 0:
            return n, k, pk
        else:
            return None, None, None

if __name__ == '__main__':
    s = Power()