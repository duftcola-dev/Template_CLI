import click 
import click 
import os
from .logging import Log
class Commands(Log):

    def __init__(self) -> None:
        super().__init__()
        self.last_command=None
        self.to_exec_commands=None 
        self.procedure=None
        self.error=None
  
  
    def execute(self,commands:list,procedure_name:str)->bool:
        """Runs a list of shell commands . If any command fails
        the process is interrupted and returns False

        Args:
            commands (list): list pf shell commands.
            procedure (list,optional) : procedure name used in the report description.
        Returns:
            bool: True if the opration suceeded . False if it failed
        """
        self.last_command=None
        self.to_exec_commands=commands 
        self.procedure=procedure_name
        self.error=None
        self.log("Executing...")
        try:
            with click.progressbar(commands,length=len(commands)) as bar:
                for command in bar:
                    self.last_command=command
                    result=os.system(command)
                    if result != 0:
                        raise Exception(f"{command} --> exit code 1")
            return True
        except Exception as err:
            self.alert("Line of commands failed",1)
            message=f"Command : {self.last_command} caused and error : {str(err)}"
            self.error=message
            self.log(message,3)
            return False
    

    def get_report(self)->list:
        report=self.to_exec_commands
        report.insert(0,f"Procedure : {self.procedure}")
        if self.error is None:
            report.append(f"+++++ Success +++++")
        else:
            report.append(f"Last command : {self.last_command}")
            report.append(f"Error : {str(self.error)}")
        return report



        
