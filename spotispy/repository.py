from dagster import repository

from spotispy import jobs, schedules


@repository
def spotispy():
    return [
        jobs.sentinel.load_current_playback,
        schedules.sentinel.schedule_current_playback
        ]
