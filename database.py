import psycopg2

# Connect to your postgres DB
conn = psycopg2.connect(dbname="myduka", user="postgres",password="Pass@123!",port=5432)

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a query
cur.execute("SELECT * FROM products;")

# Retrieve query results
records = cur.fetchall()
# print(records)