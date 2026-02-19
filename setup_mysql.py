"""
Create MySQL database and prepare for migration
"""
import mysql.connector
from mysql.connector import Error

# MySQL connection
password = '@David2211.'
connection = None

print("Attempting to connect to MySQL...")

try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password=password,
        port=3306
    )
    if connection.is_connected():
        print("✓ Connected to MySQL successfully!")
except Error as e:
    print(f"❌ Failed to connect: {e}")
    exit(1)

try:
    cursor = connection.cursor()
    
    # Create database
    print("\nCreating database...")
    cursor.execute("DROP DATABASE IF EXISTS bursary_system")
    cursor.execute("CREATE DATABASE bursary_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    print("✓ Database created: bursary_system")
    
    # Show result
    cursor.execute("SHOW DATABASES LIKE 'bursary_system'")
    if cursor.fetchone():
        print("✓ Database verified successfully")
    
    connection.commit()
    
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("✓ MySQL connection closed")
