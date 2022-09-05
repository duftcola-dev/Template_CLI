from .utils.commands import Commands
from .utils.config import ConfigReader
from .utils.logging import Log 
from .utils.report import Report 
from .utils.metadata_template import TemplateMeta
import click
import os

class Procedures:

    def __init__(self,config_file_path:str,log_file_path:str) -> None:
        self.config_file_path=config_file_path
        self.logs_file_path=log_file_path
        self.commands = Commands()
        self.config = ConfigReader(self.config_file_path)
        self.report = Report(self.logs_file_path)
        self.metadata_template=TemplateMeta().get_template()
        self.log = Log().log
        self.alert = Log().alert

    
    def update_deppendencies(self):
        """Updates the list of deppendencies used installed.
        """
        click.clear()
        self.log("Updating deppendecies list",1)
        procedure = [
                    "pip freeze > ./cli/conf/requirements.txt",
                    "pip list > ./cli/conf/list.txt"
                    ]         
        if not os.path.isfile("./cli/conf/requirements.txt"):
            procedure.insert(0,"touch ./cli/conf/requirements.txt")
        if not os.path.isfile("./cli/conf/list.txt"):
            procedure.insert(0,"touch  ./cli/conf/list.txt")
        self.commands.execute(procedure,"Updating deppendencies list")
        report = self.commands.get_report()
        self.report.generate_report(report)
        self.log("Deppendencies list updated",1)
    

    def flush_logs(self):
        """Deletes all the content of the cli logs file.
        """
        click.clear()
        if not os.path.isfile("./cli/logs/logs.txt"):
            procedure = ["touch ./cli/logs/logs.txt"]
            self.commands.execute(procedure,"Updating deppendencies list")
        if self.report.flush_logs():
            self.log("Logs deleted",1)
        else:
            self.log("Cannot delete logs file",2)


    def get_templates_and_packages(self)->tuple:
        """_summary_

        Args:
            self (_type_): dict containing the available tamplates
            dict (_type_): dict containing the available packages
        """
        t = self.config.get_conf()
        templates = t.get("templates")
        packages = t.get("packages")
        return templates,packages

    
    def create_project(self,project_name:str,template_name:str):
        """Creates app project

        Args:
            project_name (str): Name of the project and the folder where it will be hosted
        """
        click.clear()
        if project_name =="cli" or "cli" in project_name:
            self.log(f"The name {project_name} or names that contain 'cli' are not valid.",2)
            return 

        templates:dict = self.config.get_conf().get("templates")
        origin = templates.get(template_name)
        procedure = [f"git clone {origin}"]
        self.commands.execute(procedure,"Downloading template")
        os.rename(template_name,project_name)
        project_root_path = os.getcwd()+"/"+project_name
        report = self.commands.get_report()
        self.report.generate_report(report)
        if os.path.isdir(project_root_path):
            self.log(f"Project {project_name} created",1)
        else:
            self.log(f"Cannot confirm project {project_name}",1)
        

    def create_project_metadata(self,project_name:str,template:str):
        """Creates the project metadata.
            The project metadata contains : 
            - project name 
            - project root directory 
            - installed packages
        This is information will be used to add additional modules.

        Args:
            project_name (str): project name
            template (str): template name
        """
        root = os.getcwd()+"/"+project_name
        config:dict=self.config.get_conf()
        projects:dict=config.get("projects")
        metadata_template=self.metadata_template.copy()
        metadata_template["name"]=project_name
        metadata_template["template"]=template
        metadata_template["root"]=root
        if project_name not in (list(projects.keys())):
            config["projects"][project_name]=metadata_template
            self.config.update_conf(config)
        else:
            self.log(f"The project {project_name} already exists",2)
            self.log(f"Aborting current project",2)
            self.log(f"To solve this issue you can :")
            self.log(f"1) Delete the project with the name : {project_name} and retry.")
            self.log(f"2) Use a different name than : {project_name} for your new project.")
        
        
            

