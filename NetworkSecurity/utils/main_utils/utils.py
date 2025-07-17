import yaml
from NetworkSecurity.exception.exception import CustomException
from NetworkSecurity.logging.logger import logging
import os,sys
import numpy as np
import pandas as pd
import pickle
import dill


def read_yaml_file(file_path) ->dict:
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CustomException(e,sys)

def write_yaml_file(file_path:str,data:object,replace:bool=False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w') as yaml_file:
            yaml.dump(data, yaml_file)
    except Exception as e:
        raise CustomException(e,sys)

