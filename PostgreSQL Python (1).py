import psycopg2

conn = psycopg2.connect(database='max_db', user='postgres', password='')
with conn.cursor() as cur:
    cur.execute('''
    DROP table phone_db;
    DROP table client_db;
    ''')

    def create_db(cursor):
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS client_db (
        client_id SERIAL PRIMARY KEY, 
        name VARCHAR (30),
        surname VARCHAR (30),
        email VARCHAR (40) UNIQUE
        );
        ''')
        conn.commit()

    def create_phone_db(cursor):
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS phone_db (
        phone_id BIGINT,
        client_id INTEGER NOT NULL REFERENCES client_db(client_id)
        );
        ''')
        conn.commit()

    def add_client(cursor, name, surname, email):
        cursor.execute('''
        INSERT INTO client_db (name, surname, email) VALUES (%s, %s, %s);
        ''', (name, surname, email,))
        conn.commit()

    def add_phone(cursor, client_id, phone_id=None):
        cursor.execute('''
        INSERT INTO phone_db (client_id, phone_id) VALUES (%s, %s);''', (client_id, phone_id,))
        conn.commit()

    def data_update(cursor, client_id, name=None, surname=None, email=None):
        cursor.execute('''
        UPDATE client_db SET (name, surname, email) = (%s, %s, %s)
        WHERE client_id = %s;''',
                       (name, surname, email, client_id, ))
        conn.commit()

    def phone_delete(cursor, client_id, phone_id):
        cursor.execute('''
        UPDATE phone_db SET phone_id = NULL
        WHERE client_id = %s AND phone_id = %s;''', (client_id, phone_id, ))
        conn.commit()

    def delete_client(cursor, client_id):
        cursor.execute('''
        DELETE FROM phone_db WHERE client_id = %s;
        DELETE FROM client_db WHERE client_id = %s;''', (client_id, client_id, ))
        conn.commit()

    def find_client(cursor, phone_id=None, name=None, surname=None, email=None):
        if phone_id is not None:
            cursor.execute('''
            SELECT client_id FROM phone_db WHERE phone_id=%s;''',
                           (phone_id, ))
            print(cursor.fetchone())
        else:
            cursor.execute('''
            SELECT client_id FROM client_db WHERE name=%s OR surname=%s OR email=%s;''',
                           (name, surname, email, ))
            print(cursor.fetchone())

    create_db(cur)
    create_phone_db(cur)
    add_client(cur, 'Max', 'Pain', 'pain@mail.ru')
    add_client(cur, 'Oleg', 'Stark', 'oleg@mail.ru')
    add_client(cur, 'Steven', 'King', 'darktower@mail.com')
    add_phone(cur, 1, 89772542356)
    add_phone(cur, 1, 89772544002)
    add_phone(cur, 2)
    add_phone(cur, 3, 89772542350)
    data_update(cur, 2, name='Tony', surname='Stark', email='tony@ya.ru')
    phone_delete(cur, 1, 89772542356)
    # delete_client(cur, 3)
    find_client(cur, email='pain@mail.ru')
    find_client(cur, phone_id=89772542350)

