from dagster import IOManager, io_manager
import psycopg2
import os


class PostgresIOManager(IOManager):
    def handle_output(self, context, obj):
        if obj:
            self.connect_to_postgres_database()
            self.iterate_over_dict_data(obj)
            self.con.close()

    def iterate_over_dict_data(self, obj):
        for table, data in obj.items():
            if isinstance(data, list):
                for inner_data in data:
                   self.upsert(table, inner_data) 
            else:
                self.upsert(table, data)

    def upsert(self, table, data_dict):
        values = []
        for key, value in data_dict.items():
            if table == 'albums':
                print(value)
            value = str(value).replace("'", "''")
            values.append(f"'{value}'")
        values = ', '.join(values)
        query = """
            INSERT
                INTO {}
                VALUES ({})
                ON CONFLICT DO NOTHING
            """.format(table, values)
        self.cur.execute(query)
        self.con.commit()
    
    def connect_to_postgres_database(self):
        self.con = psycopg2.connect(
            host=os.environ['POSTGRES_HOST'],
            database=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD']
        )
        self.cur = self.con.cursor()

    def load_input(self, context):
        return


@io_manager
def postgres_io_manager(init_context):
    return PostgresIOManager()