from . import engine
from .. import pso
from ..core import workspace, options, logger
from ..data import helper as data_helper
import json


@engine.app.route('/pso/estimator', methods = ['POST'])
def pso_estimator():
    log = logger.get(__name__)

    if not engine.is_json():
        return engine.get_message()
    
    body = engine.get_json()#json 데이터를 받아옴
    if not body:
        return engine.get_message()

    # get dataset
    helper = data_helper.get(engine.ws)
    data = helper.create(body['sequance'])

    # predict model
    pred = pso.optimize(engine.ws, engine.model, data)
    pred['label'] = body['label']

    # export json
    return engine.Response(pso.jsondump(pred), mimetype='application/json'), 200
    


def main(args):
    print('$>', args)

    # initialize engine 
    engine.init(args)

    # initialize logger 
    logger.init(engine.ws)
    
    # load model
    engine.load_model(engine.ws, pso)
    
    app = engine.api()
    app.run()
