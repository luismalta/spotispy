from dagster import IOManager, io_manager
import firebase_admin
from firebase_admin import credentials, firestore

class FirebaseIOManager(IOManager):
    def handle_output(self, context, obj):
        if obj:
            self.connect_to_firebase_database()
            if self.track_is_playing(obj) and self.track_has_changed(obj):
                self.playback_history_collection.add(obj)
    
    def connect_to_firebase_database(self):
        cred = credentials.Certificate("firebase_account_key.json")
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        self.playback_history_collection = db.collection('playback_history')

    def track_is_playing(self, obj):
        return obj.get('is_playing', False)
    
    def track_has_changed(self, obj):
        last_history = self.playback_history_collection.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1).get()
        if last_history: 
            return last_history[0].get('item').get('id') != obj.get('item').get('id')
        else:
            return True

    def load_input(self, context):
        return


@io_manager
def firebase_io_manager(init_context):
    return FirebaseIOManager()