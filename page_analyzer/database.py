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
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute('SELECT * FROM urls WHERE id = %s;', (id,))
        url = cur.fetchone()
    return dict(url._asdict()) if url else None


def get_url_by_name(conn, url):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute('SELECT * FROM urls WHERE name = %s;', (url,))
        url_new = cur.fetchone()
    return dict(url_new._asdict()) if url_new else None


def show_url(conn, id):
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


def show_urls(conn):
    query = "SELECT id, name FROM urls ORDER BY id DESC;"
    with get_cursor(conn, RealDictCursor) as cur:
        cur.execute(query)
        return cur.fetchall()


def show_url_checks(conn):
    query = ("SELECT url_id, created_at, status_code "
             "FROM url_checks ORDER BY created_at DESC;")
    with get_cursor(conn, RealDictCursor) as cur:
        cur.execute(query)
        return cur.fetchall()


def add_url_check(conn, check_dict):
    query = """
        INSERT INTO url_checks (url_id, status_code, h1,
        title, description, created_at)
        VALUES (%(url_id)s, %(status_code)s, %(h1)s,
        %(title)s, %(description)s, %(created_at)s);
    """
    with get_cursor(conn) as cur:
        cur.execute(query, check_dict)
