import pathlib
from typing import Tuple
from .commands import Commands,Error
from .logging import Log
ROOT_DIR=str(pathlib.Path(__file__).resolve().parent.parent.parent)
SETTINGS_PATH=str(pathlib.Path(__file__).resolve())
LOGS_PATH=str(pathlib.Path(__file__).resolve().parent.parent)


class DjangoDefaultTemplate:

    def __init__(self) -> None:
        self.__project_name=""
        self.__applications=[]
        self.log=Log()
        self.excec_commands=Commands()


    def init(self,project_name:str,applications:list=None)->Error:
        self.__project_name=project_name
        self.__applications=applications

        self.log.log("Installing deppendencies")
        result,error=self.excec_commands.execute(self.__InstallDeppendencies())
        if error is not None:
            return error

        self.log.log(f"Formating project : {self.__project_name}")
        result,error=self.excec_commands.execute(self.__FormatingProject())
        if error is not None:
            return error 
            
        self.log.log("Setting up configuration")


        

    def __InstallDeppendencies(self)->list:
        commands=[
            "sudo apt-get install python3-dev default-libmysqlclient-dev build-essential",
            "sudo apt install libpq-dev python3-dev",
            ". venv/bin/activate ; pip install django --upgrade pip",
            ". venv/bin/activate ; pip install django pymemcache",
            f". venv/bin/activate ; django-admin startproject {self.__project_name}",
        ]
        return commands

    def __FormatingProject(self)->list:
        commands=[ 
            f"mv {self.__project_name} __{self.__project_name}",
            f"mv __{self.__project_name}/{self.__project_name} .",
            f"mv __{self.__project_name}/manage.py .",
            f"rmdir __{self.__project_name}",
            f"mkdir applications",
            f"mkdir {self.__project_name}/settings",
            f"mkdir {self.__project_name}/templates",
            f"mkdir {self.__project_name}/static",
            f"mv {self.__project_name}/settings.py {self.__project_name}/settings/settings.py",
            f"mv {self.__project_name}/settings/settings.py {self.__project_name}/settings/base.py",
            f"touch {self.__project_name}/settings/prod.py",
            f"touch {self.__project_name}/settings/dev.py",
            f"touch {self.__project_name}/settings/test.py",
            "touch .gitignore",
            "touch README.md",
            "mkdir docker",
            "mkdir docker/dev/",
            "mkdir docker/prod/",
            "mkdir docker/test/",
            "touch docker/dev/dockerfile",
            "touch docker/prod/dockerfile",
            "touch docker/test/dockerfile",
            "touch docker/docker-compose.yml",
        ]
        return commands


    def __CreateApplications(self,applications:list):
        commands=[]

        for application in applications:
            commands.append(f"django-admin startapp {application} applications/{application}")
        
        for application in applications:
            commands.append(f"touch applications/{application}/urls.py")
