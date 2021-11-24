import numpy as np
from TideRec.core.Fun import Fun
from scipy.fft import fftn, ifftn

class fft(Fun):
    """
    A class adding Fast Fourier transfer and inverse Fast Fourier Transfer method.
    credit to Mao Tian-Xiang

    Parameters
    ----------
    Kf:
        Fundamental frequency
    H:
        Grid size
    fn:
        One-dimension wave number array
        for e.g. -511, -510, ..., -1, 0, 1, 2, ..., 512
    mpi_fn:
        One-dimension wave number splited by mpi4py
    shape:
        number of gird number in per mpi thread
    k_ind:
        norm of 3-D wave number indice splited by mpi4py
    
    """

    def __init__(self, *args, **kwargs):
        super(fft, self).__init__(*args, **kwargs)
        try:
            self.commsd
        except AttributeError:
            from mpi4py import MPI
            self.MPI = MPI
            self.comm = MPI.COMM_WORLD
            self.rank = self.comm.rank
            self.size = self.comm.size
            self.format = np.complex64

            self.Kf = 2 * np.pi / self.BoxSize
            self.H = float(self.BoxSize)/self.NMesh
            self.fn = np.fft.fftfreq(self.NMesh, 1. / self.NMesh).astype(self.format)
            self.mpi_fn = np.array_split(self.fn, self.size)
            self.shape = int(self.NMesh * self.NMesh * self.NMesh / self.size)
            self.k_ind = (self.mpi_fn[self.rank][:, None, None]**2.
                  + self.fn[None, :, None]**2.
                  + self.fn[None, None, :]**2)**(0.5)
            self.k_perp = (self.mpi_fn[self.rank][:, None, None]**2.
                  + self.fn[None, :, None]**2.
                  + np.zeros(self.NMesh)[None, None, :])**(0.5)

    def fft(self, data):
        """
        Method to operate forward fft
        data: 3-D numpy array, with shape [NMesh/size, Nmesh, NMesh]
        data will be first transfered to np.complex64

        TO DO: change this method using fftw
        """
        data_all = None
        datak_all = None
        if self.rank == 0:
            data_all = np.empty([self.NMesh, self.NMesh, self.NMesh], dtype = self.format)
        self.comm.Gather(data.astype(self.format), data_all, root = 0)
        if self.rank == 0:
            datak_all = fftn(data_all)
        datak = np.empty([int(self.NMesh/self.size), self.NMesh, self.NMesh], dtype = self.format)
        self.comm.Scatter(datak_all, datak)
        return datak/(self.NMesh**3)

    def ifft(self, datak):
        """
        Method to operate back forward fft
        datak: 3-D numpy array, with shape [NMesh/size, Nmesh, NMesh]
        data will be first transfered to np.complex64

        TO DO: change this method using fftw
        """
        data_all = None
        datak_all = None
        if self.rank == 0:
            datak_all = np.empty([self.NMesh, self.NMesh, self.NMesh], dtype = self.format)
        self.comm.Gather(datak.astype(self.format), datak_all, root = 0)
        if self.rank == 0:
            data_all = ifftn(datak_all)
        data = np.empty([int(self.NMesh/self.size), self.NMesh, self.NMesh], dtype = self.format)
        self.comm.Scatter(data_all, data)
        return data*(self.NMesh**3)

if __name__ == '__main__':
    s = fft(BoxSize = 1, NMesh = 8)
    data = np.arange(8**3).reshape([8, 8, 8])
    s.fft(data)
    pass