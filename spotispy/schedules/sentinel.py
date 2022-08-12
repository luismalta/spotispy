from dagster import ScheduleDefinition
from spotispy.jobs.sentinel import load_current_playback

schedule_current_playback = ScheduleDefinition(job=load_current_playback, cron_schedule="*/1 * * * *")