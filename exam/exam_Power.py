import sys 
sys.path.append("..")
import numpy as np
from TideRec import Rec
from TideRec import Power
from scipy.fft import fftn, ifftn
import matplotlib.pyplot as plt

BoxSize = 250.0
NMesh = 256

MyRec = Rec(BoxSize = BoxSize, NMesh = NMesh)
MyRec.Read(mode = 'binary', path = './exam_data/Ng256_Density.bin')
MyRec.AutoRec(mode ='5term', sigma = 1)

MyPower = Power(Rec = MyRec, path = './exam_data/Ng256_Density.bin')
n, k, pk = MyPower.Compute(mode = 'DM')
if MyPower.rank == 0:
    plt.loglog(k, pk)
    plt.savefig('./exam_Power.png')