from flask import Flask, request, jsonify, Response
from flask_restful import Resource, Api
from waitress import serve
from ..core import workspace, options, logger


class message():
    def __init__(self, message, code):
        self.msg = dict()
        self.msg['msg'] = message
        self.code = code

# Create Flask instance
app = Flask(__name__)
api__ = Api(app)
status = message("The request cannot be processed", 400)

class api():
    def run(self):
        #app.run(host="0.0.0.0", port="5000", debug=True)
        serve(app, host="0.0.0.0", port="5000")

    def add_resource(self, obj, api):
        api__.add_resource(obj, api)


    
def get_json():
    data = request.get_json(silent=True)
    if data is None:
        global status
        status = message("Missing JSON in body", 400)
    return data

def is_json():
    if not request.is_json:
        global status
        status = message("Missing JSON in request", 400)
        return False
    return True


def get_message():
    return jsonify(status.msg), status.code


# global
ws = None
model = None

def init(args):
    global ws, model

    # get config
    ws = workspace.from_config(args)
    print('\n$> config:\n', ws)

    # set service name
    ws.set_service(options.service.estimator)


def load_model(ws, ml):
    global model
    log = logger.get(__name__)
    model = ml.load_model(ws)
    log.info(f'load model: {ws.load_path()}')
    log.debug(f'model summary:\n{model.summary_str()}')
