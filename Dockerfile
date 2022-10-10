FROM python:3.7-slim as dagster

RUN apt-get update && apt-get upgrade -yqq
RUN apt-get install git -y

ENV DAGSTER_HOME=/opt/dagster/dagster_home
RUN mkdir -p $DAGSTER_HOME

COPY dagster.yaml  $DAGSTER_HOME
COPY workspace.yaml $DAGSTER_HOME
COPY nhl_dbt $DAGSTER_HOME/nhl_dbt/
COPY nhl_dagster $DAGSTER_HOME/nhl_dagster/
COPY requirements.txt $DAGSTER_HOME

WORKDIR $DAGSTER_HOME

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Dagit
FROM dagster as dagit

# User Code gRPC Server
# You can either include all of your repositories in this
# stage or you can create multiple stages that each use
# the same base - one for each repository.
FROM dagster as user_code