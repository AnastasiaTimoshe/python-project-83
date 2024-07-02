import psycopg2
from psycopg2.extras import NamedTupleCursor, RealDictCursor
from datetime import date


def create_connection(database_url):
    return psycopg2.connect(database_url)


def get_url_by_id(conn, id):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute('SELECT * FROM urls WHERE id = %s;', (id,))
        url = cur.fetchone()
    return url


def get_url_by_name(conn, url):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute('SELECT * FROM urls WHERE name = %s;', (url,))
        url_new = cur.fetchone()
    return url_new


def show_url(conn, id):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            'SELECT * FROM url_checks WHERE url_id = %s '
            'ORDER BY id DESC;', (id,)
        )
        checks = cur.fetchall()
    return checks


def add_url(conn, url_name):
    post_date = date.today()
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            'INSERT INTO urls(name, created_at) VALUES(%s, %s) RETURNING id;',
            (url_name, post_date)
        )
        url_id = cur.fetchone().id
    return url_id


def show_urls(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT id, name FROM urls ORDER BY id DESC;")
        urls = cur.fetchall()
    return urls


def show_url_checks(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT url_id, created_at, status_code "
                    "FROM url_checks ORDER BY created_at DESC;")
        url_checks = cur.fetchall()
    return url_checks


def add_url_check(conn, check_dict):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute("""
            INSERT INTO url_checks (url_id, status_code,
            h1, title, description, created_at)
            VALUES (%(url_id)s, %(status_code)s, %(h1)s,
            %(title)s, %(description)s, %(created_at)s);
        """, check_dict)
    conn.commit()
