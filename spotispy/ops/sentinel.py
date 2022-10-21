import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import CacheHandler
from dagster import op, Out
import json
import os


class CacheEnvHandler(CacheHandler):
    def __init__(self):
        cache = os.environ["SPOTIFY_CACHE"]
        if cache:
            self.cache = cache
        else:
            raise NotImplementedError()

    def get_cached_token(self):
        return json.loads(self.cache)

    def save_token_to_cache(self, token_info):
        pass

cache_handler = CacheEnvHandler()

@op(out=Out(io_manager_key="firebase_io_manager"))
def get_current_playback():
    scope = ["user-read-currently-playing", "user-read-playback-state"]
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_handler=cache_handler))
    current_playback = sp.current_playback()
    return current_playback
