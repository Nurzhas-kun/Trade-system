import pymysql

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'skins'
}

def get_db_connection():
    return pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        cursorclass=pymysql.cursors.DictCursor
    )
