import mysql.connector
from mysql.connector import Error
from financial_product import Option, Swap

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
    """Load products from the database, including their IDs."""
    connection = create_connection()
    if connection is None:
        return []

    products = []
    cursor = connection.cursor(dictionary=True)

    try:
        # Load options
        cursor.execute("SELECT * FROM options")
        options = cursor.fetchall()
        for option in options:
            products.append(Option(
                _id=option['id'],  # Set ID
                _name=option['name'],
                _price=option['price'],
                _quantity=0,  # Assuming quantity is not stored in the DB
                _description="Option Product",
                _strike_price=option['strike_price'],
                _expiration=option['expiration'],
                _volatility=option['volatility']
            ))

        # Load swaps
        cursor.execute("SELECT * FROM swaps")
        swaps = cursor.fetchall()
        for swap in swaps:
            products.append(Swap(
                _id=swap['id'],  # Set ID
                _name=swap['name'],
                _price=swap['price'],
                _quantity=0,  # Assuming quantity is not stored in the DB
                _description="Swap Product",
                _fixed_rate=swap['fixed_rate'],
                _notional=swap['notional']
            ))

    except Error as e:
        print(f"Error: {e}")
    finally:
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

def save_products_to_db(products):
    """Update a list of products in the database using their IDs and return success status and message."""
    connection = create_connection()
    if connection is None:
        return False, "Failed to connect to the database."

    cursor = connection.cursor()
    try:
        for product in products:
            if isinstance(product, Option):
                cursor.execute(
                    """
                    UPDATE options SET price = %s, strike_price = %s, expiration = %s, volatility = %s
                    WHERE id = %s
                    """,
                    (product.price, product.strike_price, product.expiration, product.volatility, product.id)
                )
            elif isinstance(product, Swap):
                cursor.execute(
                    """
                    UPDATE swaps SET price = %s, fixed_rate = %s, notional = %s
                    WHERE id = %s
                    """,
                    (product.price, product.fixed_rate, product.notional, product.id)
                )
            else:
                cursor.execute(
                    """
                    UPDATE financial_products SET price = %s
                    WHERE id = %s
                    """,
                    (product.price, product.id)
                )
        connection.commit()
        return True, ""
    except Error as e:
        return False, str(e)
    finally:
        cursor.close()
        connection.close() 