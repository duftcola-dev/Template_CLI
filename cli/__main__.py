import click
import os
from procedure.procedure_generator import Procedures

#cli files path
conf_path=os.getcwd()+"/cli/conf/conf.json"
logs_path=os.getcwd()+"/cli/logs/logs.txt"
#deppendencies
procedures = Procedures(conf_path,logs_path)

@click.group()
def cli():
    pass 


@click.command()
def dep():
    """Update deppendencies list
    """
    procedures.update_deppendencies()

@click.command()
def logs():
    """Commands related to the logs file
    """
    procedures.flush_logs()

@click.command()
def init():
    pass


@click.command()
def flush():
    # log("ATTENTION","","red",True,False)
    # log("The following action will delete content.","red","",False,False)
    # log("Mapping content ...","red","",False,False)
    # flush_process = FLushProcess(conf_path)
    # flush_process.run()
    pass

if __name__ == "__main__":
    cli.add_command(init)
    cli.add_command(flush)
    cli.add_command(dep)
    cli.add_command(logs)
    cli()