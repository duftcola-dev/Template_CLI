from genericpath import isfile
import click 
from typing import Tuple
import os
from .logging import Log

class Error:

    def __init__(self,error:str) -> None:
        self.error=f"""
        The proccess execution failed.
        The following command line : \n 
        {error} .\n
        Resulted in an error with exit code 1.
        """ 
    
    def __str__(self)->str:
        return self.error 

    def __call__(self)->str:
        return self.error



class Commands(Log):

    def __init__(self) -> None:
        super().__init__()
        self.last_command=None
          
    def execute(self,commands:list)->Tuple[list,Error]:
        """Runs a line of commands.

        Args:
            commands (list): Lines of commands to run in console.

        Returns:
            Tuple[list,Error]: If suceess returns list,None. If error returns None,Error
        """
        try:
            with click.progressbar(commands,length=len(commands)) as execute_commands:
                for command in execute_commands:
                    result=os.system(command+" >/dev/null 2>&1")
                    self.last_command=command
                    if result != 0:
                        return None,Error(command)
            return commands,None

        except Exception as err:
            self.alert("Line of commands failed",1)
            message=f"Command : {self.last_command} caused and error : {str(err)}"
            self.log(message,3)
            return None,Error(message)
           

    def Insert(self,file_path:str,lines:list)->Tuple[bool,Error]:
        """Insert content into files.

        Args:
            file_path (str): Path to file to insert data.
            lines (list): Lines to insert in file

        Returns:
            Tuple[bool,Error]: _description_
        """

        if os.path.isfile(file_path) ==False:
            return False,Error(f"The file {file_path} cannot be found or was not created.")
        try:
            file = open(file_path,"a")
            for line in lines:
                file.write(line)
            file.close()
            return True,None
        except Exception as err :
            self.log(f"Unknown exception : {err}",3)
            return False,Error(f"Error: {err}")

        
