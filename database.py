import psycopg2

# Connect to your postgres DB
# conn = psycopg2.connect(host="134.209.24.19", dbname="collins", user="collins",password="12345",port=5432)
conn = psycopg2.connect(host="localhost", port="5432", database="myduka", user="postgres", password="Pass@123!")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a query
cur.execute("SELECT * FROM products;")

# Retrieve query results
records = cur.fetchall()
# print(records)