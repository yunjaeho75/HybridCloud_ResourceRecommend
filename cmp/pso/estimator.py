import os
import sys
from ..core import workspace, dataset, options, logger, util
from . import engine as ml

import pandas as pd
import numpy as np

def main(args):
    
    print('$>', args)

    # get config
    ws = workspace.from_config(args)
    print('\n$> config:\n', ws)

    # set service name
    ws.set_service(options.estimator.pso)

    # initialize logger 
    logger.init(ws)

    # get dataset
    data = dataset.get(ws)

    # get model
    model = ml.load_model(ws)
        
    #test(ws)
    result = ml.optimize(ws, model, data)

    # export predict result of model
    ml.export(ws, result)



import pandas as pd
import numpy as np
def test(ws):
    #print(util.euclidean_distance(np.array([  4.,  28., 200.]), np.array([ 1. ,  3.5, 50. ])))    
    #print(np.all(np.array([248., 5708., 8188.]) >= np.array([416., 5700., 8192.])))
    #print(np.array([1,1.75,40]) / np.array([ 1.,  .5, 1. ]))

    # result = np.where(np.array([248., 5708., 8188.]) < np.array([416., 5700., 8192.]))
    # if result[0].size:
    #     print("False")
    # else:
    #     print("True")

    arr = [24,224,1440]
    
    print(df)

    pass