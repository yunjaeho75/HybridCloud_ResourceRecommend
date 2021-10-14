import os as _os
import numpy as np

def exists(path):
    return _os.path.isdir(_os.path.abspath(_os.path.dirname(path)))

def exists_exception(log, path):
    if exists(path) is False:
        log.error(f'- Not exists directory: {_os.path.dirname(path)}')
        return False
    return True

def special_k(L, T):
    dim = T.shape[0]
    k = np.zeros(dim)
    for z in range(int(dim)):
        k[z] = np.max(np.round(L / T[z]))
    #print('k :', k)
    return max(k)

# euclidean distance function
def euclidean_distance(inst1, inst2):    
    return np.linalg.norm(inst1 - inst2)
    #return np.sqrt(np.sum(np.square(inst1 - inst2)))

def sigmoid(x):
    s=1/(1+np.exp(-x))
    ds=s*(1-s)  
    return s,ds

def relu(x) : 
    return np.maximum(0, x)