import json 
from .logging import Log
class ConfigReader(Log):

    def __init__(self,conf_path) -> None:
        super().__init__()
        self.path=conf_path


    def get_conf(self)->dict:
        """Loads the finguration file content.

        Raises:
            Exception: Cannot load content of the configuration file or
            it cannot be found
            Exception: Cannot load key templates in the configuration
            Exception: Cannot load key modules in the configuration

        Returns:
            dict: Configuration file content as a dict
        """
        try:
            file = open(self.path,"r")
            content = file.read()
            config:dict = json.loads(content)
            if config is None or isinstance(config,dict) != True:
                raise Exception(f"Cannot load configuration at : {self.path}")
            config.get("templates")
            if config.get("templates") is None:
                raise Exception(f"Cannot load templates")
            if  config.get("packages") is None:
                raise Exception(f"Cannot load packages")
            file.close()
            self.log("Templates and pacakages loaded",1)
            return config
        except FileNotFoundError as f_err:
            self.alert("Config : File not found. Cannot load configuration",2)
            self.log(f"File not found at {self.path}",3)
        except Exception as err :
            self.alert("Config : Error",2)
            self.log(str(err))
    

    def update_conf(self,conf:dict):
        try:
            file= open(self.path,"w")
            content=json.dumps(conf,indent=4)
            file.write(content)
            file.close()
        except FileNotFoundError as f_err:
            self.alert("Config : File not found. Cannot save configuration",2)
            self.log(f"File not found at {self.path}",3)
        except Exception as err :
            self.alert("Config : Error",2)
            self.log(str(err))
        
