import sys 
sys.path.append("..")
import numpy as np
from TideRec import Rec
from TideRec import CrossCor
from scipy.fft import fftn, ifftn
import matplotlib.pyplot as plt

BoxSize = 125.0
NMesh = 128

MyRec = Rec(BoxSize = BoxSize, NMesh = NMesh)
MyRec.Read(mode = 'binary', path = './exam_data/Ng128_Density.bin')
MyRec.AutoRec(mode ='5term', sigma = 1)

MyCor = CrossCor(Rec = MyRec, path = './exam_data/Ng128_Density.bin')
MyCor.setbin(style = 'linear')
n, k, rk = MyCor.Compute()
if MyCor.rank == 0:
    plt.semilogx(k, rk)
    plt.savefig('./exam_CrossCor.png')