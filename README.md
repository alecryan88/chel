# NHL Data Pipeline

An end-to-end data application to ingest NHL game data.

## Overview

The National Hockey League (NHL) provides an open API for requesting game statistics.

In this project, the game data is collected via the NHL Open API and staged in an Amazon S3 bucket. The data is then copied from the S3 bucket into Snowflake where it is transformed using dbt. The pipeline is orchestrated by Dagster running in Docker containers. There are two ways to run the pipeline: 
- Locally using docker containers
- In the cloud, using AWS Elastic Container Service (ECS) . 

## Motivation

The motivation for this project is primarily to gain experience using Apache Airflow, DBT & Snowflake. A secondary goal of the project is to showcase SQL and Tableau proficiency. 


## Architecture

## 🧐 About <a name = "about"></a>

### Prerequisites
What things you need to install the software and how to install them.

## Architecture
<img src="https://github.com/alecryan88/chel/blob/main/images/workflow.png" width=100% height=70%>


## 🚀 Deployment <a name = "deployment"></a>
Add additional notes about how to deploy this on a live system.

## ⛏️ Built Using <a name = "built_using"></a>
- [Dagster](https://dagster.io/) - Orchestration
- [dbt](https://www.getdbt.com/) - Transformation & Documentation
- [Snowflake](https://www.snowflake.com/) - Data Warehouse
- [AWS S3](https://aws.amazon.com/) - Storage
- [GitHub Actions](https://docs.github.com/en/actions) - CI/CD
- [Metabase](https://www.metabase.com/) - Data Viz

## Contents

| Name                     | Description                                                                       |
| ------------------------ | --------------------------------------------------------------------------------- |
| `README.md`              | A description and guide for this code repository                                  |
| `setup.py`               | A build script with Python package dependencies for this code repository          |
| `workspace.yaml`         | A file that specifies the location of the user code for Dagit and the Dagster CLI |
| `nhl_elt/`               | A Python directory that contains code for your Dagster repository                 |
| `nhl_elt_tests/`         | A Python directory that contains tests for `nhl_elt`                              |


## Prerequisites

1. [Install Docker](https://docs.docker.com/cloud/ecs-integration/#prerequisites)
2. [Create an AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/)
3. [Install the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
4. [Configure IAM permissions](https://docs.docker.com/cloud/ecs-integration/#requirements)
5. [Create a Docker ECS context](https://docs.docker.com/cloud/ecs-integration/#create-aws-context):

## Setup
  ```sh
  docker context create ecs dagster-ecs
  ```
6. [Create ECR Repositories](https://docs.aws.amazon.com/cli/latest/reference/ecr/create-repository.html) for our images:
  ```sh
  aws ecr create-repository --repository-name deploy_ecs/dagit
  aws ecr create-repository --repository-name deploy_ecs/daemon
  aws ecr create-repository --repository-name deploy_ecs/user_code
  ```
7. [Log in to your ECR Registry](https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-cli.html) (ensure that the $AWS_REGION environment variable is set to your registry's AWS region):
  ```sh
  export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --output text | cut -f1)
  export REGISTRY_URL=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
  aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $REGISTRY_URL
  ```

## Build and Push Images

Our docker-compose.yaml builds all of its images from local multi-stage Dockerfile. To expose these images to ECS, we first need to build them and then push them to the ECR Repositories we created:

1. `docker compose build`
2. `docker compose push`

## Deploying Dagster

```sh
docker --context dagster-ecs compose --project-name dagster up
```
