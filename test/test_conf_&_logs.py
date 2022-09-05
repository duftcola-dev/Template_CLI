import os

def test_conf_deppendencies(get_procedures):
    os.remove("./cli/conf/requirements.txt")
    os.remove("./cli/conf/list.txt")
    assert os.path.isfile("./cli/conf/requirements.txt") == False
    assert os.path.isfile("./cli/conf/list.txt") == False
    get_procedures.update_deppendencies()
    assert os.path.isfile("./cli/conf/requirements.txt") == True
    assert os.path.isfile("./cli/conf/list.txt") == True
    assert os.path.isfile("./cli/conf/conf.json") == True


def test_logs_reports(get_procedures):
    os.remove("./cli/logs/logs.txt")
    assert os.path.isfile("./cli/logs/logs.txt") == False
    get_procedures.flush_logs()
    assert os.path.isfile("./cli/logs/logs.txt") == True


def test_load_conf(get_procedures):
    result = get_procedures.config.get_conf()
    assert result is not None
    templates = result.get("templates")
    packages = result.get("packages")
    assert isinstance(result,dict) == True
    assert isinstance(packages,dict) == True
    assert isinstance(templates,dict) == True