# How to train and deploy in Azure ML

This project shows how to train a Fashion MNIST model with an Azure ML job, and how to deploy it using an online managed endpoint. It uses MLflow for tracking and model representation.


## Setup

If you have access to GitHub Codespaces, click on the "Code" button in this GitHub repo, select the "Codespaces" tab, and then click on "New codespace".

Alternatively, you can set up your local machine using the following steps.

Install conda environment:

```
conda env create -f environment.yml
```

Activate conda environment:

```
conda activate aml-command-output
```


## Run the notebook locally

Get familiar with the code in the experiment.ipynb notebook, and run it. The notebook accomplishes the following:

* Downloads the data into the "data" folder.
* Trains a model with that data, and saves the trained model in the "model_from_notebook" folder.
* Tests the trained model with test data.
* Makes a prediction using the test image.
* Creates json and csv versions of the test image, which we'll use to make predictions with mlflow and Azure ML. (These files are checked in with the project, but I included the code here so you can see how they were generated.)
 

## Train and predict locally

* Run train.py by pressing F5.
* Analyze the metrics logged in the "mlruns" directory with the following command:

```
mlflow ui
```

* Make a local prediction using the trained mlflow model. You can use either csv or json files:

```
mlflow models predict --model-uri "aml-train-deploy-output/trained_model_output" --input-path "aml-train-deploy-output/test_image/predict_image.csv" --content-type csv
mlflow models predict --model-uri "aml-train-deploy-output/trained_model_output" --input-path "aml-train-deploy-output/test_image/predict_image.json" --content-type json
```


## Train and deploy in the cloud

```
cd aml-command-output
```

Create the compute cluster.

```
az ml compute create -f cloud/cluster-cpu.yml 
```

Create the dataset.

```
az ml data create -f cloud/data.yml 
```

Run the training job. Go to the Azure ML Studio and wait until the Experiment completes.

```
run_id=$(az ml job create -f cloud/job.yml --query name -o tsv)
```

You don't need to download the trained model, but here's how you would do it if you wanted to:

```
az ml job download --name $run_id --output-name "trained_model_output"
```

Create the Azure ML model from the output.

```
az ml model create --name model-command-output --version 1 --path "azureml://jobs/$run_id/outputs/trained_model_output" --type mlflow_model
```

Create the endpoint.

```
az ml online-endpoint create -f cloud/endpoint.yml
az ml online-deployment create -f cloud/deployment.yml --all-traffic
```

Invoke the endpoint.

```
az ml online-endpoint invoke --name endpoint-command-output --request-file test_image/predict_image_azureml.json
```