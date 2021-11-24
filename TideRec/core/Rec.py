import numpy as np
from TideRec.core.RS import RS


class Rec(RS):
    """
    This class contains the tidal reconstruction algorithms.
    
    
    TO DO: raise Value error (reconstruction has not been performed)

    Parameters
    ----------
    mode:
        two tidal reconstruction modes are available ( 5term and 2term )
    sigma:
        scale of Gaussian filter in estimating the shear field
    delta:
        density contrast
    deltak：
        density contrast in Fourier space

    """
    def __init__(self, BoxSize=300., NMesh=128, **kwargs):
        super(Rec, self).__init__(BoxSize=BoxSize, NMesh=NMesh, **kwargs)

        self.rank_print('=' * 80)
        self.rank_print('Reconstruction box parameters:')
        self.rank_print('BoxSize: %f, NMesh: %d' % (self.BoxSize, self.NMesh))
        self.rank_print('=' * 80)

    def AutoRec(self, mode = '5term', sigma = 1):
        """
        Method to call up tidal reconstruction.
        """
        try:
            self.delta
        except NameError:
            raise ValueError('Density field is not imported!')
        else:
            pass
    
        self.rank_print('=' * 80)
        self.rank_print('Tidal Reconstruction Parameters:')
        self.rank_print('RecMode: %s, Filter Scale: %f' % (mode, sigma))
        self.rank_print('Tidal reconstruction begins ...')

        if mode == '5term':
            self.Rec5(sigma)
        elif mode == '2term':
            self.Rec2(sigma)
        else:
            raise ValueError('Please choose reconstruction mode from 5term and 2term!')

        self.rank_print('Tidal reconstruction completed.')
        self.rank_print('=' * 80)

    def Rec5(self, sigma):
        """
        First estimate the filtered field
        """
        deltak = self.fft(self.delta)
        deltak *= self._GaussianWindow(sigma)*1j*self.Kf
        deltak1 = ((self.mpi_fn[self.rank][:, None, None]
                  + np.zeros(self.NMesh)[None, :, None]
                  + np.zeros(self.NMesh)[None, None, :])* deltak)
        deltak2 = ((np.zeros(int(self.NMesh/self.size))[:, None, None]
                  + self.fn[None, :, None] 
                  + np.zeros(self.NMesh)[None, None, :]) * deltak)
        deltak3 = ((np.zeros(int(self.NMesh/self.size))[:, None, None]
                  + np.zeros(self.NMesh)[None, :, None]
                  + self.fn[None, None, :])* deltak)
        del deltak
        deltax1 = self.ifft(deltak1).real
        deltax2 = self.ifft(deltak2).real
        deltax3 = self.ifft(deltak3).real
        del deltak1, deltak2, deltak3

        """
        Estimate the shear fields.
        """
        e1k = self.fft((deltax1*deltax1 - deltax2*deltax2)*0.5)
        e2k = self.fft(deltax1*deltax2)
        exk = self.fft(deltax1*deltax3)
        eyk = self.fft(deltax2*deltax3)
        ezk = self.fft((2*deltax3*deltax3 - deltax1*deltax1 - deltax2*deltax2)/6)
        del deltax1, deltax2, deltax3
        self.changezero(self.k_ind, 1, mode = 'point')
        k1 = (self.mpi_fn[self.rank][:, None, None]**2 - self.fn[None, :, None]**2 + np.zeros(self.NMesh)[None, None, :])/(2*self.k_ind**2)
        k2 = (2*self.mpi_fn[self.rank][:, None, None]*self.fn[None, :, None]*np.ones(self.NMesh)[None, None, :])/(2*self.k_ind**2)
        kx = (2*self.mpi_fn[self.rank][:, None, None]*self.fn[None, None, :]*np.ones(self.NMesh)[None, :, None])/(2*self.k_ind**2)
        ky = (2*self.fn[None, :, None]*self.fn[None, None, :]*np.ones(int(self.NMesh/self.size))[:, None, None])/(2*self.k_ind**2)
        kz = (2*self.fn[None, None, :]**2 - self.mpi_fn[self.rank][:, None, None]**2 - self.fn[None, :, None]**2)/(2*self.k_ind**2)
        self.changezero(self.k_ind, 0, mode = 'point')

        """
        Estimate the trace of cosmic tides
        """
        e0k = k1*e1k + k2*e2k + kx*exk + ky*eyk + kz*ezk
        self.delta_re = self.ifft(e0k)

    def Rec2(self, sigma):
        """
        First estimate the filtered field
        """
        deltak = self.fft(self.delta)
        deltak *= self._GaussianWindow(sigma)*1j*self.Kf
        deltak1 = ((self.mpi_fn[self.rank][:, None, None]
                  + np.zeros(self.NMesh)[None, :, None]
                  + np.zeros(self.NMesh)[None, None, :])* deltak)
        deltak2 = ((np.zeros(int(self.NMesh/self.size))[:, None, None]
                  + self.fn[None, :, None] 
                  + np.zeros(self.NMesh)[None, None, :]) * deltak)
        del deltak
        deltax1 = self.ifft(deltak1).real
        deltax2 = self.ifft(deltak2).real
        del deltak1, deltak2

        """
        Estimate the shear fields.
        """
        e1k = self.fft((deltax1*deltax1 - deltax2*deltax2)*0.5)
        e2k = self.fft(deltax1*deltax2)
        del deltax1, deltax2
        self.changezero(self.k_perp, 1, mode = 'line')
        k1 = (self.mpi_fn[self.rank][:, None, None]**2 - self.fn[None, :, None]**2 + np.zeros(self.NMesh)[None, None, :])*self.k_ind**2/self.k_perp**4
        k2 = (2*self.mpi_fn[self.rank][:, None, None]*self.fn[None, :, None]*np.ones(self.NMesh)[None, None, :])*self.k_ind**2/self.k_perp**4
        self.changezero(k1, 0, mode = 'line')
        self.changezero(k2, 0, mode = 'line')

        """
        Estimate the trace of cosmic tides
        """
        e0k = k1*e1k + k2*e2k
        self.delta_re = self.ifft(e0k)