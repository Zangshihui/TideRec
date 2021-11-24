import sys 
sys.path.append("..")
import numpy as np
from core.Rec import Rec
from scipy.fft import fftn, ifftn

BoxSize = 250.0
NMesh = 256

MyRec = Rec(BoxSize = BoxSize, NMesh = NMesh)
MyRec.Read(mode = 'binary', path = './exam_data/Ng256_Density.bin')
MyRec.AutoRec(mode ='5term', sigma = 15)
MyRec.Save(mode = 'binary', path = './exam_data/Re_Density_MY.bin', data = MyRec.Get('delta_re'))
