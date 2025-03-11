import mysql.connector

password = ""	
database = "milma_management"

def connect_db():
    """Establish a database connection."""
    try:
        cnx = mysql.connector.connect(user="root", password=password, host="localhost", database=database)
        return cnx
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

def execute_query(query, params=None, fetch=False, commit=False):
    """General function to execute queries safely."""
    cnx = connect_db()
    if not cnx:
        return None  # Return None if connection fails
    
    try:
        with cnx.cursor(dictionary=True) as cur:
            cur.execute(query, params or ())  # Use empty tuple if no params
            
            if fetch:
                result = cur.fetchall()
            elif commit:
                cnx.commit()
                result = cur.rowcount if 'DELETE' in query or 'UPDATE' in query else cur.lastrowid
            else:
                result = None

        cnx.close()
        return result

    except mysql.connector.Error as err:
        print(f"Query execution error: {err}")
        return None  # Handle error safely

def select(query, params=None):
    """Execute SELECT queries."""
    return execute_query(query, params, fetch=True)

def update(query, params=None):
    """Execute UPDATE queries."""
    return execute_query(query, params, commit=True)

def delete(query, params=None):
    """Execute DELETE queries."""
    return execute_query(query, params, commit=True)

def insert(query, params=None):
    """Execute INSERT queries and return last inserted ID."""
    return execute_query(query, params, commit=True)
