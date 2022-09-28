import click 
from datetime import datetime

class Log:

    def __init__(self) -> None:
        pass

    def alert(self,message:str,color:int):
        """Prints and alert int the console. There are 3 available options : 
            0 = "green"
            1 = "yellow"
            2 = "red"

        Args:
            message (str): Message to be passed to the console.
            background (int): Background color of the alert.
        """
        if not isinstance(color,int):
            raise Exception("Param background must be int")
        if not isinstance(message,str):
            raise ValueError("Param message must be str")
        colors = ["green","yellow","red"]
        click.secho(message,fg="white",bg=colors[color],bold=True)


    def log(self,message:str,color:int=0,date:bool=False):
        """Prints a log message in the console.
        There are 4 available colors : 

            0 = default white 
            1 = green
            2 = yellow 
            3 = red

        Args:
            message (str): _description_
            color (int, optional): Text color. Defaults to 0.
            date (bool, optional): If True the message will display the current date. 
            Defaults to False.
        """
        if not isinstance(message,str):
            raise Exception("Param message must be str")
        if not isinstance(color,int):
            raise Exception("Param color must be int")  
        colors = ["white","green","yellow","red"]
        current_date = datetime.now()
        if date:
            message = message + " - "+str(current_date)
        click.secho(message,fg=colors[color])