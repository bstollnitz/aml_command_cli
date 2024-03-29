# How to train and deploy in Azure ML

This project shows how to train a Fashion MNIST model with an Azure ML job, and how to deploy it using an online managed endpoint. It uses the Azure ML CLI, and MLflow for tracking and model representation.


## Blog post

To learn more about the code in this repo, check out the accompanying blog post: https://bea.stollnitz.com/blog/aml-command/


## Setup

* You need to have an Azure subscription. You can get a [free subscription](https://azure.microsoft.com/en-us/free) to try it out.
* Create a [resource group](https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-portal).
* Create a new machine learning workspace by following the "Create the workspace" section of the [documentation](https://docs.microsoft.com/en-us/azure/machine-learning/quickstart-create-resources). Keep in mind that you'll be creating a "machine learning workspace" Azure resource, not a "workspace" Azure resource, which is entirely different!
* Install the Azure CLI by following the instructions in the [documentation](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli).
* Install the ML extension to the Azure CLI by following the "Installation" section of the [documentation](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-configure-cli).
* Install and activate the conda environment by executing the following commands:
```
conda env create -f environment.yml
conda activate aml_command_cli
```
* Within VS Code, go to the Command Palette clicking "Ctrl + Shift + P," type "Python: Select Interpreter," and select the environment that matches the name of this project.
* In a terminal window, log in to Azure by executing `az login`. 
* Set your default subscription by executing `az account set -s "<YOUR_SUBSCRIPTION_NAME_OR_ID>"`. You can verify your default subscription by executing `az account show`, or by looking at `~/.azure/azureProfile.json`.
* Set your default resource group and workspace by executing `az configure --defaults group="<YOUR_RESOURCE_GROUP>" workspace="<YOUR_WORKSPACE>"`. You can verify your defaults by executing `az configure --list-defaults` or by looking at `~/.azure/config`.
* You can now open the [Azure Machine Learning studio](https://ml.azure.com/), where you'll be able to see and manage all the machine learning resources we'll be creating.
* Optionally, you can install the [Azure Machine Learning extension for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.vscode-ai). Log in by clicking on "Azure" in the left-hand menu, and then clicking on "Sign in to Azure."


## Train and predict locally

* Under "Run and Debug" on VS Code's left navigation, choose the "Train locally" run configuration and press F5.
* Analyze the metrics logged in the "mlruns" directory with the following command:

```
mlflow ui
```

* Navigate to the root of this repo in your terminal.
* Make a local prediction using the trained mlflow model. You can use either csv or json files:

```
cd aml_command_cli
mlflow models predict --model-uri "model" --input-path "test_data/images.csv" --content-type csv --env-manager local
mlflow models predict --model-uri "model" --input-path "test_data/images.json" --content-type json --env-manager local
```


## Train and deploy in the cloud

Create the compute cluster.

```
az ml compute create -f cloud/cluster-cpu.yml 
```

Create the dataset.

```
az ml data create -f cloud/data.yml 
```

Run the training job.

```
run_id=$(az ml job create -f cloud/job.yml --query name -o tsv)
```

Go to the Azure ML Studio and wait until the Job completes.
Create the Azure ML model from the output.

```
az ml model create --name model-command-cli --path "azureml://jobs/$run_id/outputs/model" --type mlflow_model
```

Look for the job in the [Azure ML Studio](https://ml.azure.com/) and wait for it to complete.

You don't need to download the trained model, but here's how you would do it if you wanted to:

```
az ml job download --name $run_id --output-name "model"
```

Create the endpoint.

```
az ml online-endpoint create -f cloud/endpoint.yml
az ml online-deployment create -f cloud/deployment.yml --all-traffic
```

Invoke the endpoint.

```
az ml online-endpoint invoke --name endpoint-command-cli --request-file test_data/images_azureml.json
```

Cleanup the endpoint, to avoid getting charged.

```
az ml online-endpoint delete --name endpoint-command-cli -y
```


## Related resources
* [YAML schema for Command Job](https://docs.microsoft.com/en-us/azure/machine-learning/reference-yaml-job-command?WT.mc_id=aiml-67316-bstollnitz)
* [az ml job commands](https://docs.microsoft.com/en-us/cli/azure/ml/job?view=azure-cli-latest#az-ml-job-create?WT.mc_id=aiml-67316-bstollnitz)
* [Output formats for Azure CLI commands](https://docs.microsoft.com/en-us/cli/azure/format-output-azure-cli?WT.mc_id=aiml-67316-bstollnitz)
