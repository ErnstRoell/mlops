from azureml.core import Workspace
from azureml.core.webservice import AciWebservice, Webservice
import uuid
import azureml.core
from azureml.core import Workspace
import os 

# from azureml.core.authentication import AzureCliAuthentication




# cli_auth = AzureCliAuthentication()

# ws = Workspace(subscription_id="d30d76c0-804c-4f4e-ab7b-509d06a49550",
#               resource_group=os.getenv("WORKSPACE_RG"),
#               workspace_name=os.getenv("WORKSPACE_NAME"),
#               auth=cli_auth)


# print("Found workspace {} at location {}".format(ws.name, ws.location))


#######################################

from azureml.core.authentication import ServicePrincipalAuthentication
svc_pr = ServicePrincipalAuthentication(
    tenant_id="72f988bf-86f1-41af-91ab-2d7cd011db47",
    service_principal_id="06ab050f-3848-4e29-a408-c8ba1a3d3716",
    service_principal_password="zn~8Q~2MLMrp-kvMsdDcGZaSjkBDDMOpjiLQpb8s")


ws = Workspace(subscription_id="d30d76c0-804c-4f4e-ab7b-509d06a49550",
              resource_group=os.getenv("WORKSPACE_RG"),
              workspace_name=os.getenv("WORKSPACE_NAME"),
              auth=svc_pr)



print("Found workspace {} at location {}".format(ws.name, ws.location))

from azureml.core import Workspace
from azureml.core.compute import AksCompute, ComputeTarget
from azureml.core.webservice import Webservice, AksWebservice
from azureml.core.model import Model

import azureml.core
from azureml.core import Environment
from azureml.core.conda_dependencies import CondaDependencies 
import os

#Register the model
from azureml.core.model import Model
model = Model(ws, 'sk-learn-linear-reg-model')

print(model.name, model.description, model.version)

from azureml.core import Environment
from azureml.core.conda_dependencies import CondaDependencies 

conda_deps = CondaDependencies.create(conda_packages=['numpy','scikit-learn==0.24.1','scipy'], pip_packages=['azureml-defaults', 'inference-schema'])
myenv = Environment(name='myenv')
myenv.python.conda_dependencies = conda_deps

from azureml.core.model import InferenceConfig

inf_config = InferenceConfig(entry_script='score.py', environment=myenv)

from azureml.core.compute import ComputeTarget
from azureml.core.compute_target import ComputeTargetException

# Choose a name for your AKS cluster
aks_name = os.getenv("AKS_CLUSTER")

# Verify that cluster does not exist already
try:
    aks_target = ComputeTarget(workspace=ws, name=aks_name)
    print('Found existing cluster, use it.')
except ComputeTargetException:
    # Use the default configuration (can also provide parameters to customize)
    prov_config = AksCompute.provisioning_configuration()

    # Create the cluster
    aks_target = ComputeTarget.create(workspace = ws, 
                                    name = aks_name, 
                                    provisioning_configuration = prov_config)

# Set the web service configuration (using default here)
aks_config = AksWebservice.deploy_configuration()

aks_service_name =f'aks-service-{str(uuid.uuid4())[:5]}'

aks_service = Model.deploy(workspace=ws,
                           name=aks_service_name,
                           models=[model],
                           inference_config=inf_config,
                           deployment_config=aks_config,
                           deployment_target=aks_target)

aks_service.wait_for_deployment(show_output = True)
print(aks_service.state)
