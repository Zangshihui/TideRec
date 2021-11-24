import numpy as np
from TideRec.core.fft import fft


class Utils(fft):
    """
    This class contains some tools including Gaussian filter and deconvolution

    Parameters:
    -----------

    TO DO: Deconvolution
    """
    def __init__(self, BoxSize = 300, NMesh = 128, **kwargs):
        super(Utils, self).__init__(BoxSize=BoxSize, NMesh=NMesh, **kwargs)

    def Get(self, dataname = None):
        """
        Get private data of Rec()

        Available dataname:
            1) delta
            2) delta_re
            3) density
            4) density_re
            5) NMesh
            6) BoxSize
        """
        if dataname is None:
            raise ValueError('Please input dataname!')
        if dataname == 'delta':
            return self.delta
        elif dataname == 'delta_re':
            return self.delta_re
        elif dataname == 'density':
            return self.delta + 1
        elif dataname == 'density_re':
            return self.delta_re + 1
        elif dataname == 'NMesh':
            return self.NMesh
        elif dataname == 'BoxSize':
            return self.BoxSize
        else:
            raise ValueError('dataname is not available!')

    def _GaussianWindow(self, sigma):
        window = np.exp(-0.5 * (self.k_ind * self.Kf) ** 2. * sigma**2.)
        return window

    def convolve_fft(self, a, b):
        """
        Convolution in Fourier space.
        return the result in Fourier space

        Parameters
        ----------
        a: 
            data in configure space
        b: 
            window function in Fourier space
        """
        a = self.fft(a)
        result = self.ifft(a*b)
        return result

    def Smooth(self, data, sigma):
        """
        Gaussian smooth tool.

        Parameters
        ----------
        data:
            data to smooth with shape [NMesh/size, NMesh, NMesh]
        sigma:
            Gaussian smooth scale
        """
        window = self._GaussianWindow(sigma)
        return self.convolve_fft(data, window)

    def Preview(self, sigma):
        pass

if __name__ == '__main__':
    utils = Utils()