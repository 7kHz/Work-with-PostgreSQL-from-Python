import psycopg2

with psycopg2.connect(database='max_db', user='postgres', password='Pg19cska114') as connect:

    def drop_table(conn):
        with conn.cursor() as cur:
            cur.execute('''
            DROP table phone_db;
            DROP table client_db;
            ''')

    def create_db(conn):
        with conn.cursor() as cur:
            cur.execute('''
            CREATE TABLE IF NOT EXISTS client_db (
            client_id SERIAL PRIMARY KEY, 
            name VARCHAR (30) NOT NULL,
            surname VARCHAR (30) NOT NULL,
            email VARCHAR (40) UNIQUE
            );
            ''')

    def create_phone_db(conn):
        with conn.cursor() as cur:
            cur.execute('''
            CREATE TABLE IF NOT EXISTS phone_db (
            phone_id BIGINT,
            client_id INTEGER NOT NULL REFERENCES client_db(client_id)
            );
            ''')

    def add_client(conn, name, surname, email):
        with conn.cursor() as cur:
            cur.execute('''
            INSERT INTO client_db (name, surname, email) VALUES (%s, %s, %s);
            ''', (name, surname, email,))

    def add_phone(conn, client_id, phone_id=None):
        with conn.cursor() as cur:
            cur.execute('''
            INSERT INTO phone_db (client_id, phone_id) VALUES (%s, %s);''', (client_id, phone_id,))

    def data_update(conn, client_id, name=None, surname=None, email=None):
        with conn.cursor() as cur:
            if name is not None:
                cur.execute('''
                UPDATE client_db SET name = %s
                WHERE client_id = %s''',
                            (name, client_id))
            if surname is not None:
                cur.execute('''
                UPDATE client_db SET surname = %s
                WHERE client_id = %s''',
                            (surname, client_id))
            if email is not None:
                cur.execute('''
                UPDATE client_db SET email = %s
                WHERE client_id = %s''',
                            (email, client_id))

    def phone_delete(conn, client_id, phone_id):
        with conn.cursor() as cur:
            cur.execute('''
            UPDATE phone_db SET phone_id = NULL
            WHERE client_id = %s AND phone_id = %s;''', (client_id, phone_id,))

    def delete_client(conn, client_id):
        with conn.cursor() as cur:
            cur.execute('''
            DELETE FROM phone_db WHERE client_id = %s;
            DELETE FROM client_db WHERE client_id = %s;''', (client_id, client_id,))

    def find_client(conn, phone_id=None, name=None, surname=None, email=None):
        with conn.cursor() as cur:
            if phone_id is not None:
                cur.execute('''
                SELECT client_id FROM phone_db WHERE phone_id=%s;''',
                            (phone_id,))
                print(cur.fetchone())
            if name is not None:
                cur.execute('''
                SELECT client_id FROM client_db WHERE name=%s;''',
                            (name,))
                print(cur.fetchone())
            if surname is not None:
                cur.execute('''
                SELECT client_id FROM client_db WHERE surname=%s;''',
                            (surname,))
                print(cur.fetchone())
            if email is not None:
                cur.execute('''
                SELECT client_id FROM client_db WHERE email=%s;''',
                            (email,))
                print(cur.fetchone())

    drop_table(connect)
    create_db(connect)
    create_phone_db(connect)
    add_client(connect, 'Max', 'Pain', 'pain@mail.ru')
    add_client(connect, 'Tony', 'Stark', 'stark@mail.ru')
    add_client(connect, 'Steven', 'King', 'darktower@mail.com')
    add_client(connect, 'Bruce', 'Wayne', 'batman@ya.ru')
    add_phone(connect, 1, 89772542356)
    add_phone(connect, 1, 89772544002)
    add_phone(connect, 2, 89771000200)
    add_phone(connect, 3, 89772542350)
    data_update(connect, 2, name='Dan', surname='Braun')
    phone_delete(connect, 1, 89772542356)
    # delete_client(connect, 3)
    find_client(connect, name='Steven')
    find_client(connect, phone_id=89771000200)
