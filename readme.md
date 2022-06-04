# MlOps with Databicks

## Infrastructure prerequisites

The following infrastructure should be first be put in place. 
  - Four resource groups, 3 for dev/test/prod and one for the cmr
  - In the cmr resource group, add a databricks workspace and a keyvautl
  - In each of the other workpaces, the following should be added:
    - A databricks workspace
    - A Azure machine learning workspace
    - A Storage account

The following RBAC roles should be configured: 
  - The user should have contributor rights on the resource groups.
  - The user should have admin rights in the DevOps repository, as you need to configure 
    the service connections.

## Process

This section describes the process for the developer aiming to build an mlops
Pipeline. It is viewed from a process perspective, to view it from
infrastructural perspective see later sections.

## 01. Local Development

### Prepare the local machine

- Fork the repo to your DevOps project. 
- Clone the repo to your local machine. 
- [OPTIONAL] Create a feature branch called "initial"
- Install the Azure CLI  and install the pip packages DBX and 
- Login into Azure via 
  ```{bash}
  az login
  ```
- Create an install script to authenticate to your Azure Databricks workspace. 
  Example
  ````{bash}
  export DATABRICKS_TOKEN= 
  export DATABRICKS_HOST= 
  `````
- Add this file to the .gitignore, to prevent credentials being added to the repo.

### Configure Databicks 
- First go to the dev Resource group and create a pat token for the install script. (Or use other auth methods ofc)u
- Create a cluster. (For the demo, a single node cluster is sufficient)
- Install mlflow[extras] and pyyaml on the cluster itself. That is, on the cluster install the libraries via the packages tab. 

### Configure the storage account
- Go to the storage account 
- Create blob containers with name data 
- Add the wine dataset csv winequality-red.csv
```{bash}
curl -L https://raw.githubusercontent.com/zygmuntz/wine-quality/master/winequality/winequality-red.csv -o winequality-red.csv
```
- Fetch the storage account key and cluster
- Open databricks and a scrap notebook.
- Mount the storage account, needs to be done once, by running the following snippet, add the details.

```{python}
try: 
    dbutils.fs.mount(
      source = "wasbs://<container>@<storageaccount-name>.blob.core.windows.net",
      mount_point = "/mnt/data",
      extra_configs = {"fs.azure.account.key.<storageaccount-name>.blob.core.windows.net":"<storageaccount-key>"})
except Exception as e:  
    print('mount error:', e)
```

### Run the code from a local machine. 
- Test if the connection to databricks works by running the command 
  ```{bash}
  dbx execute --job=wine-model-train --cluster-name=<your-databricks-cluster-name>
  ```
- If it runs, you are in a position to code locally and run the script on the databricks cluster 
from your local machine.

### Push the code to Master

- Check the new code in git, if you created a separate branch you will have to do a pull request to 
  master from your branch. 

## 02. Deploy to test.
The above step shows how to develop locally and run jobs on the cluster, in this step we will add 
the code to a devops pipeline, configure devops to deploy to test and run the code. 

### Configure Azure ML 
- No configuration needed.

### Configure DevOps
- First fetch the pat token and vault uri. 
- Go to azure devops and create a test-env library for the test environment variables and add the following 
  with the appropriate values linking to the test resource group and test resources.
  ```{bash}
    AKS_CLUSTER=
    DATABRICKS_HOST=
    DATABRICKS_TOKEN=
    MLFLOW_TRACKING_URI=databricks
    AML_WORKSPACE_NAME=
    RESOURCE_GROUP=
    REGISTRY_URI=databricks # databricks://cmr:cmr
    MODEL=sk-learn-linear-reg-model
    DATABRICKS_CLUSTER=
  ```
- Create a service connection with contributor rights on the Resource group.
- Create the azure devops pipeline and check if all variables are properly defined.
- Run the devops pipeline, and check that it works. 

### Check everything works in test. 
- In principal the deploy.py script should create an aks cluster if it does not exist, 
  it might fail on timeout the first run when it creates the cluster, but afterwards it 
  should run. 
- The models should appear in the model registry once the pipeline has ran. 
- Also check that the service got deployed and check that you can send data to the service. 
- NOTE: At this stage the pipeline will fail at the Prod stage 


## 03. Deploy to prod.

This stage is an exact replication of the deployment to test, with the following differences.

### Configure Databricks
- In the Prod workspace create an azure keyvault backed secret scope.
- This can be done by creating 
- Call the secret scope cmr and prefix the secrets with cmr. (See docs.)

### Configure and run the azure pipeline
Create a new library called prod-env with the same set of env variables pointing 
to the prod resources. 
  
  ```{bash}
    AKS_CLUSTER=
    DATABRICKS_HOST=
    DATABRICKS_TOKEN=
    MLFLOW_TRACKING_URI=databricks
    AML_WORKSPACE_NAME=
    RESOURCE_GROUP=
    REGISTRY_URI=databricks://cmr:cmr
    MODEL=sk-learn-linear-reg-model
    DATABRICKS_CLUSTER=
  ```
- Note that in this case we link to the Databricks CMR to log the model. 

### Push code to the release branch [OPTIONAL]
- If you would like to add the prod part to a release branch, add a filter on the stage part for filtering.
- See the azure-pipelines.yaml in wine-project folder for an example.
```{yaml}
  condition: |
    or(
      startsWith(variables['Build.SourceBranch'], 'refs/heads/releases'),
      startsWith(variables['Build.SourceBranch'], 'refs/tags/v')
    )
```
