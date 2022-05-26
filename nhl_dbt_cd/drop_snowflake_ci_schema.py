import snowflake.connector
import os

#Connect to Snowflake
conn = snowflake.connector.connect(
    user=os.environ['SNOWFLAKE_USER'],
    password=os.environ['SNOWFLAKE_PASSWORD'],
    account=os.environ['SNOWFLAKE_ACCOUNT'],
    session_parameters={
        'QUERY_TAG': 'EndOfMonthFinancials',
    }
)

#Drop schema created by CI process
con.cursor().execute(f"DROP SCHEMA {os.environ['CI_SCHEMA']} ")