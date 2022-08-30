from dagster import IOManager, io_manager
import psycopg2


class SentinelIOManager(IOManager):
    def handle_output(self, context, obj):
        querry = context.config.get("querry")

        con = psycopg2.connect(
            host='dagster-postgres',
            database='spotispy',
            user='postgres',
            password='secret'
        )
        cur = con.cursor()

        cur.execute(querry)
        con.commit()
        con.close()

    def load_input(self, context):
        return


@io_manager
def sentinel_io_manager(init_context):
    return SentinelIOManager()