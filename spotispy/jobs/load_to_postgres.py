from dagster import job, fs_io_manager
from more_itertools import last
from spotispy.ops.load_to_postgres import get_last_playback_history_from_postgres, get_history_from_firebase, insert_into_postgres
from spotispy.io_managers.postgres import postgres_io_manager


@job(resource_defs={'postgres_io_manager': postgres_io_manager})
def load_to_postgres():
    last_playback_history = get_last_playback_history_from_postgres()
    get_history_from_firebase(last_playback_history).map(insert_into_postgres)

if __name__ == "__main__":
    result = load_to_postgres.execute_in_process()
