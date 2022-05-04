FROM python:3.7-slim

RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app
RUN mkdir /opt/dagster/app/nhl_dagster
RUN mkdir /opt/dagster/app/nhl_dbt

COPY requirements.txt /opt/dagster/app
COPY nhl_dbt /opt/dagster/app/nhl_dbt/ 
COPY nhl_dagster /opt/dagster/app/nhl_dagster/
COPY workspace.yaml /opt/dagster/app/

ENV DAGSTER_HOME=/opt/dagster/dagster_home/

COPY dagster.yaml /opt/dagster/dagster_home/

WORKDIR /opt/dagster/app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 3000

ENTRYPOINT ["dagit", "-h", "0.0.0.0", "-p", "3000"]