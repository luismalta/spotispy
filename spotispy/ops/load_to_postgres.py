import os
import psycopg2
import firebase_admin

from datetime import datetime
from firebase_admin import credentials, firestore
from dagster import op, Out, DynamicOut, DynamicOutput

def connect_to_postgres_database():
    con = psycopg2.connect(
        host=os.environ['POSTGRES_HOST'],
        database=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD']
    )
    return con

def connect_to_firebase():
    certificate_path = os.environ['FIREBASE_CERTIFICATE_PATH']
    cred = credentials.Certificate(certificate_path)
    firebase_admin.initialize_app(cred)
    return firestore.client()

def parse_date(date_string, release_date_precision):
    if release_date_precision == 'year':
        format = '%Y'
    elif release_date_precision == 'month':
        format = '%Y-%m'
    elif release_date_precision == 'day':
        format = '%Y-%m-%d'
    return datetime.strptime(date_string, format)

@op
def get_last_playback_history_from_postgres():
    connection = connect_to_postgres_database();
    cur = connection.cursor()
    query = """
        select 
            playback_datetime 
        from 
            playback_history 
        order by 
            playback_datetime desc
        limit 1;
    """
    cur.execute(query)
    last_history_date = cur.fetchone()
    connection.commit()
    connection.close()
    print(last_history_date)
    if last_history_date:
        print(last_history_date)
        return last_history_date[0]

@op(out=DynamicOut())
def get_history_from_firebase(last_history_date):
    print(last_history_date)
    db = connect_to_firebase()
    playback_history_collection = db.collection('playback_history')
    if last_history_date:
        last_history_date = last_history_date.timestamp() * 1000
        print(last_history_date)
        historys = playback_history_collection.where('timestamp', '>', last_history_date).get()
    else:
        historys = playback_history_collection.get()
    for history in historys:
        yield DynamicOutput(history.to_dict(), mapping_key=str(history.get('timestamp')))

@op(out=Out(io_manager_key="postgres_io_manager"))
def insert_into_postgres(history):
    data = {}

    item = history.get('item')
    device = history.get('device')

    data['albums'] = {
        'id': item.get('album').get('id'),
        'name': item.get('album').get('name'),
        'release_date': parse_date(
            item.get('album').get('release_date'),
            item.get('album').get('release_date_precision')
        ),
        'total_tracks': item.get('album').get('total_tracks'),
    }

    data['devices'] = {
        'id': device.get('id'),
        'name': device.get('name'),
        'device_type': device.get('type')
    }

    data['tracks'] = {
        'id': item.get('id'),
        'name': item.get('name'),
        'explicit': item.get('explicit'),
        'duration_ms': item.get('duration_ms'),
        'album_id': item.get('album').get('id'),
    }

    data['artists'] = []
    data['tracks_artists'] = []
    data['tracks_albums'] = []

    for artist_item in item.get('artists'):
        data['artists'].append({
            'id': artist_item.get('id'),
            'name': artist_item.get('name'),
        })
    
        data['tracks_artists'].append({
            'track_id': item.get('id'),
            'artist_id': artist_item.get('id'),
        })

        data['tracks_albums'].append({
            'track_id': item.get('id'),
            'album_id': item.get('album').get('id'),
        })
    
    data['playback_history'] = {
        'track_id': item.get('id'),
        'device_id': device.get('id'),
        'playback_datetime': datetime.fromtimestamp(history.get('timestamp') / 1000.0),
    }

    return data


