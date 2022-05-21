import sqlalchemy
from sqlalchemy_utils import database_exists, create_database
from pprint import pprint

def db_user_create(data_base='sql_db_210522', user='user_210522'):
    db_1 = f'postgresql://postgres:654321@localhost:5432/{data_base}'
    engine_1 = sqlalchemy.create_engine(db_1)
    if not database_exists(engine_1.url):
        create_database(engine_1.url)
    print(f"Database '{data_base}' created: {database_exists(engine_1.url)}.")
    connection_1 = engine_1.connect()
    try:
        connection_1.execute(f"CREATE USER {user} WITH PASSWORD '654321';")
        print(f'User "{user}" created.')
    except sqlalchemy.exc.ProgrammingError:
        print(f'User "{user}" already exist.')
    connection_1.execute(f"ALTER DATABASE {data_base} OWNER TO {user};")
    return data_base, user

def create_tables():
    db_user_create()
    sql_table = 'CREATE TABLE IF NOT EXISTS'
    dict_tables = {
        'style_list' : {'id' : ['SERIAL', 'PRIMARY KEY', ','], 'style_name' : ['VARCHAR(20)', 'NOT NULL', '']},
        'singer_list' : {'id' : ['SERIAL', 'PRIMARY KEY', ','], 'singer_name' : ['VARCHAR(40)', 'NOT NULL', '']},
        'style_singer' : {'id' : ['SERIAL', 'PRIMARY KEY', ','], 'style_id' : ['INTEGER', 'NOT NULL',
                          'REFERENCES style_list(id),'], 'singer_id' : ['INTEGER', 'NOT NULL',
                          'REFERENCES singer_list(id)']
                          },
        'album_list': {'id' : ['SERIAL', 'PRIMARY KEY', ','], 'album_name' : ['VARCHAR(40)', 'NOT NULL', ','],
                       'release_year' : ['INTEGER', 'CHECK(release_year>=1900 AND release_year<=2022)', '']
                       },
        'singer_album': {'id' : ['SERIAL', 'PRIMARY KEY', ','], 'album_id' : ['INTEGER', 'NOT NULL',
                         'REFERENCES album_list(id),'], 'singer_id' : ['INTEGER', 'NOT NULL',
                         'REFERENCES singer_list(id)']
                         },
        'track_list': {'id' : ['SERIAL', 'PRIMARY KEY', ','], 'track_name' : ['VARCHAR(40)', 'NOT NULL', ','],
                       'track_time' : ['INTEGER', 'CHECK(track_time > 0 AND track_time <= 3600)', ','],
                       'album_id' : ['INTEGER', 'REFERENCES album_list(id)', '']
                       },
        'collection': {'id' : ['SERIAL', 'PRIMARY KEY', ','], 'collection_name' : ['VARCHAR(40)', 'NOT NULL', ','],
                       'collection_year' : ['INTEGER', 'CHECK(collection_year>=1900 AND collection_year<=2022)', '']
                       },
        'collection_track': {'id' : ['SERIAL', 'PRIMARY KEY', ','], 'collection_id' : ['INTEGER', 'NOT NULL',
                             'REFERENCES collection(id)'], 'track_id' : ['INTEGER', 'NOT NULL',
                             'REFERENCES track_list(id)']
                             }
    }



if __name__ == '__main__':
    create_tables()
