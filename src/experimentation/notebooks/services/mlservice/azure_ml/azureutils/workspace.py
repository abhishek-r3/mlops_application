from azureml.core import Workspace

class AZWorkspace:
    def __init__():
        pass

    def load_azure_workspace(workspace_name, subscription_id, resource_group):
        """
        Function loads the azure work space to the current code environment 
        """
        
        try:
            # loading workspace
            ws = Workspace.get(name = workspace_name, 
                                subscription_id = subscription_id,
                                resource_group = resource_group
                            )
            print("Sucessfully loaded workspace : ", workspace_name)
            return ws

        except Exception as e:
            print("Error while loading the workspace")
            print(e)

