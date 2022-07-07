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