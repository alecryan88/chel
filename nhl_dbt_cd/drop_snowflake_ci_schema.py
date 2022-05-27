import snowflake.connector
import os

#Connect to Snowflake
conn = snowflake.connector.connect(
    user=os.environ['SNOWFLAKE_USER'],
    password=os.environ['SNOWFLAKE_PASSWORD'],
    account=os.environ['SNOWFLAKE_ACCOUNT'],
    session_parameters={
        'QUERY_TAG': 'dbt_CI_CD',
    }
)

#Specify database where CI schema is located
conn.cursor().execute(f"""USE DATABASE {os.environ['SNOWFLAKE_DB']};""")


#Drop schema created by CI process
conn.cursor().execute(f"""DROP SCHEMA IF EXISTS {os.environ['CI_SCHEMA']} CASCADE ;""")

print(f"Deleted schema {os.environ['CI_SCHEMA']} from {os.environ['SNOWFLAKE_DB']} succesfully.")




#Drop schema if exists 
    #If not then do something ...