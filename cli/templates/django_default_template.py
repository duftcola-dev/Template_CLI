from genericpath import isdir
import os
from .utils.settings import  ROOT_DIR
from .utils.commands import Commands,Error
from .utils.logging import Log

class DjangoDefaultTemplate:

    def __init__(self) -> None:
        self.__project_name=""
        self.__applications=[]
        self.log=Log()
        self.excec_commands=Commands()
    


    def init(self,project_name:str,applications:list=None)->Error:
        self.__project_name=project_name
        self.__applications=applications
        to_run_commands=[]

        if os.path.isdir(project_name):
            self.log.log(f"Project {project_name} already exists.",2)
            self.log.alert("Aborting")
            return None

        if "test" in self.__applications or "tests" in self.__applications:
            self.log.log(self.__applications)
            self.log.log("The name 'test' or 'tests' is not allowed for applications",2)
            return None

        permisions=os.system("sudo echo 'Provide root premission : '")
        if permisions != 0:
            self.log.log("You must provide root privileges to proceed")
            return None

        self.log.log("Fetching deppendencies")
        to_run_commands+=self.__InstallDeppendencies()
       
        self.log.log(f"Deffining project layout : {self.__project_name}")
        to_run_commands+=self.__FormatingProject()
        
        self.log.log(f"Defining applications: {str(self.__applications)}") 
        to_run_commands+=self.__CreateApplications(self.__applications)
        
        self.excec_commands.execute(to_run_commands)

        self.log.log("Setting-up configuration")
        self.__SetupConfiguration()

        self.log.log("Setting up applications files")
        self.__SetUpApplicationFiles()

        self.log.log("Project ready",1,True)
        return None
        

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
            commands.append(f"mkdir applications/{application}")
            commands.append(f"django-admin startapp {application} applications/{application}")
        
        for application in applications:
            commands.append(f"touch applications/{application}/urls.py")

        return commands


    def __SetupConfiguration(self):
        dev=ROOT_DIR+"/"+self.__project_name+"/settings/"+"dev.py"
        prod=ROOT_DIR+"/"+self.__project_name+"/settings/"+"prod.py"
        test=ROOT_DIR+"/"+self.__project_name+"/settings/"+"test.py"

        test_database="""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
            """

        dev_database="""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'my_database',
        'USER': 'user',
        'PASSWORD': 'user_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
        """

        temp=[
            "from .base import *\n",
            "DEBUG = True\n",
"""
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
""",
            "\n\n",
            "# Session Cache ",
            "# https://docs.djangoproject.com/en/4.1/topics/cache/",
            "# https://pypi.org/project/pymemcache/",
            "\n\n",
        """
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:8000',
        }
    }
""",
        "\n\n",
"SESSION_ENGINE='django.contrib.sessions.backends.cache'\n",
        "\n\n",
        "# Database",
        "# https://docs.djangoproject.com/en/4.1/ref/settings/#databases",
        ]

        dev_lines=temp
        test_lines=temp

        dev_lines.append(dev_database)
        test_lines.append(test_database)

        self.excec_commands.InsertLines(dev,dev_lines,context="development configuration")
        self.excec_commands.InsertLines(test,test_lines,context="test configuration")


    def __SetUpApplicationFiles(self):
        root=ROOT_DIR+"/applications/"
        
        for application in self.__applications:
            if os.path.isdir(root+application):
                content=f"""
from django.apps import AppConfig

class {str(application).capitalize()}(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.{application}'
"""             
                file_path=root+application+"/apps.py"
                self.excec_commands.InsertText(file_path,content)
    
