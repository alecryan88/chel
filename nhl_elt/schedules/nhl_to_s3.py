from dagster import schedule


@schedule(
    cron_schedule="@daily",
    job=job,
    execution_timezone="US/Central",
)
def daily_run(context):
    data = scheduled_execution_time.strftime("%Y-%m-%d")