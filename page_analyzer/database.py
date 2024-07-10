import psycopg2
from psycopg2.extras import NamedTupleCursor, RealDictCursor
from datetime import date
from contextlib import contextmanager


@contextmanager
def get_cursor(conn, cursor_factory=NamedTupleCursor):
    try:
        with conn.cursor(cursor_factory=cursor_factory) as cur:
            yield cur
    except psycopg2.DatabaseError as e:
        conn.rollback()
        raise e
    else:
        conn.commit()


def create_connection(database_url):
    return psycopg2.connect(database_url)


def get_url_by_id(conn, id):
    with get_cursor(conn) as cur:
        cur.execute('SELECT * FROM urls WHERE id = %s;', (id,))
        return cur.fetchone()


def get_url_by_name(conn, url):
    with get_cursor(conn) as cur:
        cur.execute('SELECT * FROM urls WHERE name = %s;', (url,))
        return cur.fetchone()


def get_url_checks(conn, id):
    query = 'SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC;'
    with get_cursor(conn) as cur:
        cur.execute(query, (id,))
        return cur.fetchall()


def add_url(conn, url_name):
    query = 'INSERT INTO urls(name, created_at) VALUES(%s, %s) RETURNING id;'
    post_date = date.today()
    with get_cursor(conn) as cur:
        cur.execute(query, (url_name, post_date))
        return cur.fetchone().id


def get_urls(conn):
    query = "SELECT id, name FROM urls ORDER BY id DESC;"
    with get_cursor(conn, RealDictCursor) as cur:
        cur.execute(query)
        return cur.fetchall()


def get_url_checks_all(conn):
    query = ("SELECT url_id, created_at, status_code "
             "FROM url_checks ORDER BY created_at DESC;")
    with get_cursor(conn, RealDictCursor) as cur:
        cur.execute(query)
        return cur.fetchall()


def get_urls_data(conn):
    urls = get_urls(conn)
    url_checks = get_url_checks_all(conn)

    return [
        {
            'id': url['id'],
            'name': url['name'],
            'last_check': next(
                (check['created_at'] for check in url_checks
                 if check['url_id'] == url['id']), None
            ),
            'status_code': next(
                (check['status_code'] for check in url_checks
                 if check['url_id'] == url['id']), None
            )
        }
        for url in urls
    ]


def add_url_check(conn, check_dict):
    query = """
        INSERT INTO url_checks (url_id, status_code, h1,
        title, description, created_at)
        VALUES (%(url_id)s, %(status_code)s, %(h1)s,
        %(title)s, %(description)s, %(created_at)s);
    """
    with get_cursor(conn) as cur:
        cur.execute(query, check_dict)
