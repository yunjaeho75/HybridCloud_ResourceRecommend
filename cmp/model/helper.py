import os as _os
import sys
from . import spamfilter
from . import psoazure
from .. import core
from ..core import logger, util
import math
import csv

def get(ws):
    if ws.base_model == "ml-bilstm-v1":
        param = core.Parameter.from_kwargs(in_feature=1, out_feature=['cpu.avg'], in_step=60, out_step=60)
        model = spamfilter.model_v1()
        model.create(param)
        return model

    if ws.base_model == "ml-bilstm-v2":
        param = core.Parameter.from_kwargs(in_feature=1, out_feature=['cpu.avg'], in_step=60, out_step=60)
        model = spamfilter.model_v2()
        model.create(param)
        return model
    
    if ws.optimizer == "pso":
        #param = core.Parameter.from_kwargs(particles=300, iters=500, options = {'c1': .9, 'c2': .1, 'w':1.})
        param = core.Parameter.from_kwargs(particles=7000, iters=150, options = {'c1': .9, 'c2': .1, 'w':1.})
        #param = core.Parameter.from_kwargs(particles=100, iters=100, options = {'c1': .5, 'c2': .3, 'w':.9})
        optimizer = psoazure.optimizer()
        optimizer.create(param)
        return optimizer

    return None


def load(ws):
    path = ws.load_path()
    
    if ws.data_helper == "azure-vm":
        log = logger.get(__name__)
        
        model = get(ws)
        if model is None:            
            log.error(f'Not found optimizer.')
            sys.exit()

        ret = model.load(path)
        if ret is None:
            return None
            
        return model

    if ws.optimizer != "pso":
        # return default tf model
        model = spamfilter.helper()
        model.load(path)
        return model

    return None


def save(ws, model):
    log = logger.get(__name__)
    path = ws.save_path()
    log.info(f'save model (path: {path})')
    if ws.base_model == "spamfilter-v1" or ws.base_model == "spamfilter-v2":
        # if ws.exists(path) is False:
        #     log.info(f'- Not exists directory: {_os.path.dirname(path)}')
        #     return
        if util.exists(path):
            model.save(path)
            writeMeta(path, ws)
            log.info(f'- save completed.')
        else:
            log.info(f'- Not exists directory: {_os.path.dirname(path)}')
            log.info(f'- save failed.')

def writeMeta(path, ws):
    f = open(f'{path}/meta.csv','w', newline='')
    wr = csv.writer(f)
    wr.writerow(["property", "value"])
    wr.writerow(["mean", ws.mean])
    wr.writerow(["std", ws.std])
    f.close()