from connect import get_db_connection

def get_bank_settings():
    cnx = get_db_connection()
    cursor = cnx.cursor()

    query = ("SELECT * FROM Bank_Settings")
    cursor.execute(query)

    res = cursor.fetchone()

    cursor.close()
    cnx.close()

    return res