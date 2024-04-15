import mysql.connector  # Replace with your database library (e.g., psycopg2 for PostgreSQL)

# Database connection details (replace with your actual credentials)
db_name = "student"
username = "root"
password = "0990064691a"
host = "127.0.0.1"  # Or the database server hostname/IP

# Connect to the database
try:
    connection = mysql.connector.connect(
        database=db_name, user=username, password=password, host=host
    )
    cursor = connection.cursor()

except mysql.connector.Error as err:
    print("Error connecting to database:", err)
    exit()

# Connect to the database
try:
    connection = mysql.connector.connect(
        database=db_name, user=username, password=password, host=host
    )
    cursor = connection.cursor()

except mysql.connector.Error as err:
    print("Error connecting to database:", err)
    exit()

# Sample SELECT query
sql_query = "SELECT * FROM students"  # Change "students" to your actual table name

# Execute the query
try:
    cursor.execute(sql_query)
    # Fetch all results (replace with specific fetching methods if needed)
    results = cursor.fetchall()
    # Process the results (e.g., print, store in a list)
    for row in results:
        print(row)  # Print each row as a tuple

except mysql.connector.Error as err:
    print("Error fetching data:", err)

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()