FROM mcr.microsoft.com/azureml/curated/pytorch-1.10-ubuntu18.04-py38-cuda11-gpu:22

COPY conda-mlflow.yml .
RUN conda env update -p $AZUREML_CONDA_ENVIRONMENT_PATH -f conda-mlflow.yml
