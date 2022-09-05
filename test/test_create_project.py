import os 
import shutil
def test_get_templates(get_procedures):
    templates = get_procedures.config.get_conf().get("templates") 
    default_app = templates.get("app_template")
    assert isinstance(templates,dict) == True 
    assert isinstance(default_app,str) == True 


def test_get_modules(get_procedures):
    pacakge = get_procedures.config.get_conf().get("packages") 
    redis = pacakge.get("redis")
    assert isinstance(pacakge,dict) == True 
    assert isinstance(redis,str) == True 


def test_modules_and_templates(get_procedures):
    result = get_procedures.get_templates_and_packages()
    assert isinstance(result,tuple) == True
    assert isinstance(result[0],dict) == True
    assert isinstance(result[1],dict) == True


def test_create_project(get_procedures):
    project_name = "test_project"
    template = "app_template"
    os.path.isdir("test_project/") == False
    get_procedures.create_project(project_name,template)
    os.path.isdir("test_project/") == True
    shutil.rmtree("test_project/")
    os.path.isdir("test_project/") == False
    


def test_project_data_update(get_procedures):
    """Creates the metadata about the project created .
    The project metadata contains : 
        - project name 
        - project root directory 
        - template type
        - installed packages
    Args:
        get_procedures (Procedures): Procedures class
    """
    root=os.getcwd()+"/"+"test"
    project_name="test"
    project_template="app_template"
    metadata_template={
            "name":"test",
            "template":project_template,
            "root":root,
            "installed":["package1","package2"]
        }
    config:dict=get_procedures.config.get_conf()
    if project_name not in list(config["projects"].keys()):
        # a new project will be created
        config["projects"][project_name]=metadata_template
        get_procedures.config.update_conf(config)
    new_config:dict=get_procedures.config.get_conf()
    assert isinstance(config,dict) == True
    assert isinstance(new_config,dict) == True
    assert new_config.get("projects") is not None 
    assert new_config["projects"][project_name] is not None
    assert new_config["projects"][project_name]["name"]==project_name
    #cleanup mess 
    


def test_delete_project(get_procedures):
    """Test the functionality of deleting a project
        while also updating the project metadata.

    Args:
        get_procedures (Procedures): Procedures class
    """
#     # check temp project does not exists
#     project_name = "test_project"
#     template = "app_template"
#     root=os.getcwd()+"/"+"test_project"

#     # create temporal project
#     assert os.path.isdir(root) == False
#     get_procedures.create_project(project_name,template)
#     assert os.path.isdir(root) == True

#    # create project metadata
#     metadata_template={
#             "name":project_name,
#             "template":template,
#             "root":root,
#             "installed":["package1","package2"]
#         }
    
    
#     # check project metadata does not exists
#     config:dict=get_procedures.config.get_conf()
#     assert config is not None
#     assert config.get("projects") is not None
#     assert isinstance(config,dict) == True
#     assert project_name not in list(config["projects"].keys())
#     # update project metadata with new project created
#     config["projects"][project_name]=metadata_template
#     get_procedures.config.update_conf(config)
#     #check configuration have changed with new project data
#     config:dict=get_procedures.config.get_conf()
#     assert config["projects"].get(project_name) is not None
#     assert config["projects"].get(project_name)["name"] == project_name

#     #deleting projects and update conf 
#     shutil.rmtree(root)
#     assert os.path.isdir(root) == False 

#     # delete configuration of deleted project
#     old_config = config.copy()
#     config["projects"].pop(project_name)
#     assert config["projects"].get(project_name) is None 
#     # update configuration
#     get_procedures.config.update_conf(config)
#     # check configuration has changed
#     config:dict=get_procedures.config.get_conf()
#     assert old_config != config 
#     assert config["projects"].get("test") is None 


