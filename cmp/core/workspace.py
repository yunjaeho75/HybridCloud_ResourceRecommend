import os as _os
import pandas as pd
import sys
from ..data import helper
from . import logger



def arg_parse(args, action='model', default='None'):
    try:
        value = getattr(args, action)
    except AttributeError as err:
        try:
            return eval(default)
        except NameError as err:
            return default
        except SyntaxError as err:
            return default
    return value

def from_config(args):
    ws = Workspace()
    ws.name = arg_parse(args, action="name", default='Unkown')
    ws.input = arg_parse(args, action="input", default='None')
    ws.output = arg_parse(args, action="output", default=_os.getcwd())
    ws.base_model = arg_parse(args, action="base_model", default="None")
    ws.data_helper = arg_parse(args, action="data_helper", default="None")
    ws.model = arg_parse(args, action="model", default="None")
    ws.output_consol = arg_parse(args, action="output_consol", default="False")
    ws.output_file = arg_parse(args, action="output_file", default="False")
    ws.log = arg_parse(args, action="log", default="./")    
    ws.verbose = arg_parse(args, action="verbose", default="1")
    ws.optimizer = arg_parse(args, action="optimizer", default="None")
    ws.Init()
    return ws

class config:
    name: str
    input: str
    output: str
    base_model: str
    data_helper: str

class Workspace(config):
    # def describe(self):
    #     return "\r--name: {}\n--input: {}\n--output: {}\n--base-model: {}\n--data-helper: {}\n".format(
    #         self.name, self.input, self.output, self.base_model, self.data_helper)

    def Init(self):
        # read scv data
        err = None
        if self.model is not None and self.optimizer is None:
            try:
                path = _os.path.abspath(f"{self.model}/meta.csv")            
                df = pd.read_csv(path)
                self.__mean__ = float(df.loc[(df['property'] == 'mean'), 'value'])
                self.__std__ = float(df.loc[(df['property'] == 'std'), 'value'])
            except FileNotFoundError as e:
                err = e
            except AttributeError as err:
                err = e

            if err is not None:
                logger.init(self)
                log = logger.get(__name__)
                log.error("Not found meta data.")
                sys.exit()
        
    def __repr__(self):
        return ''.join([
            '\rWorkspace(',
            f"name='{self.name}', ",
            f"input='{self.input}', ",
            f"output='{self.output}', ",
            f"base-model='{self.base_model}', ",
            f"data-helper='{self.data_helper}', ",
            f"model='{self.model}', ",
            f"output_consol='{self.output_consol}', ",
            f"output_file='{self.output_file}', ",
            f"log='{self.log}', ",
            f"verbose='{self.verbose}'",
            ')'])

    def load_path(self):
        return f'{self.model}'

    def save_path(self):
        return f'{self.output}/{self.name}'

    def export_path(self):
        return f'{self.output}'

    def set_service(self, service):
        self.service=service

    @property
    def mean(self):
        return self.__mean__
    
    @property
    def std(self):
        return self.__std__

    @mean.setter
    def mean(self, v):
        self.__mean__ = v
    
    @std.setter
    def std(self, v):
        self.__std__ = v
