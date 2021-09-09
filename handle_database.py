import sys
import time
from datetime import datetime
from mysql.connector import connect, Error
#from getpass import getpass


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
        """
        Get the currently active people.
        """
        currently_active = [] # the people that are currently active, this can be compared to self.active
        for user in data:
            currently_active.append(user["id"])
        return (currently_active)

    def read_data(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        for row in result:
            print(row)

    def get_recently_logged_off(self, currently_active):
        """
        Get the session id that just logged off. This session will be put into the database.
        """
        logged_off = list(set(self.active) - set(currently_active))
        return (logged_off)



    def insert_data(self, data, currently_active):
        # Create table if table doesn't exist yet
        self.extract_hosts(data)

        # Get the difference between the active and currently_active people
        logged_off = list(set(self.active) - set(currently_active))
        #print(logged_off)

        # Request the api for the session which logged off
        

        # Insert user data
        # for user in data:

        #     host = user["host"][:-9]
        #     if (user["id"] not in self.active):
        #         #begin_at = datetime.strptime(user["begin_at"],  "%Y-%m-%dT%H:%M:%S.%fZ")
        #         #end_at = datetime.strptime(user["end_at"],  "%Y-%m-%dT%H:%M:%S.%fZ")
        #         insert_login_session_query = """
        #         INSERT INTO {}
        #         (session_id, login, begin_at, end_at)
        #         VALUES (%s, %s, %s, %s)
        #         """.format(host)
        #         #print(insert_login_session_query)
        #         self.cursor.execute(insert_login_session_query, [user["id"], user["user"]["login"], user["begin_at"], user["end_at"]])
        # self.connector.commit()
            

    def extract_hosts(self, data):
        """
        Extract the hosts from the data (for example f0r1s6.codam.nl).
        If there is no table for this specific host yet, create one.
        """
        for user in data:
            host = user["host"][:-9]
            query = "show tables like \'" + str(host) + "\';"
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            if result:
                #print("{} does exist as a table".format(host))
                pass
            else:
                #print("{} doesn't exist as a table. Creating...".format(host))
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