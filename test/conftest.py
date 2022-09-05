from cli import Procedures
import pytest
import os

@pytest.fixture
def get_procedures():

    conf_path=os.getcwd()+"/cli/conf/conf.json"
    logs_path=os.getcwd()+"/cli/logs/logs.txt"
    procedures =  Procedures(conf_path,logs_path)
    return procedures
 