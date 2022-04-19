from dagster_aws.s3.sensor import get_s3_keys


@sensor(job=my_job)
def my_s3_sensor(context):
    new_s3_keys = get_s3_keys("my_s3_bucket", since_key=context.last_run_key)
    if not new_s3_keys:
        yield SkipReason("No new s3 files found for bucket my_s3_bucket.")
        return
    for s3_key in new_s3_keys:
        yield RunRequest(run_key=s3_key, run_config={})