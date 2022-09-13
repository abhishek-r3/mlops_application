"""
This is a script to register the trained model to azure cloud
"""

from azureml.core import Model 
from ..azureutils.workspace import AZWorkspace

def register_model_to_azure_workspace(ws, model_name, model_path, 
                                      model_framework = Model.Framework.SCIKITLEARN, 
                                      model_frame_work_version = "1.1.2"):
    """
    Function registers the trained model to azure cloud workspace
    """
    
    ## Register the trained model
    print("Registering Model To Azure Cloud.....")

    try:

        azure_model = Model.register(workspace=ws,
                                model_name = model_name,
                                model_path = model_path,
                                model_framework = model_framework,
                                model_framework_version = model_frame_work_version)
        print("Sucessfully registerd model : ", model_name)
        return azure_model
    
    except Exception as e:
        print("Error while registering the model to azure workspace")
        print(e)

def get_list_of_models_in_workspace(workspace_name, subscription_id, resource_group):
    """
    Function to get the list of models from the workspace
    """

    ws = AZWorkspace.load_azure_workspace(workspace_name, subscription_id, resource_group)

    try:
        models_in_ws = {}
        #view the registered model
        for i, model in enumerate(Model.list(ws)):
            models_in_ws[i] = [model.name, model.version]
        return models_in_ws
    
    except Exception as e:
        print("Error while listing the models")
        print(e)


def start_model_registration(workspace_name, subscription_id, resource_group, model_name, model_path,):
    """
    """

    ws = AZWorkspace.load_azure_workspace(workspace_name, subscription_id, resource_group)
    azure_model = register_model_to_azure_workspace(ws, model_name, model_path)
    return azure_model