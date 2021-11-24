# TideRec
TideRec is a Python package for performing tidal reconstruction developed by [Shihui Zang](zangshastro.com). This package can perform both 5-shear-term and 2-shear-term tidal reconstruction according to [Zhu et al. 2021](https://arxiv.org/abs/2108.01575). Here we provide some functions to analyze the result of tidal reconstruction. 

__Note that some functions are still under development.__ If you find any bug or have any suggestion, please do not hesitate to email me. Your contributions would be greatly appreciated! Next we will use fftw to accelerate the calculation and develop more analyze functions such as analysis with regard to wedges $\mu$, along with 2-D slice preview function.

## Install
    git clone https://github.com/Zangshihui/TideRec
    cd TideRec
    pip install -e .

## Quick Start
### Initial the Rec class
Frist you should import the related class Rec into the program

    import numpy as np
    from TideRec import Rec

Then initial this class using two parameters NMesh and BoxSize.

    NMesh = 256
    BoxSize = 250.0
    MyRec = Rec(BoxSize = BoxSize, NMesh = NMesh)

We need to provide the inital density field before reconstruction by a binary file. (More reading procedures are under development.)

    MyRec.Read(mode = 'binary', path = './exam_data/Ng256_Density.bin')

### Perform tidal reconstruction
Reconstruction method is required. 5-shear-term tidal reconstruction '5term' and 2-shear term tidal reconstruction '2-term' are available. 'sigma' is the filter size before reconstruction, you can set is to the grid size approximately.

    MyRec.AutoRec(mode ='5term', sigma = 1)

### Save the reconstructed field
If mpi4py is not used in the program, you can just Get the density field and save it.

    data = Density.Get('density')

However, if mpiexec is used to run the program, we provide a function to save the data, otherwise only part of the data would be saved.

    MyRec.Save(data = MyRec.Get('density'), path = './data.bin')

__See the example file to see more functions of this package.__

## Links

* Source code: [https://github.com/Zangshihui/TideRec](https://github.com/Zangshihui/TideRec)

## mpi available
This package is compatible with mpi4py. You may run the program like

    mpiexec -n 8 python XXX.py

__Note that the number of processes must be the divisor of NMesh.__ We recommend you to choose NMesh as power of 2 and number of process as 2,4,8 or 16.

## License
TideRec is distributed under the Apache License, Version 2.0.
