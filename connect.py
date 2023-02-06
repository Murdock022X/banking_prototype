import sqlite3

def get_db_connection():
    """
    Get a connection to the bank database.
    :return: Connection to the database, dictionary ouput enabled.
    """
    cnx = sqlite3.connect('bank_data.db')
    cnx.row_factory = sqlite3.Row
    return cnx