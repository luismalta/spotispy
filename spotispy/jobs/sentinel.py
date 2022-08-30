from dagster import job
from spotispy.ops.sentinel import get_current_playback
from spotispy.io_managers.firebase import firebase_io_manager


@job(resource_defs={'firebase_io_manager': firebase_io_manager})
def load_current_playback():
    get_current_playback()

if __name__ == "__main__":
    result = load_current_playback.execute_in_process()
