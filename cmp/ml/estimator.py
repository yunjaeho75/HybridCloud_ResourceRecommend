import os
import sys
from .. import core
from ..core import workspace, dataset, options, logger
from . import engine as ml

def main(args):
    
    print('$>', args)
    
    # get config
    ws = workspace.from_config(args)
    print('\n$> config:\n', ws)

    # initialize logger 
    logger.init(ws)
    log = logger.get(__name__)
    log.info(f'start estimator porcess.')

    # set service name
    ws.set_service(options.service.estimator)
    
    # get dataset
    data = dataset.get(ws)
    log.debug(f"dataset:\n{data.describe()}")

    # create time window
    window = ml.window_generator(ws, data)
    log.info(f'input shape: {window.example[0].shape}')

    # load model
    model = ml.load_model(ws)    
    log.info(f'load model: {ws.load_path()}')
    log.debug(f'model summary:\n{model.summary_str()}')
    
    # predict model
    pred = ml.predict(model, window)
    pred['predict'] = core.standardization(pred['predict'], ws.mean, ws.std, inverse=True).flatten().tolist()
    log.info(f'prediction result: {pred}')
    
    # export predict result of model    
    ml.export(ws, pred)
    