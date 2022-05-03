FROM python:3.7-slim

RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app
RUN mkdir /opt/dagster/app/nhl_elt
RUN mkdir /opt/dagster/app/nhl_dbt

RUN pip install dagster dagit dagster-postgres dagster-dbt dagster-aws dagster-snowflake pandas requests dbt-core dbt-snowflake

COPY nhl_dbt /opt/dagster/app/nhl_dbt/ 
COPY nhl_elt /opt/dagster/app/nhl_elt/
COPY workspace.yaml /opt/dagster/app/

ENV DAGSTER_HOME=/opt/dagster/dagster_home/

COPY dagster.yaml /opt/dagster/dagster_home/

WORKDIR /opt/dagster/app

EXPOSE 3000

ENTRYPOINT ["dagit", "-h", "0.0.0.0", "-p", "3000"]