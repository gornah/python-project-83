from contextlib import contextmanager
from psycopg2.extras import NamedTupleCursor
from psycopg2 import pool
from datetime import datetime
from page_analyzer.config import DATABASE_URL

# if not DATABASE_URL:
#    raise ValueError("DATABASE_URL is not set in the environment variables.")

connection_pool = pool.SimpleConnectionPool(1, 10, DATABASE_URL)


@contextmanager
def get_connection():
    """
    Context manager for getting a connection from the pool.
    """
    conn = connection_pool.getconn()
    try:
        yield conn
    finally:
        connection_pool.putconn(conn)


def get_from_db(query, value=None, fetch=''):
    """
    Executes a SELECT query and returns the data.
    """
    with get_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(query, (value,) if value is not None else None)
            data = cursor.fetchall() if fetch == 'all' else cursor.fetchone()
    return data


def add_to_db(query, *args):
    """
    Executes an INSERT query.
    """
    with get_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(query, args)
        conn.commit()


def get_url(search_by, value):
    """
    Fetches a record from the `urls` table by name or ID.
    """
    if search_by == 'name':
        query = 'SELECT * FROM urls WHERE name=%s'
    elif search_by == 'id':
        query = 'SELECT * FROM urls WHERE id=%s'
    else:
        raise ValueError('Invalid query parameter in get_url function')
    return get_from_db(query, value)


def get_url_list():
    """
    Returns a list of unique URLs with the latest checks.
    """
    query = '''SELECT DISTINCT ON (urls.id)
                urls.id,
                name,
                url_checks.created_at,
                status_code
            FROM urls
            LEFT JOIN url_checks ON urls.id=url_id
            ORDER BY urls.id DESC'''
    return get_from_db(query, fetch='all')


def add_url_to_base(url):
    """
    Adds a new URL to the `urls` table.
    """
    query = 'INSERT INTO urls (name, created_at) VALUES (%s, %s);'
    add_to_db(query, url, datetime.now())


def add_check_to_base(id, check_data):
    """
    Adds check data for a URL to the `url_checks` table.
    """
    query = '''INSERT INTO url_checks
            (url_id, status_code, h1, title, description, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)'''
    add_to_db(
        query,
        id,
        check_data['status_code'],
        check_data['h1'],
        check_data['title'],
        check_data['description'],
        datetime.now()
        )


def get_urls_with_checks(id):
    """
    Returns URL and its checks by ID.
    """
    query = '''SELECT name,
                urls.created_at as url_created_at,
                urls.id,
                url_checks.id as check_id,
                status_code, h1, title,
                description,
                url_checks.created_at as check_created_at
            FROM urls
            LEFT JOIN url_checks ON urls.id=url_id
            WHERE urls.id=%s
            ORDER BY url_checks.id DESC'''
    return get_from_db(query, id, fetch='all')
