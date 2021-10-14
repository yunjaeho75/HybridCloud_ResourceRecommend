import sys
import logging
import logging.handlers

formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(name)s: %(message)s')
streamHandler = None
fileHandler = None
logLevels = [
    logging.DEBUG ,
    logging.INFO ,
    logging.WARNING ,
    logging.ERROR ,
    logging.CRITICAL ]
levelSize = len(logLevels)
logVerbose = 1
logFile = None

def getLogLevel(verbose):
    return logLevels[verbose]

def init(ws):
    global logVerbose
    global logFile

    #logWS = ws
    logFile = ws.log
    logVerbose = ws.verbose
    if logVerbose < 0 or logVerbose > (levelSize - 1):
        logVerbose = 1
    reset()

def reset():    
    global streamHandler
    global fileHandler

    logging.basicConfig()
    logging.root.setLevel(logging.NOTSET)
    logging.basicConfig(level=logging.NOTSET)

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    streamHandler.setLevel(getLogLevel(logVerbose))

    err = None
    try:
        fileHandler = logging.FileHandler(logFile)
        fileHandler.setFormatter(formatter)
        fileHandler.setLevel(getLogLevel(logVerbose))
    except FileNotFoundError as e:
        err = e
    except AttributeError as e:
        err = e
    except IsADirectoryError as e:
        err = e    

    if err is not None:
        l = logging.getLogger(__name__)
        l.addHandler(streamHandler)
        logging.root = l
        l.error("Create log file failed.")
        sys.exit()



def get(name):
    l = logging.getLogger(name)

    if len(l.handlers) > 0:
        return l # Logger already exists
    
    l.addHandler(streamHandler)
    l.addHandler(fileHandler)
    l.setLevel(getLogLevel(logVerbose))

    logging.root = l

    return l

