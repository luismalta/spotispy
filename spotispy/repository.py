from dagster import repository

from spotispy import jobs, schedules


@repository
def spotispy():
    return [
        jobs.sentinel.load_current_playback,
        jobs.load_to_postgres.load_to_postgres,
        schedules.sentinel.schedule_current_playback,
        schedules.load_to_postgres.schedule_load_to_postgres,
        ]
