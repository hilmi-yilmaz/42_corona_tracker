import sys

from mysql.connector import connect, Error
from getpass import getpass
from get_user_data import API42

# Get the data from the 42 API
# api = API42()
# payload = {"filter[campus_id]":14, "filter[active]": "true", "page[size]": 50}
# data = api.get("locations", payload)

# # Print the data obtained from api request
# i = 0
# for element in data:
#     print(element)
#     print("")
#     i += 1
# print(i)

# # Connect to the database with mysql-connector
# try:
#     connection = connect(
#         host="localhost",
#         user="hilmi",
#         password="hilmi",
#         database="classicmodels")
# except Error as e:
#     print(e)
#     connection.close()

# # Cursor is used for executing SQL queries, which abstracts away the access to database records
# cursor = connection.cursor()

# # Show the tables
# cursor.execute("show tables")
# for tables in cursor:
#     print(tables)

# # Select some data from employees table
# select_employees_query = "select * from employees"
# with connection.cursor() as cursor:
#     cursor.execute(select_employees_query)
#     result = cursor.fetchall()
#     for row in result:
#         print(row)

# # Close the connection
# connection.close()

class DatabaseOperations:
    """
    Handles all operations related to the mysql database.
    """

    def __init__(self, db_name, user, password):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.connector = self.connect_to_database()
        self.cursor = self.connector.cursor()

    def connect_to_database(self):
        try:
            connection = connect(
                host="localhost",
                user=self.user,
                password=self.password,
                database=self.db_name)
        except Error as e:
            print(f"Cannot connect to {self.db_name}: {e}")
            sys.exit(1)
        print(f"Succesfully connected to database {self.db_name}.")
        return (connection)

    def read_data(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        for row in result:
            print(row)

    
    def insert_data(self, data):
        # Create tables if tables don't exist yet
        self.extract_hosts(data)

        # Insert user data
        #for user in data:


    def extract_hosts(self, data):
        """
        Extract the computers from the data (for example f0r1s6.codam.nl).
        If there is no table for this specific computer yet, create one.
        """
        for user in data:
            host = user["host"][:-9]
            query = "show tables like \'" + str(host) + "\';"
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            if result:
                print("{} does exist as a table".format(host))
            else:
                print("{} doesn't exist as a table. Creating...".format(host))
                self.create_host_table(host)

    def create_host_table(self, host_name):
        """
        Create a table with the host_name.
        """
        create_host_table_query = '''
        CREATE TABLE {}(
            session_id INT,
            login VARCHAR(100),
            begin_at DATETIME,
            end_at DATETIME
        )
        '''.format(host_name)
        self.cursor.execute(create_host_table_query)
        self.connector.commit()





# Instantiate a DatabaseOperations object
db_operations = DatabaseOperations("codam_corona_tracker", "hilmi", "hilmi")

# Perform a query
api = API42()
payload = {"filter[campus_id]":14, "filter[active]": "true", "page[size]": 50}
data = api.get("locations", payload) # data is a list
db_operations.insert_data(data)