from datetime import datetime
import os
from string import Template
from ..deppedencies import Error,Commands,Log,ROOT_DIR
from .dev import DEV
from .test import TEST
from .apps import APPS
from .url import URLS
from .html_layout import LAYOUT,FOOTER,HEADER,HOME
from .docker_dev import DOCKER_DEV 
from .docker_prod import DOCKER_PROD 
from .docker_test import DOCKER_TEST


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
            self.log.log(f"Project --> {project_name} already exists.",2)
            self.log.alert("Aborting",1)
            return None

        if "test" in self.__applications or "tests" in self.__applications:
            self.log.log(self.__applications)
            self.log.log("The name 'test' or 'tests' is not allowed for applications",2)
            return None

        permisions=os.system("sudo echo 'Provide root privileges to proceed : '")
        if permisions != 0:
            self.log.log("You must provide root privileges to proceed")
            return None

        self.log.log("Fetching deppendencies")
        to_run_commands+=self.__InstallDeppendencies()
       
        self.log.log(f"Defining project layout : {self.__project_name}")
        to_run_commands+=self.__FormatingProject()
        
        self.log.log(f"Defining applications: {str(self.__applications)}") 
        to_run_commands+=self.__CreateApplications(self.__applications)
        
        self.excec_commands.execute(to_run_commands)

        self.log.log("Setting-up configuration")
        self.__SetupConfiguration()

        self.log.log("Setting-up applications files")
        self.__SetUpApplicationFiles()

        self.log.log("Setting-up urls files")
        self.__SetUpUrlFiles()

        self.log.log("Creating html templates")
        self.__SetUpHTMLTemplates()

        self.log.log("Creating dockerfiles for prod | dev | test")
        self.__ConfigureDockerFiles()

        self.log.log("Creating environment files")
        self.__SetEnvironmentFiles()
        
        os.system("tree -d -L 1")
        self.log.log("Project ready",1,True)
        return None
        

    def __InstallDeppendencies(self)->list:
        commands=[
            "sudo apt-get install python3-dev default-libmysqlclient-dev build-essential",
            "sudo apt install tree",
            "sudo apt install libpq-dev python3-dev",
            ". venv/bin/activate ; pip install django pymemcache psycopg2 pytest  --upgrade pip",
            "mkdir requirements",
            ". venv/bin/activate ; pip freeze > ./requirements/base.txt"
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
            f"mkdir .github",
            f"mkdir .github/workflows",
            f"mkdir {self.__project_name}/settings",
            f"mkdir {self.__project_name}/templates",
            f"mkdir {self.__project_name}/templates/include",
            f"mkdir {self.__project_name}/templates/layout",
            f"mkdir {self.__project_name}/static",
            f"mv {self.__project_name}/settings.py {self.__project_name}/settings/settings.py",
            f"mv {self.__project_name}/settings/settings.py {self.__project_name}/settings/base.py",
            f"touch {self.__project_name}/settings/prod.py",
            f"touch {self.__project_name}/settings/dev.py",
            f"touch {self.__project_name}/settings/test.py",
            f"touch {self.__project_name}/settings/__init__.py",
            "touch .gitignore",
            "touch README.md",
            "touch .dockerignore",
            "mkdir docker",
            "mkdir docker/dev/",
            "mkdir docker/prod/",
            "mkdir docker/test/",
            "touch docker/dev/dockerfile",
            "touch docker/prod/dockerfile",
            "touch docker/test/dockerfile",
            "touch docker/docker-compose.yml",
            f"touch {self.__project_name}/templates/home.html",
            f"touch {self.__project_name}/templates/layout/_layout.html",
            f"touch {self.__project_name}/templates/include/_header.html",
            f"touch {self.__project_name}/templates/include/_footer.html",
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
        test=ROOT_DIR+"/"+self.__project_name+"/settings/"+"test.py"

        applications_list=""
        for application in self.__applications:
            applications_list=applications_list+f"'applications.{application}',\n    "


        dev_conf=Template(DEV).substitute(applications=applications_list,)
        test_conf=Template(DEV).substitute(applications=applications_list,)
        self.excec_commands.InsertText(dev,dev_conf)
        self.excec_commands.InsertText(test,test_conf)



    def __SetUpApplicationFiles(self):
        root=ROOT_DIR+"/applications/"
        
        for application in self.__applications:
            if os.path.isdir(root+application):
                content=Template(APPS).substitute(app_class=str(application).capitalize(),appls="applications."+application)
                file_path=root+application+"/apps.py"
                self.excec_commands.InsertText(file_path,content)
    

    def __SetUpUrlFiles(self):
        root=ROOT_DIR+"/applications/"
        for application in self.__applications:
            if os.path.isdir(root+application):
                file_path=root+application+"/urls.py"
                self.excec_commands.InsertText(file_path,URLS)

    
    def __SetUpHTMLTemplates(self):
        root=ROOT_DIR+"/"+self.__project_name 
        _home=root+"/templates/home.html"
        _layout=root+"/templates/layout/_layout.html"
        _header=root+"/templates/include/_header.html"
        _footer=root+"/templates/include/_footer.html"

        home=HOME
        layout=LAYOUT
        header=HEADER
        footer=FOOTER 
        

        self.excec_commands.InsertText(_layout,layout)
        self.excec_commands.InsertText(_header,header)
        self.excec_commands.InsertText(_footer,footer)
        self.excec_commands.InsertLines(_home,home)


    def __ConfigureDockerFiles(self):

        root=ROOT_DIR+"/docker"
        _docker_dev=root+"/dev/dockerfile"
        _docker_prod=root+"/prod/dockerfile"
        _docker_test=root+"/test/dockerfile"

        docker_dev=Template(DOCKER_DEV).substitute(project=self.__project_name)
        docker_prod=Template(DOCKER_PROD).substitute(project=self.__project_name)
        docker_test=Template(DOCKER_TEST).substitute(project=self.__project_name)
        
        self.excec_commands.InsertText(_docker_dev,docker_dev)
        self.excec_commands.InsertText(_docker_prod,docker_prod)
        self.excec_commands.InsertText(_docker_test,docker_test)

    
    def __SetEnvironmentFiles(self):

        root=ROOT_DIR+"/"
        _gitignore=root+".gitignore"
        _readme=root+"README.md"
        _dockerignore=root+".dockerignore"

        gitignore="""
venv/
__pycache__
__pycache__/
.pyc
        """
        date = datetime.now()
        readme=f"""
# <project_name> 
## Author : 
## Date: {date}
## Version : 1.0 
## Stable : No
## Requirements: 
    - Linux Ubuntu
    - Docker | Docker-Compose 
    - Django 
    - psycopg2
## Description: 
     <project_description> 
## Usage:

        """

        self.excec_commands.InsertText(_gitignore,gitignore)
        self.excec_commands.InsertLines(_dockerignore,gitignore)
        self.excec_commands.InsertLines(_readme,readme)