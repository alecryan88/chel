from dagster import DailyPartitionsDefinition

#Partition def to get used in multiple assets
daily_partitions_def = DailyPartitionsDefinition(start_date="2020-01-01")