import numpy as np
from TideRec.core.utils import Utils


class RS(Utils):
    """
    This class contains methods to load density field from various kinds of files
    Available reading modes:
    1) array:
        
    2) binary:
        Read from a binary file.
    3)...

    Available saving modes:
    1) binary:
        Save to a binary file with data type np.float32

    TO DO: expand to catalog, bigfile...

    Parameters:
    -----------

    TO DO: Deconvolution
    """
    def __init__(self, BoxSize = 300, NMesh = 128, **kwargs):
        super(RS, self).__init__(BoxSize=BoxSize, NMesh=NMesh, **kwargs)

    def Read(self, mode = 'array', data = None, path = None):
        """
        Call up reading functions to read density field
        """
        self.rank_print('=' * 80)
        self.rank_print('Reading mode: %s'%mode)
        self.rank_print('Reading density field ...')

        if mode == 'array':
            self.ReadArray(data)
        elif mode == 'binary':
            self.ReadBinary(path)
        else:
            raise ValueError('This reading mode does not exists!')

        self.rank_print('Reading completed.')
        self.rank_print('=' * 80)

    def ReadArray(self, data):
        """
        Read density field from a numpy array
        """
        pass

    def ReadBinary(self, path):
        """
        Read density field from binary file.
        Note that data tupe of binary field should be np.float32.
        """
        df = self.fromfile(path=path, shape=[self.NMesh, self.NMesh, self.NMesh], dtype=np.float32)
        self.delta = df.reshape([int(self.NMesh/self.size), self.NMesh, self.NMesh]) - 1

    def Save(self, mode = 'binary', data = None, path = None):
        """
        Call up save functions

        Parameters
        ----------
        data: 
            numpy array with shape [NMesh/size, NMesh, NMesh]
        path:
            saving path
        """
        self.rank_print('=' * 80)
        self.rank_print('Saving mode: %s'%mode)
        self.rank_print('Saving data ...')

        if type(data) is not np.ndarray:
            raise ValueError('Saving data is not a numpy array!')
        if np.array(data.shape).prod() != self.shape:
            raise ValueError('Data shape is not correct!')
        if path is None:
            raise ValueError('File path is not explicit!')

        if mode == 'binary':
            self.SaveBinary(data, path)
        else:
            raise ValueError('Saving mode is not available!')
        
        self.rank_print('Saving completed.')
        self.rank_print('=' * 80)

    def SaveBinary(self, data, path):
        """
        Save density field to a binary file.
        """
        data_all = None
        if self.rank == 0:
            data_all = np.empty([self.NMesh, self.NMesh, self.NMesh], dtype = self.format)
        self.comm.Gather(data.astype(self.format), data_all, root = 0)
        if self.rank == 0:
            data_all.real.astype(np.float32).tofile(path)


if __name__ == '__main__':
    Read = Read()