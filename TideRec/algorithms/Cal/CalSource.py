import numpy as np
from TideRec.algorithms.Cal.Bin import Bin

class CalSource(Bin):
    """
    This class provides the interface with Rec class.

    TO DO: Read from Rec class
    ----------
    
    """

    def __init__(self, Rec = None, path = None, *args, **kwargs):
        super(CalSource, self).__init__(Rec = None, *args, **kwargs)
        if Rec == None:
            raise ValueError('Please input Rec class!')
        try:
            self.NMesh = Rec.Get(dataname = 'NMesh')
            self.BoxSize = Rec.Get(dataname = 'BoxSize')
            self.delta_re = Rec.Get(dataname = 'delta_re')
            self.Kf = 2*np.pi/self.BoxSize
        except:
            raise ValueError('Information of Rec class is not completed!')

        self.fn = np.fft.fftfreq(self.NMesh, 1. / self.NMesh).astype(self.format)
        self.mpi_fn = np.array_split(self.fn, self.size)
        self.k_ind = (self.mpi_fn[self.rank][:, None, None]**2.
                  + self.fn[None, :, None]**2.
                  + self.fn[None, None, :]**2)**(0.5)

        self.rank_print('=' * 80)
        self.rank_print('Analyze box parameters:')
        self.rank_print('BoxSize: %f, NMesh: %d' % (self.BoxSize, self.NMesh))
        self.rank_print('=' * 80)

        if path == None:
            pass
        else:
            self.rank_print('=' * 80)
            self.rank_print('Reading dark matter density ...')
            self.rank_print('=' * 80)
            df = self.fromfile(path=path, shape=[self.NMesh, self.NMesh, self.NMesh], dtype=np.float32)
            self.delta = df.reshape([int(self.NMesh/self.size), self.NMesh, self.NMesh]) - 1

if __name__ == '__main__':
    s = CalSource()