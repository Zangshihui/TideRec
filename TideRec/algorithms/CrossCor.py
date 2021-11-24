import numpy as np
from TideRec.algorithms.Cal.CalSource import CalSource

class CrossCor(CalSource):
    """
    This class provides the algorithm to calculate the power spectrum.

    Parameters
    ----------
    """

    def __init__(self, mode = 'Rec', Dim = '1D', *args, **kwargs):
        super(CrossCor, self).__init__(*args, **kwargs)

    def Compute(self, Dim = '1D'):
        """
        
        Available Dim:
        1) 1D
        2) 2D
        """
        self.rank_print('=' * 80)
        self.rank_print('Cross Correlation parameters:')
        self.rank_print('Dim: %s' % (Dim))
        self.rank_print('Cross Correlation computing ...')

        try:
            self.delta
        except:
            raise ValueError('Please input dark matter density field!')
        deltak1 = self.fft(self.delta)
        deltak2 = self.fft(self.delta_re)
        pk1 = (deltak1*np.conjugate(deltak1)).real
        pk2 = (deltak2*np.conjugate(deltak2)).real
        pkc = (deltak1*np.conjugate(deltak2)).real

        if Dim == '1D':
            n, k, pk1 = self.UniDimension(pk1)
            n, k, pk2 = self.UniDimension(pk2)
            n, k, pkc = self.UniDimension(pkc)
            if self.rank == 0:
                rk = pkc/(pk1*pk2)**0.5
        elif Dim == '2D':
            n, k, rk = self.BiDimensionBin(pk, Nmu = 5)
        else:
            raise ValueError('Dim mode is not available!')
            
        self.rank_print('Cross Correlation compute completed.')
        self.rank_print('=' * 80)

        if self.rank == 0:
            return n, k, rk
        else:
            return None, None, None

if __name__ == '__main__':
    s = Power()