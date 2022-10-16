# NHL Data Pipeline

An end-to-end data application to ingest NHL game data.

## Overview

The National Hockey League (NHL) provides an open API for requesting game statistics.

In this project, the game data is collected via the NHL Open API and staged in an Amazon S3 bucket. The data is then copied from the S3 bucket into Snowflake where it is transformed using dbt. The pipeline is orchestrated by Dagster running in Docker containers. There are two ways to run the pipeline: 
- Running Application Locally
- Running Application in ECS

## Motivation

The motivation for this project is primarily to gain experience using Dagster, dbt, AWS & Snowflake. A secondary goal of the project is to showcase SQL and Tableau proficiency. 

## Architecture
<img src="https://github.com/alecryan88/chel/blob/main/images/workflow.png" width=100% height=70%>

## Setup
There is some initial setup required regardless of the method of deployment: 
1. Create Snowlake Warehouse
2. Create S3 bucket
3. Create Postgres DB 
4. Add the variables to the dev.env file that will be persisted into the containers: 

First create the file: 
```sh
touch dev.env
```
You will then need to add the following variables to run the application in either ECS or locally: 

```sh
DAGSTER_PG_USERNAME=
DAGSTER_PG_PASSWORD=
DAGSTER_PG_DB=
DAGSTER_PG_HOST=

AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1

RAW_DATA_BUCKET=
DBT_DOCS_BUCKET=

SNOWFLAKE_ACCOUNT=
SNOWFLAKE_USER=
SNOWFLAKE_PASSWORD=
SNOWFLAKE_WAREHOUSE=
SNOWFLAKE_DATABASE=
SNOWFLAKE_ROLE=
```




## Running Application in ECS

1. [Install Docker](https://docs.docker.com/cloud/ecs-integration/#prerequisites)
2. [Create an AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/)
3. [Install the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
4. [Configure IAM permissions](https://docs.docker.com/cloud/ecs-integration/#requirements)
5. [Create a Snowflake account](https://signup.snowflake.com/)
6. [Create a Docker ECS context](https://docs.docker.com/cloud/ecs-integration/#create-aws-context):
  ```sh
docker context create ecs nhl
  ```
6. [Create ECR Repositories](https://docs.aws.amazon.com/cli/latest/reference/ecr/create-repository.html) for the images:
  ```sh
  aws ecr create-repository --repository-name nhl/dagit
  aws ecr create-repository --repository-name nhl/daemon
  aws ecr create-repository --repository-name nhl/user_code
  ```
7. [Log in to your ECR Registry](https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-cli.html) (ensure that the $AWS_REGION environment variable is set to your registry's AWS region):
  ```sh
  export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --output text | cut -f1)
  export REGISTRY_URL=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
  aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $REGISTRY_URL
  ```

### Build and Push Images

The docker-compose.yaml builds all of it's images from the multi-stage Dockerfile. To expose these images to ECS, we first need to build them and then push them to the ECR Repositories we created. 

1. `docker compose build`
2. `docker compose push`


### Deploying Application 

```sh
docker --context nhl compose --project-name nhl-dagster up
```

## Running Application Locally 
1. [Install Docker](https://docs.docker.com/cloud/ecs-integration/#prerequisites)
2. [Create a Snowflake account](https://signup.snowflake.com/)

### Build Images

For running the application locally, we need to specify the compose file being used with the ```-f``` command. This tells docker to build the images with a specific compose file. For the local implementation, we'll use the docker-compose file below: 
```sh
docker compose -f docker-compose-local.yaml build 
```

### Deploying Application 
Once the images are built, to deploy the application locally we can simply run: 
```sh
docker compose -f docker-compose-local.yaml up
```
