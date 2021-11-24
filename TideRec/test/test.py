import sys 
sys.path.append("..")
import numpy as np
from core.Rec import Rec
from scipy.fft import fftn, ifftn

data = np.fromfile('../exam/exam_data/Ng128_Density.bin', dtype = np.float32).reshape([128, 128, 128]) - 1
deltak = fftn(data)/128**3
pk = deltak*np.conjugate(deltak).real*500**3
print(pk.real[:, 0, 0])

