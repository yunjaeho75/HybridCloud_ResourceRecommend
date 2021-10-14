import json
import sys
import numpy as np
from ..model import helper as model_helper
from ..data import helper as data_helper
from ..core import logger, util

#load_model    
def load_model(ws):
    model = model_helper.load(ws)
    if model is None:
        log = logger.get(__name__)
        log.error(f'Not found model.')
        sys.exit()
    return model


# get model
def get_model(ws):
    model = model_helper.get(ws)
    model.load(ws.load_path())
    return model
    

# predict model
def predict(model, window):
    return model.predict(window)


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def jsondump(data):
    return json.dumps(data, indent=4, cls=NumpyEncoder)

# export predict result of model
def export(ws, data):
    log = logger.get(__name__)

    path = ws.export_path()
    log.info(f'export to file: {path}')
    if util.exists_exception(log, path):
        with open(path, 'w') as f:
            json.dump(data, f, indent='\t', cls=NumpyEncoder)

def window_parameter(ws, data):
    return data_helper.get(ws).window_parameter(ws, data)

# comple model
def compile(model, window):
    model.compile(window)

# predict model
def predict(model):
    return model.predict()    

# optimize
def optimize(ws, model, data):
    log = logger.get(__name__)
    log.debug(f"dataset:\n{data.head()}")
    log.debug(f'model summary:\n{model.summary_str()}')

    log.info('start estimator porcess.')    
    # create parameter
    param = window_parameter(ws, data)
    log.info(f'crate parameter: {param}')

    # comple model
    compile(model, param)

    # predict model
    log.info('start pso cost optimizor porcess.')
    cost, pos = predict(model)
    log.info('finish pso cost optimizor porcess.')

    # report
    recommand = report(model, cost, pos)
    log.info(f'recommand: {recommand}')

    return recommand

# report
def report(model, cost, pos):
    n_repeat = 73
    #apos = pos
    #apos = np.around(pos)
    #apos = np.around(np.dot(pos, 20))
    #apos = np.trunc(pos)
    #apos = np.fix(pos)
    apos = pos
    cloud_request = model.gL
    cloud_present = np.dot(apos, model.gT)
    cloud_cost = np.dot(apos, model.gM)
    cloud_index = np.where(apos >= 1.0)[0]
    cloud_product = cloud_index + np.array([1])
    cloud_detail = apos[cloud_index]
    
    logger.reset()
    log = logger.get(__name__)
    # Report optimize cost
    log.info("="*n_repeat)
    log.info(f"*** Report optimize cost ***")
    log.info("-"*n_repeat)
    log.info(f"> Request: {cloud_request}")
    log.info("-"*n_repeat)
    log.info(f"> product present: {cloud_present}")
    log.info(f"> product cost: {cloud_cost}")
    log.info(f"> product index: {cloud_product}")
    log.info(f"> product detail: {cloud_detail}")    
    log.debug("-"*n_repeat)
    log.debug(f"> Debug")
    log.debug(f"> Cost: {cost}")
    log.debug(f"> Configuration:\n{apos}")    
    log.info("="*n_repeat)

    result = dict()
    result['request'] = cloud_request.flatten()
    result['present'] = cloud_present.flatten()
    result['present-cost'] = cloud_cost.flatten()
    result['product'] = model.product(cloud_product.flatten())
    result['product-no'] = cloud_product.flatten()
    result['product-size'] = cloud_detail.flatten()

    return result

