import datetime
import pandas as pd
import numpy as np
from . import metahelper
from .. import core

class helper(metahelper.AbstractHelper):

    def names(self):
        return ["Datetime", "System", "Resource", "Max.", "Avg.", "Path"]

    def window_parameter(self):        
        return core.Parameter.from_kwargs(in_feature=['cpu.avg'], out_feature=['cpu.avg'], in_step=60, out_step=60)
    
    def load_data(self, ws):
        try:            
            # read scv data
            df = pd.read_csv(ws.input, names=self.names(), header=None)

            # convert datastampe to unix times
            date_time = make_datetime(df, 'Datetime', '%Y%m%d%H%M')
            timestamp_s = make_timestamp_s(date_time)

            # rebuild data format
            data = {'cpu.max': make_resource(df, 1, 'Max.'),
                'cpu.avg': make_resource(df, 1, 'Avg.'),
                'memory.max': make_resource(df, 2, 'Max.'),
                'memory.avg': make_resource(df, 2, 'Avg.'),
                'disk.max': make_resource(df, 3, 'Max.'),
                'disk.avg': make_resource(df, 3, 'Avg.')}
            data.update(make_time2signal(timestamp_s, "day"))
            data.update(make_time2signal(timestamp_s, "week"))
            data.update(make_time2signal(timestamp_s, "month"))
            data.update(make_time2signal(timestamp_s, "year"))
            # return pd.DataFrame(data)
            
            data.update({'date': date_time})
            _df = pd.DataFrame(data)
            mask = (_df['date'] > '2020-12-04 00:00') & (_df['date'] < '2020-12-05 00:00')
            _df = _df.loc[mask]
            return _df.drop(['date'], axis=1)
        except FileNotFoundError as err:
            return None
        except AttributeError as err:
            return None

class base_helper(metahelper.AbstractHelper):

    def names(self):
        return ["target"]
        #return ["Datetime", "System", "Resource", "Max.", "Avg.", "Path"]

    def window_parameter(self):        
        return core.Parameter.from_kwargs(in_feature=['target'], out_feature=['target'], in_step=60, out_step=60)
    
    def load_data(self, ws):
        # read scv data
        try:
            df = pd.read_csv(ws.input, names=self.names(), header=None)
            return pd.DataFrame(df)
        except FileNotFoundError as err:
            return None
        except AttributeError as err:
            return None        
        
    def create(self, data):
        df = dict()
        df[self.names()[0]] = data
        return pd.DataFrame(df)


# #### 데이터 변환 함수
def make_resource(df, resource, target):
    indices = df["Resource"] == resource
    return np.array(df.loc[indices,target])

def make_datetime(df, target, format):
    item = make_resource(df, 1, target)
    return pd.to_datetime(item, format=format)

def make_timestamp_s(df):
    return df.map(datetime.datetime.timestamp)

# df : 초단위 타입스탬프 입력 (make_timestamp_s, make_datetime 활용)
# unit : 'day', 'week', 'year'
def make_time2signal(df, unit='day'):
    day = 24*60*60    
    week = (7)*day
    month = (30.4369)*day
    year = (365.2425)*day
    time = {'day': day, 'week': week, 'month': month, 'year': year}.get(unit, day)
    signal = {}
    signal[unit+'.sin'] = np.array(np.sin(df * (2 * np.pi / time)))
    signal[unit+'.cos'] = np.array(np.cos(df * (2 * np.pi / time)))
    return signal

