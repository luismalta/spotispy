from dagster import job
from spotispy.ops.sentinel import get_current_playback


@job
def load_current_playback():
    get_current_playback()
