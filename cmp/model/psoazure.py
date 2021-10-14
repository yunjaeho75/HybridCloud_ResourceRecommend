import numpy as np
from . import metahelper
from ..data import psoazure as data_helper
from ..core import logger
import sys

# Import PySwarms
import pyswarms as ps
import pyswarms.utils.search as pus
from pyswarms.utils.functions import single_obj as fx
from numpy import inf
import math

class helper(metahelper.AbstractHelper):
    data = None
    
    def names(self) -> str:
        pass

    def summary(self):
        pass
    
    def create(self, parameter):
        pass

    def summary(self):
        if self.data is not None:
            return self.data.describe()
            #return self.data.head()
        return None
        
    def summary_str(self):
        return self.summary()

    def get_model(self):
        pass

    # def load(self, ws):
    #     print(f'---> {ws.load_path()}')
    #     rsc_filter = data_helper.base_helper().rsc_filter()
    #     cst_filter = data_helper.base_helper().cst_filter()
    #     self.data = data_helper.base_helper().load(ws.load_path())
    #     self.gT = self.data[rsc_filter].to_numpy()
    #     self.gM = self.data[cst_filter].to_numpy().reshape(self.data[cst_filter].to_numpy().shape[0], 1)        
    #     self.dimensions = self.gT.shape[0]
    #     self.weak =  data_helper.base_helper().weak(self.data, rsc_filter)
    #     return self.data
    def load(self, path):
        rsc_filter = data_helper.base_helper().rsc_filter()
        cst_filter = data_helper.base_helper().cst_filter()
        self.data = data_helper.base_helper().load(path)
        if self.data is None:
            return None
        self.gT = self.data[rsc_filter].to_numpy()
        self.gM = self.data[cst_filter].to_numpy().reshape(self.data[cst_filter].to_numpy().shape[0], 1)        
        self.dimensions = self.gT.shape[0]
        self.weak =  data_helper.base_helper().weak(self.data, rsc_filter)
        #self.data = self.data.sort_index()
        return self.data
        
    # def load(self, ws):
    #     self.data = data_helper.base_helper().load(ws.load_path())        
    #     df = self.data.to_numpy()
    #     self.gT = df[::, :-1]
    #     self.gM = df[::, -1].reshape(df.shape[0], 1)        
    #     self.dimensions = self.gT.shape[0]
    #     return self.data

    def save(self, path):
        pass

    def evaluate(self, data):
        pass

    def predict(self, data):
        pass
        
class optimizer(helper):

    def create(self, parameter):
        self.particles = parameter.particles
        self.options = parameter.options
        self.iters = parameter.iters

    def compile(self, window):
        self.gL = window.gL.flatten()
        #self.gK = special_k(self.gL, self.gT)        
        self.gK = self.special_k()
        #self.gK = 20
        #self.constraints = (np.zeros(self.dimensions, dtype=np.float), np.full(self.dimensions, self.gK, np.float))
        #self.constraints = (np.full(self.dimensions, 40, np.float), np.full(self.dimensions, 0, dtype=np.float))
        self.constraints = (np.full(self.dimensions, 0, dtype=np.int), np.full(self.dimensions, 1, np.int))
        #self.optimizer = ps.single.GlobalBestPSO(n_particles=self.particles, dimensions=self.dimensions, options=self.options, bounds=self.constraints)
        #self.optimizer = ps.single.GlobalBestPSO(n_particles=self.particles, dimensions=self.dimensions, options=self.options, bounds=self.constraints, bh_strategy="nearest")
        self.optimizer = ps.single.GlobalBestPSO(
            n_particles=self.particles,
            #n_particles=self.dimensions * 20,
            #n_particles=self.particles * int(self.gK),
            #n_particles=max(self.particles, int(self.gK)),
            dimensions=self.dimensions, 
            options=self.options, 
            bounds=self.constraints, 
            bh_strategy="nearest"#, intermediate, nearest
            #vh_strategy="invert"
        )

        #self.optimizer = ps.single.GlobalBestPSO(n_particles=self.particles, dimensions=self.dimensions, options=self.options, bounds=self.constraints, vh_strategy="invert")
        #self.optimizer = ps.single.LocalBestPSO(n_particles=self.particles*1, dimensions=self.dimensions, options=self.options, bounds=self.constraints)
        

    def predict(self):
        self.optimizer.reset()
        cost, pos = self.optimizer.optimize(self.f, iters=self.iters, verbose=True)
        D = np.around(np.dot(pos, self.gK))
        return cost, D

    # objective function
    def f(self, x):
        n_particles = x.shape[0]
        j = [self.cost_optimize(x[i]) for i in range(n_particles)]
        return np.array(j)

    def cost_optimize(self, params):
        #D = params
        #D = np.around(params)
        D = np.around(np.dot(params, self.gK))
        P = np.dot(D, self.gT)
        C = np.dot(D, self.gM)[0]
        #E = euclidean_distance(np.append(P, C), np.append(self.gL, 0))
        E = euclidean_distance(P, self.gL)
        err = 0
        #if np.all(P < self.gL):
        S = np.where(np.array(P) < self.gL)
        if S[0].size > 0:
            err = 9999e+308
            #err = 1e+208
        
        R = np.where(D > 0)
        #print(R[0].size)

        #R = E + C + err
        R = 1. * E + 1. * C + err + 0.7 * R[0].size
        #R = C + err
        #R = math.sqrt(E + C + err)
        #print(f"{R} = {E} + {C} + {err}")
        return R

    def __repr__(self):
        return '\n'.join([
            f'pso optimizer',
            f'    gL: {self.gL}',
            f'    gK: {self.gK}',
            f'    gT: {self.gT.shape}',
            f'{self.gT[0:5, ::]}',
            f'...',
            f'    gT: {self.gM.shape}',
            f'{self.gM[0:5, ::]}',
            f'...',
            f'    particles: {self.particles}',
            f'    dimensions: {self.dimensions}',
            f'    options: {self.options}',
            f'    constraints: {self.constraints}'])
            

    def special_k(self):
        log = logger.get(__name__)
        log.debug(f'> gL: {self.gL}')
        log.debug(f'> weak: {self.weak}')
        log.debug(f'> max: {self.gL / self.weak}')
        log.debug(f'> max: {int(np.max(self.gL / self.weak))}')
        return int(np.max(self.gL / self.weak))

    def product(self, item):
        col_filter = data_helper.base_helper().product_filter()
        df = self.data.loc[item, col_filter]
        product = df.apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
        return product.to_numpy()
        

# def special_k(L, T):
#     dt = T[np.lexsort(np.transpose(T)[::-1])]
#     k = L / dt[0]
#     print('k :', k)
#     return max(k)

# euclidean distance function
# Vector space 
def euclidean_distance(inst1, inst2):    
    return np.linalg.norm(inst1 - inst2)
    #return np.sqrt(np.sum(np.square(inst1 - inst2)))

def sigmoid(x):
    s=1/(1+np.exp(-x))
    ds=s*(1-s)  
    return s,ds

def relu(x) : 
    return np.maximum(0, x)
