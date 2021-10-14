import datetime
import pandas as pd
import numpy as np
from . import metahelper
from .. import core

class CpuFilter():
    def __init__(self, num=None):
        self.num = num

    @property
    def column(self):
        return "CPU.Type"

    @property
    def value(self):
        return self.num

class helper(metahelper.AbstractHelper):
    def names(self):
        return ["CPU.Core", "RAM (GB)", "Storage (GB)"]
        
    def window_parameter(self):
        pass
        
    def window_parameter(self, ws, data):
        cpufilter = self.filter(self.cputype(data))
        return core.Parameter.from_kwargs(gL=np.array(data, dtype=np.float64), cpufilter=cpufilter)

    def create(self, data):
        size = len(self.names())
        return pd.DataFrame(np.array(data).reshape(-1, size), columns=self.names(), index=[0])
        pd.DataFrame(data, columns=self.names())

    def load_data(self, ws):
        # read scv data
        try:
            self.df = pd.read_csv(ws.input, names=self.names(), header=None)
            return self.df
        except FileNotFoundError as err:
            return None
        except AttributeError as err:
            return None   



    def cputype(self, df):
        return np.array(df).flatten()[0]

    def filter(self, cputype):
        return CpuFilter(cputype)

    @property
    def gL():
        pass

    @property
    def gK():
        pass

    @property
    def data():
        pass


class base_helper(metahelper.AbstractHelper):
    def names(self):
        return ["CPU.Core", "RAM (GB)", "Storage (GB)", "Cost (US)"]

    def index(self):
        return ["No"]

    def window_parameter(self):
        pass
    
    def load_data(self, ws):
        self.df = self.load(ws.input)
        return self.df

    def load(self, path):
                # read scv data
        # read scv data
        try:
            self.df = pd.read_csv(path, index_col=0)
            return self.df
        except FileNotFoundError as err:
            return None
        except AttributeError as err:
            return None   
        
    def weak(self, df, names):
        df.sort_values(by=names, inplace=True)
        df = df[(df.T != 0).any()]
        return df[names].loc[1].to_numpy()

    @property
    def data(self):
        pass

    @property
    def gT(self):
        pass

    @property
    def gM(self):
        pass

    @property
    def dimensions(self):
        pass

    def rsc_filter(self):        
        return ["CPU.Core", "RAM (GB)", "Storage (GB)"]

    def cst_filter(self):
        return ["Cost (US)"]

    def product_filter(self):
        return ['Instance.Series', 'Series.Type']