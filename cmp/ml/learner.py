import os
import sys
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
    log.info(f'start learner porcess.')
    
    # set service name
    ws.set_service(options.service.learner)
    
    # get dataset
    data = dataset.get(ws)
    log.debug(f"dataset:\n{data.describe()}")
    
    # create time window
    window = ml.window_generator(ws, data)
    log.info(f'window.column.indices: {window.column_indices}')
    log.info(f'window.input.shape: {window.example[0].shape}')
    log.debug(f'window.describe:\n{window}')
    
        
    # get model
    model = ml.get_model(ws)
    log.debug(f'model summary:\n{model.summary_str()}')
    
    
    # comple model
    history = ml.compile(model, window)

    # save model
    ml.save(ws, model)
    
    # evaluate model
    val, test = ml.evaluate(model, window)
    log.info('result evaluate:')
    log.info(f'- val : {val}')
    log.info(f'- test: {test}')

    