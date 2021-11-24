import numpy as np
from TideRec.core.RS import RS

class Bin(RS):
    """
    This class including algorithms to allocate 3D information into 1D/2D bins

    Available algorithms
    --------------------
    1) UniDimension
    2) BiDimension
    3) BiDimensionBin

    Parameters
    ----------
    
    """

    def __init__(self, *args, **kwargs):
        super(Bin, self).__init__(*args, **kwargs)

        self.setbin(style = 'linear', binnum = int(self.NMesh/2))

    def Binnize(self, data, mode = None, style = 'linear', binnum = None, Nmu = 5):
        """
        Set the basic parameters for binize algorithm.
        kmin is set to the fundamental frequency.
        kmax is set to Nyquist frequency.
        
        Available mode:
        1) 1D
        3) 2Dbin

        Available style:
        1) linear
        2) log

        """
        self.rank_print('=' * 80)
        self.rank_print('Binnize Parameters:')
        self.rank_print('mode: %s' % (mode))
        self.rank_print('Binnize begins ...')

        self.mubin = np.linspace(0, 1, Nmu + 1, endpoint = True)

        if mode == None:
            raise ValueError('Please provide the mode!')
        else:
            raise ValueError('Bin style is not available!')


        if mode == '1D':
            MPI_n, MPI_k, MPI_Ak = self.UniDimension(data)
        elif mode == '2Dbin':
            MPI_n, MPI_k, MPI_Ak = self.BiDimension(data, binnum, Nmu)
        else:
            raise ValueError('Bin mode is not available!')

        MPI_k *= self.Kf

        self.rank_print('Binnize Completed.')
        self.rank_print('=' * 80)

        return MPI_n, MPI_k, MPI_Ak
    
    def setbin(self, style = 'linear', binnum = None):
        """
        Function to set bin style.

        Available style:
            1) linear
            2) log
        """
        self.rank_print('=' * 80)
        self.rank_print('Bin style:')
        self.rank_print('style: %s, binnum: %d' % (style, binnum))
        self.rank_print('=' * 80)

        if binnum == None:
            binnum = int(self.NMesh/2)
        if style == 'linear':
            self.linearbin(binnum)
        elif style == 'log':
            self.logbin(binnum)
        else:
            raise ValueError('Bin style is not available!')

    
    def linearbin(self, binnum):
        self.bin = np.linspace(0.5, self.NMesh/2 - 0.5, binnum, endpoint = True)

    def logbin(self, binnum):
        self.bin = np.logspace(np.log(1), np.log(self.NMesh/2 - 0.5), binnum, endpoint = True, base = np.e)

    def UniDimension(self, data):
        """
        Allocate 3-D information into 1D bins
        """
        n_bin = []
        Ak_bin = []
        k_bin = []
        self.k_ind = (self.mpi_fn[self.rank][:, None, None]**2.
                  + self.fn[None, :, None]**2.
                  + self.fn[None, None, :]**2)**(0.5)
        for i in range(len(self.bin) - 1):
            bool = (self.bin[i] <= self.k_ind) * (self.k_ind < self.bin[i + 1])
            n_bin.append(bool.sum())
            k_bin.append(self.k_ind[bool].real.astype(np.float32).sum())
            Ak_bin.append(data[bool].astype(np.float32).sum())
        n_bin = np.array(n_bin)
        Ak_bin = np.array(Ak_bin)
        k_bin = np.array(k_bin)
        MPI_n = self.comm.reduce(n_bin, root = 0)
        MPI_Ak = self.comm.reduce(Ak_bin, root = 0)
        MPI_k = self.comm.reduce(k_bin, root = 0)
        
        if self.rank == 0 :
            print(MPI_n)
            return MPI_n, MPI_k/MPI_n*self.Kf, MPI_Ak/MPI_n
        else:
            return None, None, None

    def BiDimension(self, data, Nmu):
        """
        Allocate 3-D information into 2D bins
        """
        nbin = np.empty([Nmu, binnum])
        Ak_bin = np.empty([Nmu, binnum])
        k_bin = np.empty([Nmu, binnum])
        self.z_ind = (np.zeros(int(self.NMesh/self.size))[:, None, None]
                  + np.zeros(self.NMesh)[None, :, None]
                  + self.fn[None, None, :]**2.)**(0.5)
        self.changezero(self.k_ind, 1, mode = 'point')
        self.z_ind = self.z_ind/self.k_ind
        self.changezero(self.k_ind, 0, mode = 'point')

        for i in range(len(self.bin) - 1):
            for j in range(Nmu):
                bool = (self.bin[i] <= self.k_ind) * (self.k_ind < self.bin[i + 1]) * (self.mubin[j] <= self.z_ind) * (self.z_ind < self.mubin[j + 1])
                n_bin[j, i] = bool.sum()
                k_bin[j, i] = self.k_ind[bool].real.astype(np.float32).sum()
                Ak_bin[j, i] = data[bool].astype(np.float32).sum()

        MPI_n = self.comm.reduce(n_bin, root = 0)
        MPI_Ak = self.comm.reduce(Ak_bin, root = 0)
        MPI_k = self.comm.reduce(k_bin, root = 0)
        
        return MPI_n, MPI_k, MPI_Ak

    

if __name__ == '__main__':
    s = Bin()