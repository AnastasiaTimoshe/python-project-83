import psycopg2
from psycopg2.extras import NamedTupleCursor


class DatabaseManager:
    def __init__(self, app):
        self.app = app

    @staticmethod
    def execute_in_db(func):
        """Декоратор для выполнения функций соединения с базой данных."""
        def inner(self, *args, **kwargs):
            with psycopg2.connect(self.app.config['DATABASE_URL']) as conn:
                with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
                    result = func(self, cursor=cursor, *args, **kwargs)
                    conn.commit()
                    return result
        return inner

    @staticmethod
    def with_commit(func):
        def inner(self, *args, **kwargs):
            try:
                with psycopg2.connect(self.app.config['DATABASE_URL']) as conn:
                    cursor = conn.cursor(cursor_factory=NamedTupleCursor)
                    result = func(self, cursor, *args, **kwargs)
                    conn.commit()
                    return result
            except psycopg2.Error as e:
                print(f'Ошибка при выполнении транзакции: {e}')
                raise e
        return inner

    @with_commit
    def insert_url(self, cursor, url):
        cursor.execute("""INSERT INTO urls (name) VALUES (%s)
                       RETURNING *""", (url,))
        url_data = cursor.fetchone()
        return url_data

    @execute_in_db
    def find_url_by_id(self, id, cursor):
        cursor.execute("SELECT * from urls WHERE id=%s", (id,))
        url_id = cursor.fetchone()
        return url_id

    @execute_in_db
    def find_url_by_name(self, name, cursor):
        value = str(name)
        cursor.execute("SELECT * from urls WHERE name=%s", (value,))
        url_id = cursor.fetchone()
        return url_id.id if url_id else None

    @execute_in_db
    def get_all_urls(self, cursor):
        query = '''
            SELECT u.id, u.name, MAX(c.created_at) AS last_checked,
            MAX(c.status_code) AS status_code
            FROM urls u
            LEFT JOIN url_checks c ON u.id = c.url_id
            GROUP BY u.id
            ORDER BY u.created_at DESC
        '''
        cursor.execute(query)
        urls_data = cursor.fetchall()
        return urls_data

    @with_commit
    def add_check(self, cursor, id, result_check):
        cursor.execute(
            '''INSERT INTO url_checks (url_id, status_code, h1, title,
            description)
            VALUES (%s, %s, %s, %s, %s) RETURNING *''',
            (id, result_check['status_code'], result_check['h1'],
             result_check['title'], result_check['description'],)
        )
        checks = cursor.fetchall()
        return checks

    @execute_in_db
    def find_checks_by_id(self, id, cursor):
        value = str(id)
        cursor.execute("SELECT * from url_checks WHERE url_id=%s", (value,))
        checks = cursor.fetchall()
        return checks
