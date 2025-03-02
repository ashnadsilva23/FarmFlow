import mysql.connector

password = ""	
database = "milma_management"

def connect_db():
    """Establish a database connection."""
    return mysql.connector.connect(user="root", password=password, host="localhost", database=database)

def select(query, params=None):
    """Execute SELECT queries with optional parameters."""
    cnx = connect_db()
    cur = cnx.cursor(dictionary=True)
    
    if params:
        cur.execute(query, params)  # Secure parameterized query
    else:
        cur.execute(query)

    result = cur.fetchall()
    
    cur.close()
    cnx.close()
    return result

def update(query, params=None):
    """Execute UPDATE queries with optional parameters."""
    cnx = connect_db()
    cur = cnx.cursor(dictionary=True)

    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)

    cnx.commit()
    row_count = cur.rowcount

    cur.close()
    cnx.close()
    return row_count

def delete(query, params=None):
    """Execute DELETE queries with optional parameters."""
    cnx = connect_db()
    cur = cnx.cursor(dictionary=True)

    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)

    cnx.commit()
    row_count = cur.rowcount

    cur.close()
    cnx.close()
    return row_count  # Missing return statement was added

def insert(query, params=None):
    """Execute INSERT queries with optional parameters and return last inserted ID."""
    cnx = connect_db()
    cur = cnx.cursor(dictionary=True)

    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)

    cnx.commit()
    last_id = cur.lastrowid

    cur.close()
    cnx.close()
    return last_id
