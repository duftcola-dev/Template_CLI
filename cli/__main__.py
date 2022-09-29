import click
from templates.django_default_template import DjangoDefaultTemplate
from templates.utils.logging import Log    
l=Log()

@click.group()
def cli():
    pass 


@click.command()
@click.option("-t","--type",required=True,default="default",type=str)
@click.option("-n","--name",required=False,default="project",type=str)
@click.option("-a","--app",required=False,default="myapp",type=str)
def create_project(type:str,name:str,app:str):
    """ - create-project \n
    Create a project eskeleton by selecting a project type, a project name 
    and the number of applications that project supports.
    Some project support only one application.\n
    Arguments :\n 
        * -t | --type  <project_type> \n
        * -n | --name  <project_name> | default : project \n
        * -a | --app  <applications> | default : myapp  \n 

        example : \n 

        python cli -t default_app -n myproject -a app1,app2,app3
    """
    if type:
        print(type)
    if name:
        print(name)
    if app:
        print(app)

    l.log("Creating project",0,True)
    app=app.split(",")
    print(app)
    error=DjangoDefaultTemplate().init(name,app)


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