import click
from settings.settings import DjangoDefaultTemplate
from settings.logging import Log    
l=Log()

@click.group()
def cli():
    pass 


@click.command()
def create_project():
    """Create project eskeleton
    """
    l.log("Creating project",0,True)
    error=DjangoDefaultTemplate().init("test_project",["test","users","stores"])


@click.command()
def build_project():
    """Commands related to the logs file
    """
    print("Building project")

@click.command()
def deploy_project():
    print("Deploying project")


@click.command()
def delete_project():
    print("Deleting project")
    # log("ATTENTION","","red",True,False)
    # log("The following action will delete content.","red","",False,False)
    # log("Mapping content ...","red","",False,False)
    # flush_process = FLushProcess(conf_path)
    # flush_process.run()
    pass

if __name__ == "__main__":
    cli.add_command(create_project)
    cli.add_command(build_project)
    cli.add_command(deploy_project)
    cli.add_command(delete_project)
    cli()