import sqlalchemy
from sqlalchemy_utils import database_exists, create_database
from pprint import pprint

class Sqldb_Musicsite:
    def __init__(self, data_base, user):
        self.data_base = data_base
        self.user = user

    def db_user_create(self):
        db_1 = f'postgresql://postgres:654321@localhost:5432/{self.data_base}'
        engine_1 = sqlalchemy.create_engine(db_1)
        if not database_exists(engine_1.url):
            create_database(engine_1.url)
        print(f"Database '{self.data_base}' created: {database_exists(engine_1.url)}.")
        connection_1 = engine_1.connect()
        try:
            connection_1.execute(f"CREATE USER {self.user} WITH PASSWORD '654321';")
            print(f'User "{self.user}" created.')
        except sqlalchemy.exc.ProgrammingError:
            print(f'User "{self.user}" already exist.')
        connection_1.execute(f"ALTER DATABASE {self.data_base} OWNER TO {self.user};")

    def create_tables(self):
        Sqldb_Musicsite.db_user_create(Sqldb_Musicsite(data_base='sql_db_210522', user='user_210522'))
        sql_table = 'CREATE TABLE IF NOT EXISTS'
        dict_tables = {
            'style_list': ['id SERIAL PRIMARY KEY,', 'style_name VARCHAR(20) NOT NULL', '', ''],
            'singer_list': ['id SERIAL PRIMARY KEY,', 'singer_name VARCHAR(40) NOT NULL', '', ''],
            'style_singer': ['id SERIAL PRIMARY KEY,', 'style_id INTEGER NOT NULL REFERENCES style_list(id),',
                             'singer_id INTEGER NOT NULL REFERENCES singer_list(id)', ''],
            'album_list': ['id SERIAL PRIMARY KEY,', 'album_name VARCHAR(40) NOT NULL,',
                           'release_year INTEGER CHECK(release_year>=1900 AND release_year<=2022)', ''],
            'singer_album': ['id SERIAL PRIMARY KEY,', 'album_id INTEGER NOT NULL REFERENCES album_list(id),',
                             'singer_id INTEGER NOT NULL REFERENCES singer_list(id)', ''],
            'track_list': ['id SERIAL PRIMARY KEY,', 'track_name VARCHAR(40) NOT NULL,',
                           'track_time INTEGER CHECK(track_time > 0 AND track_time <= 3600),',
                           'album_id INTEGER REFERENCES album_list(id)'],
            'collection': ['id SERIAL PRIMARY KEY,', 'collection_name VARCHAR(40) NOT NULL,',
                           'collection_year INTEGER CHECK(collection_year>=1900 AND collection_year<=2022)', ''],
            'collection_track': ['id SERIAL PRIMARY KEY,', 'collection_id INTEGER NOT NULL REFERENCES collection(id),',
                                 'track_id INTEGER NOT NULL REFERENCES track_list(id)', '']
        }
        db_2 = f'postgresql://{self.user}:654321@localhost:5432/{self.data_base}'
        engine_2 = sqlalchemy.create_engine(db_2)
        connection_2 = engine_2.connect()

        for tbl_name, tbl_col in dict_tables.items():
            if tbl_name == 'style_list' or tbl_name == 'singer_list':
                req = f"{sql_table} {tbl_name} ({tbl_col[0]} {tbl_col[1]});"
            elif tbl_name == 'track_list':
                req = f"{sql_table} {tbl_name} ({tbl_col[0]} {tbl_col[1]} {tbl_col[2]} {tbl_col[3]});"
            else:
                req = f"{sql_table} {tbl_name} ({tbl_col[0]} {tbl_col[1]} {tbl_col[2]});"
            connection_2.execute(req)
            print(f"Request is being made to create a table:\n{req}")


if __name__ == '__main__':
    Sqldb_Musicsite.create_tables(Sqldb_Musicsite('sql_db_210522', 'user_210522'))