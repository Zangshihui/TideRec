import numpy as np

class MPI_IO(object):
    """
    Class for input/output using mpi4py.

    Parameters
    ----------
    comm:
        the global MPI communicator
    size：
        number of mpi threads
    rank:
        thread number
    offset:
        start point of saving/reading file
    """

    def __init__(self, comm, MPI):
        self.comm = comm
        self.MPI = MPI
        self.size = comm.Get_size()

    def MPI_READ(self, path=''):
        rmode = self.MPI.MODE_RDONLY
        fp = self.MPI.File.Open(self.comm, path, rmode)
        offset = self.comm.Get_rank() * self.datar.nbytes
        fp.Read_at_all(offset, self.datar)
        fp.Close()

    def MPI_WRITE(self, path=''):
        amode = self.MPI.MODE_WRONLY | self.MPI.MODE_CREATE
        fp = self.MPI.File.Open(self.comm, path, amode)
        offset = self.comm.Get_rank() * self.dataw.nbytes
        fp.Write_at_all(offset, self.dataw)
        fp.Close()

def fromfile(path, comm, MPI, shape=[], dtype = np.float32):
    """
    Method to read a binary file using mpi4py.

    Paramters
    ---------
    l:
        the length of the array going to read
    datar:
        data in of the thread to read
    path:
        the path of the file
    dtype:
        the desired data type of the binary file
    shape:
        expected shape of the array before splited
    """

    mpi_io = MPI_IO(comm = comm, MPI = MPI)
    l = np.array(shape).prod()
    assert shape[0]%mpi_io.size==0, \
            "Inappropriate mpi size. processes number: %d, shape: %s"%(mpi_io.size, shape)
    mpi_io.datar = np.empty([l//mpi_io.size], dtype = dtype)
    mpi_io.MPI_READ(path = path)
    return mpi_io.datar.copy()

def tofile(data, path, comm, MPI):
    """
    Method to save an array to a binary file using mpi4py.

    Parameters
    ----------
    dataw:
        data in of the thread to be written
    path:
        the path of the file
    """
    mpi_io = MPI_IO(comm = comm, MPI = MPI)
    mpi_io.dataw = data.copy(order = 'C')
    return mpi_io.MPI_WRITE(path = path)
    
if __name__ == '__main__':
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    data = np.arange(12, dtype = np.float32)
    data = np.array_split(data, size)[rank]
    tofile(data, '../test/test.bin', comm, MPI)
    if rank == 0:
        s = np.fromfile('../test/test.bin', dtype=np.float32, count=12)
        print(s)
    datar = fromfile('../test/test.bin', comm, MPI, shape=[12], dtype=np.float32)
    print(rank, datar)