# MlOps with Databicks

## Infrastructure 
The following infrastructure should be first be put in place. 
- Resource Group (DEV/TEST/Prod)
  - 


## Process

This section describes the process for the developer aiming to build an mlops
Pipeline. It is viewed from a process perspective, to view it from
infrastructural perspective see later sections.

## 01. Local Development

### Prepare the local machine

- Fork the repo to your DevOps project. 
- Clone the repo to your local machine. 
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
- First go to the dev Resource group and create a pat token for the install script. (Or use other auth methods ofc)
- Create a cluster. (For the demo, a single node cluster is sufficient)
- Install mlflow[extras] and pyyaml on the cluster itself. That is, on the cluster install the libraries via the packages tab. 

### Configure the storage account
- Go to the storage account 
- Create blob containers with name data 
- Add the wine dataset csv winequality-red.csv
```{bash}
curl -L https://raw.githubusercontent.com/zygmuntz/wine-quality/master/winequality/winequality-red.csv -o winequality-red.csv
```


### Run the code from a local machine. 
- Test if the connection to databricks works by running the command 
  ```{bash}
  dbx execute --job=wine-model-train --cluster-name=<your-databricks-cluster-name>
  ```
- If it runs, you are in a position to run the 
### Push the code to Master





## 02. Deploy to test.

### Configure Databicks 

### Configure Azure ML 

### Configure DevOps 

### Create the azure pipeline.


## 03. Deploy to prod.

### Configure Databicks 

### Configure Azure ML 

### Configure DevOps 

### Create the azure pipeline.

### Push code to the release branch

