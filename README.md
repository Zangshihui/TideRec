# TideRec
TideRec is a Python package for performing tidal reconstruction developed by [Shihui Zang](zangshastro.com). This package can perform both 5-shear-term and 2-shear-term tidal reconstruction according to [Zhu et al. 2021](https://arxiv.org/abs/2108.01575). Here we provide some functions to analyze the result of tidal reconstruction. 

__Note that some functions are still under development.__ If you find any bug or have any suggestion, please do not hesitate to email me. Your contributions would be greatly appreciated! Next we will use fftw to accelerate the calculation and develop more analyze functions such as analysis with regard to wedges $\mu$, along with 2-D slice preview function.

## Install
    git clone https://github.com/Zangshihui/TideRec
    cd TideRec
    pip install -e .

## Links

* Source code: [https://github.com/Zangshihui/TideRec](https://github.com/Zangshihui/TideRec)

## mpi available
This package is compatible with mpi4py. You may run the program like

    mpiexec -n 8 python XXX.py

__Note that the number of processes must be the divisor of NMesh.__ We recommend you to choose NMesh as power of 2 and number of process as 2,4,8 or 16.

## License
TideRec is distributed under the Apache License, Version 2.0.
