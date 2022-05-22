import sqlalchemy
from sqlalchemy_utils import database_exists, create_database
from pprint import pprint

class Sqldb_Musicsite:
    def __init__(self, data_base, user):
        self.data_base = data_base
        self.user = user

    # Текстовый файл с паролем, в учебных целях для "камуфляжа" на Git поменял расширение.
    def sql_psw(self):
        with open('sqlpsw.jpg', 'r') as file:
            psw = file.read().strip()
        return psw

    def db_user_create(self):
        pswd = Sqldb_Musicsite.sql_psw(Sqldb_Musicsite(data_base='sql_db_210522', user='user_210522'))
        db = f'postgresql://postgres:{pswd}@localhost:5432/{self.data_base}'
        engine = sqlalchemy.create_engine(db)
        if not database_exists(engine.url):
            create_database(engine.url)
        print(f"Database '{self.data_base}' created: {database_exists(engine.url)}.")
        connection = engine.connect()
        try:
            connection.execute(f"CREATE USER {self.user} WITH PASSWORD '{pswd}';")
            print(f'User "{self.user}" created.')
        except sqlalchemy.exc.ProgrammingError:
            print(f'User "{self.user}" already exist.')
        connection.execute(f"ALTER DATABASE {self.data_base} OWNER TO {self.user};")

    def db_connect(self):
        Sqldb_Musicsite.db_user_create(Sqldb_Musicsite(data_base='sql_db_210522', user='user_210522'))
        pswd = Sqldb_Musicsite.sql_psw(Sqldb_Musicsite)
        user_db = f'postgresql://{self.user}:{pswd}@localhost:5432/{self.data_base}'
        main_engine = sqlalchemy.create_engine(user_db)
        connect = main_engine.connect()
        return connect

    def create_tables(self):
        connect = Sqldb_Musicsite.db_connect(Sqldb_Musicsite(data_base='sql_db_210522', user='user_210522'))
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
        for tbl_name, tbl_col in dict_tables.items():
            if tbl_name == 'style_list' or tbl_name == 'singer_list':
                req = f"{sql_table} {tbl_name} ({tbl_col[0]} {tbl_col[1]});"
            elif tbl_name == 'track_list':
                req = f"{sql_table} {tbl_name} ({tbl_col[0]} {tbl_col[1]} {tbl_col[2]} {tbl_col[3]});"
            else:
                req = f"{sql_table} {tbl_name} ({tbl_col[0]} {tbl_col[1]} {tbl_col[2]});"
            connect.execute(req)
            print(f"Request is being made to create a table:\n{req}")

    def insert_tabvalues(self):
        Sqldb_Musicsite.create_tables(Sqldb_Musicsite('sql_db_210522', 'user_210522'))
        connect = Sqldb_Musicsite.db_connect(Sqldb_Musicsite(data_base='sql_db_210522', user='user_210522'))
        req = ''
        count = 0
        with open('Script_Insert_SQL_190522.sql', 'r') as file:
            string_list = file.readlines()
        for index in range(1, len(string_list) + 2):
            if index % 3 != 0:
                req += f' {string_list[index - 1].strip()}'
            else:
                count += 1
                connect.execute(req.strip())
                print(f"String №{count}. Insert data values in a table: {req.strip()}")
                req = ''

    def select_tabdata(self):
        connect = Sqldb_Musicsite.db_connect(Sqldb_Musicsite(data_base='sql_db_210522', user='user_210522'))
        req = ''
        count_req = 0
        with open('Script_SELECT_SQL_200522.sql', 'r') as file:
            string_list = file.readlines()
        print('*' * 67, 'EXECUTIVE PART', '*' * 67)
        for index in range(1, len(string_list) + 2):
            if index % 3 != 0:
                req += f' {string_list[index - 1].strip()}'
            else:
                count_req += 1
                sel = connect.execute(req.strip()).fetchall()
                print(f"Task №{count_req}. --- {req.strip()}")
                print(f'The selection result №{count_req} is:\n{sel}', '\n', '*' * 150)
                req = ''

if __name__ == '__main__':
    # Sqldb_Musicsite.insert_tabvalues(Sqldb_Musicsite('sql_db_210522', 'user_210522'))
    Sqldb_Musicsite.select_tabdata(Sqldb_Musicsite('sql_db_210522', 'user_210522'))