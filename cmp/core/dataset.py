import sys
from ..data import helper as data_helper
from ..core import logger

def get(ws):
    log = logger.get(__name__)
    handler = data_helper.get(ws)
    if handler is None:
        log.error(f"Not found data helper (data-helper={ws.data_helper})")
        sys.exit()

    data = handler.load_data(ws)
    if data is None:
        log.error(f"Load data set failed.")
        sys.exit()

    return data
    
    
