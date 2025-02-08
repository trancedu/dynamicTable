import mysql.connector
from mysql.connector import Error

def create_connection():
    """Create a database connection."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='financial_product_db',
            user='User',
            password='user123'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def load_products():
    """Load products from the database."""
    connection = create_connection()
    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT name, price FROM financial_products")
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return products

def save_product(name, price):
    """Save a product to the database."""
    connection = create_connection()
    if connection is None:
        return False

    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO financial_products (name, price) VALUES (%s, %s)", (name, price))
        connection.commit()
        return True
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        connection.close() 