import sys
from datetime import datetime
from mysql.connector import connect, Error
from getpass import getpass
from get_user_data import API42

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
        self.active = [] # Contains login session id

    def connect_to_database(self):
        try:
            connection = connect(
                host="localhost",
                user=self.user,
                password=self.password,
                database=self.db_name)
            if connection.is_connected():
                db_info = connection.get_server_info()
                print(f"Connected to MySQL server version {db_info}")
        except Error as e:
            print(f"Cannot connect to {self.db_name}: {e}")
            sys.exit(1)
        print(f"Succesfully connected to database {self.db_name}.")
        return (connection)

    def get_active_students(self, data):
        for user in data:
            self.active.append(user["id"])
        print(self.active)

    def read_data(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        for row in result:
            print(row)

    
    def insert_data(self, data):
        # Create tables if tables don't exist yet
        self.extract_hosts(data)

        # Insert user data
        for user in data:

            host = user["host"][:-9]
            #begin_at = datetime.strptime(user["begin_at"],  "%Y-%m-%dT%H:%M:%S.%fZ")
            #end_at = datetime.strptime(user["end_at"],  "%Y-%m-%dT%H:%M:%S.%fZ")
            insert_login_session_query = """
            INSERT INTO {}
            (session_id, login, begin_at, end_at)
            VALUES (%s, %s, %s, %s)
            """.format(host)#, user["user"]["login"], user["begin_at"])#, user["end_at"])
            #print(insert_login_session_query)
            #datetime_object = datetime.strptime(user["begin_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
            #print(datetime_object)
            self.cursor.execute(insert_login_session_query, [user["id"], user["user"]["login"], user["begin_at"], user["end_at"]])
        self.connector.commit()
            

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
            begin_at VARCHAR(100),
            end_at VARCHAR(100)
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
db_operations.get_active_students(data)
db_operations.insert_data(data)