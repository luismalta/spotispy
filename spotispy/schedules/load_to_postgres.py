from dagster import ScheduleDefinition
from spotispy.jobs.load_to_postgres import load_to_postgres

schedule_load_to_postgres = ScheduleDefinition(job=load_to_postgres, cron_schedule="0 4 * * *")