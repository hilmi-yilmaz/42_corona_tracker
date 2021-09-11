import sys
import time
from typing import List, Dict
from datetime import datetime
from mysql.connector import connect, Error


class DatabaseOperations:
    """
    Handles all operations related to the mysql database.
    Including connecting to the database,
    inserting and reading data from the database.
    """

    def __init__(self, db_name, user, password):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.connector = self.connect_to_database()
        self.cursor = self.connector.cursor()
        self.active = []  # Contains login session id

    def connect_to_database(self):
        """
        Connects to the database.

        Arguments:
                None.

        Returns:
                connection: Connection object contains all that's needed to communicate with the database.
        """
        try:
            connection = connect(
                host="localhost",
                user=self.user,
                password=self.password,
                database=self.db_name)
            if connection.is_connected():
                db_info = connection.get_server_info()
                print(f"Connected to MySQL server version {db_info}")
        except Error as err:
            sys.exit(f"Cannot connect to {self.db_name}: {err}")
        print(f"Succesfully connected to database {self.db_name}.")
        return (connection)

    def get_active_students(self, data: List[Dict]) -> List[Dict]:
        """
        Get the currently active users.

        Arguments:
                data: (List[Dict]) contains user data from the 42 API.

        Returns:
                logged_in: (List[Dict]) contains currently active session_id's. 
        """
        logged_in = []  # the people that are currently active, this can be compared to self.active
        for user in data:
            logged_in.append(user)
        return (logged_in)

    def get_recently_logged_off(self, logged_in: List[Dict]) -> List[Dict]:
        """
        Get the users that just logged off.

        Arguments:
                logged_in: (List[Dict]) contains currently logged in users.

        Returns:
                logged_off: (List[Dict]) contains logged off users.
        """
        logged_off = list(set(self.active) - set(logged_in))
        return (logged_off)

    def read_data(self, query):
        self.cursor.execute(query)
        return (self.cursor.fetchall())

    def insert_data(self, who_logged_off: List[Dict]):
        """ 
        Inserts the people who logged off into the database.

        Arguments:
                who_logged_off: (List[Dict]) contains users who logged off.

        Returns:
                None.
        """
        # Create table if table doesn't exist yet
        self.extract_hosts(who_logged_off)

        # Insert user data
        for user in who_logged_off:
            host: str = user["host"][:-9]
            #begin_at = datetime.strptime(user["begin_at"],  "%Y-%m-%dT%H:%M:%S.%fZ")
            #end_at = datetime.strptime(user["end_at"],  "%Y-%m-%dT%H:%M:%S.%fZ")
            insert_login_session_query: str = """
			INSERT INTO {}
			(session_id, login, begin_at, end_at)
			VALUES (%s, %s, %s, %s)
			""".format(host)
            # print(insert_login_session_query)
            self.cursor.execute(insert_login_session_query, [
                                user["id"], user["user"]["login"], user["begin_at"], user["end_at"]])
        self.connector.commit()

    def extract_hosts(self, data: List[Dict]):
        """
        Extract the hosts from the data (for example f0r1s6.codam.nl).
        If there is no table for this specific host yet, create one.

        Arguments:
                data: (List[Dict]) contains user data.

        Returns:
                None.
        """
        for user in data:
            host: str = user["host"][:-9]
            query: str = "show tables like \'" + str(host) + "\';"
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            if not result:
                #print("{} doesn't exist as a table. Creating...".format(host))
                self.create_host_table(host)

    def create_host_table(self, host_name: str):
        """
        Create a table with host_name.

        Arguments:
                host_name: (str) name of the host.
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
