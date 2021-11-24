from mpi4py import MPI
import numpy as np
import os
from TideRec.core.Base import Base
from TideRec.MPI_IO.MPI_IO import fromfile as _fromfile
from TideRec.MPI_IO.MPI_IO import tofile as _tofile

class Fun(Base):

    def __init__(self, BoxSize=300., NMesh=128, **kwargs):
        """
        This class includes basic operations.

        Parameters
        ----------
        BoxSize:
            Length of side of density field Box
        NMesh:
            Grid numbers of the density field
        """
        super(Fun, self).__init__(BoxSize=300., NMesh=128, **kwargs)
        self.MPI = MPI
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.rank
        self.size = self.comm.size

        self.NMesh = NMesh
        self.BoxSize = BoxSize
    
    def mybarrier(self):
        """
        Barrir tool
        """
        return self.comm.barrier()

    def rank_print(self, str=''):
        """
        Print tool in mpi4py
        """
        if self.rank == 0:
            print(str)
        
    def changezero(self, data, value, mode = 'point'):
        """
        Change the value of the data with zero indice to avoid zeros division.
        """
        if mode == 'point':
            if self.rank == 0:
                data[0,0,0] = value
        elif mode == 'line':
            data[0, 0, :] = value

    def fromfile(self, path, shape=[], dtype=np.float32):
        """
        Tool to read a binary file

        Parameters
        ----------
        path:
            the path of the binary file
        shape: 
            the shape of the array before spliting
        dtype:
            the type of data of file to read
        """
        return _fromfile(path, self.comm, self.MPI, shape=shape, dtype=dtype)

    def tofile(self, data, path):
        """
        Tool to save a binary file
        """
        return _tofile(data, path, self.comm, self.MPI)

if __name__ == '__main__':
    s = Fun()
    pass