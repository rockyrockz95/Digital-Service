import mysql.connector

mydb = mysql.connector.connect(
    host="localhost", user="root", password="databases336", database="cc_copy"
)


my_cursor = mydb.cursor()

# my_cursor.execute("CREATE DATABASE cc_copy")

my_cursor.execute("SHOW DATABASES")

for db in my_cursor:
    print(db)
