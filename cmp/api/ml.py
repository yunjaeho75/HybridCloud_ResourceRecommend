from . import engine
from .. import ml
from .. import core
from ..core import workspace, options, logger
from ..data import helper as data_helper
import json


@engine.app.route('/ml/estimator', methods = ['POST'])
def ml_estimator():
    log = logger.get(__name__)

    if not engine.is_json():
        return engine.get_message()
    
    body = engine.get_json()#json 데이터를 받아옴
    if not body:
        return engine.get_message()

    helper = data_helper.get(engine.ws)    
    data = helper.create(body['sequance'])
    if data is None:
        log.error(f"Load data set failed.")
        return engine.get_message()

    # create time window
    window = ml.window_generator(engine.ws, data)
    #log.info(f'input shape: {window.shape()}')
    log.info(f'input shape: {window.shape()}')
    
    
    # predict model
    pred = ml.predict(engine.model, window)
    pred['label'] = body['label']
    pred['predict'] = core.standardization(pred['predict'], engine.ws.mean, engine.ws.std, inverse=True).flatten().tolist()    

    # export json
    pred = json.dumps(pred, indent=4)
    log.info(f'export json: {pred}')
    return engine.Response(pred, mimetype='application/json'), 200



def main(args):
    print('$>', args)

    # initialize engine 
    engine.init(args)

    # initialize logger 
    logger.init(engine.ws)
    log = logger.get(__name__)
    
    helper = data_helper.get(engine.ws)
    if helper is None:
        log.error(f"Not found data helper (data-helper={engine.ws.data_helper})")
        return

    # load model
    engine.load_model(engine.ws, ml)

    app = engine.api()
    app.run()
