import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dagster import op
import requests

@op
def get_current_playback():
    scope = ["user-read-currently-playing", "user-read-playback-state"]
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    current_playback = sp.current_playback()
    return current_playback