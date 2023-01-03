from configparser import ConfigParser
import psycopg
import logging

logging.basicConfig(
    filename="data_scraping.log",
    level=logging.INFO,
    encoding="utf-8",
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)


def config(filename: str = "db.ini", section: str = "postgres") -> dict:
    """
    Parses config file with Postgres credentials.
    Returns a dictionary.
    """

    parser = ConfigParser()
    parser.read("db.ini")

    db = {}

    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )

    return db


def create_connection(credentials: dict, dbname: str):
    """ "Connect to the PostgreSQL database server (localhost)"""

    conn = None
    try:
        conn = psycopg.connect(**credentials, dbname=dbname)
        cur = conn.cursor()
        cur.execute("SELECT version()")
        db_version = cur.fetchone()
        logging.info(f"Connected to PostgreSQL version: {db_version}")
        cur.close()
    except psycopg.DatabaseError as error:
        logging.error(error)
        raise error

    return conn


def create_table(conn, sql: str):
    with conn.cursor() as cur:
        cur.execute(sql)
        cur.close()
    conn.commit()


def batch_insert_values(conn, sql, iterable):
    with conn.cursor() as cur:
        cur.executemany(sql, iterable)
        cur.close()
    conn.commit()
