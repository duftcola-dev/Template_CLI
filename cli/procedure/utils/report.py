from datetime import datetime
from .logging import Log

class Report(Log):

    def __init__(self,path:str) -> None:
        super().__init__()
        self.path=path
    
    def generate_report(self,report:list)->bool:
        """Generaters saves logs of the activity of the cli into a file.

        Args:
            report (list): Colection of logs generated during the
            command execution process.
        Returns:
            bool: True if the records where saved . False if the operation failed.
        """
        try:
            file=open(self.path,"a")
            date = str(datetime.now())
            temp = f"---- {date}\n"
            file.write(temp)
            for line in report :
                file.write(line+"\n")
            file.close()
            return True
        except FileNotFoundError as f_err:
            self.alert("Report : Log file cannot be found",2)
            self.log(str(f_err),2)
            return False
        except Exception as err:
            self.alert("Report : Unknown error",2)
            self.log(str(err),2)
            return False
    
    def flush_logs(self):
        """Deletes all logs from the log file
        """
        try:
            file=open(self.path,"w")
            file.write("")
            file.close()
            return True
        except FileNotFoundError as f_err:
            self.alert("Report : Log file cannot be found",2)
            self.log(str(f_err),2)
            return False
        except Exception as err:
            self.alert("Report : Unknown error",2)
            self.log(str(err),2)
            return False
    
