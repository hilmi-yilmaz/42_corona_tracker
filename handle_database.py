import sys
import time
from typing import List, Dict, Tuple
from datetime import datetime, timedelta
from mysql.connector import connect, Error


class OperationsDatabase:
    """
    Handles all operations related to the mysql database.
    Including connecting to the database,
    inserting and reading data from the database.

    Arguments:
		db_name: (str) name of the database to create if not exist, or connect to if exists.
		user: (str) mysql user
		password: (str) mysql password
    """

    def __init__(self, db_name, table_name, user, password):
        self.db_name = db_name
        self.table_name = table_name
        self.user = user
        self.password = password
        self.connector = self.connect_to_database()
        self.cursor = self.connector.cursor(dictionary=True)

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

    def read(self, query: str) -> List[Dict]:
        """
        Read data from database.

        Arguments:
            query: (str) the query to execute against the database.

        Returns:
            data: (List[Dict]) data returned by the database.
        """

        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return (data)

    def insert(self, insert_query: str, insert_data: List) -> None:
        """
        Insert data into database.

        Arguments:
                insert_query: (str) the query to execute against the database.
                insert_data: (List) the data to pass within the query.

        Returns:
                None.
        """

        self.cursor.execute(insert_query, insert_data)
        self.connector.commit()


class UpdateDatabase(OperationsDatabase):
    """
    Updates the database. Inserts and deletes data.
    """

    def __init__(self, db_name, table_name, user, password):
        super().__init__(db_name, table_name, user, password)
        self.active = []

    def get_recently_logged_off(self, logged_in: List[Dict]) -> List[Dict]:
        """
        Get the users that just logged off.

        Arguments:
            logged_in: (List[Dict]) contains currently logged in users.

        Returns:
            logged_off: (List[Dict]) contains logged off users.
        """

        logged_off: List[Dict] = []
        for user in self.active:
            if user not in logged_in:
                logged_off.append(user)
        return (logged_off)

    def insert_logged_off(self, logged_off_session: Dict) -> None:
        """
        Insert recently logged of users into the database.

        Arguments:
            logged_off_session: (Dict) a single response from the 42API.

        Returns:
            None.
        """

        begin_at = datetime.strptime(
            logged_off_session["begin_at"], "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=2)
        end_at = datetime.strptime(
            logged_off_session["end_at"], "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=2)
        insert_login_session_query: str = """
		INSERT INTO {}
		(session_id, host, login, begin_at, end_at)
		VALUES (%s, %s, %s, %s, %s)
		""".format(self.table_name)
        insert_login_session_data = [
            logged_off_session["id"], logged_off_session["host"], logged_off_session["user"]["login"], begin_at, end_at]
        print(f"insert_login_session_query = {insert_login_session_query}")
        self.insert(insert_login_session_query, insert_login_session_data)

    def remove_old_data(self, x: int, time_frame: str):
        """
        Removes data from the database that is x timeframes old.

        Arguments:
            x: (int) amount of time in timeframe.
            time_frame: (str) can be any of week, day, hour.

        Returns:
            None.
        """

        query_delete_old_data = """
		delete from {} where end_at < date_sub(now(), interval {} {})
		""".format(self.table_name, x, "hour")
        self.cursor.execute(query_delete_old_data)
        self.connector.commit()


if __name__ == "__main__":

    db = UpdateDatabase("codam_corona_tracker", "data", "hilmi", "hilmi")

    #db = OperationsDatabase("codam_corona_tracker", "hilmi", "hilmi")
    query = "select * from data"
    data = db.read(query)
    print("data\n{}".format(data))
    print(type(data))

    insert_query = "insert into data (session_id, host, login, begin_at, end_at) values (%s, %s, %s, %s, %s)"
    insert_data = ["23331", "f0r1s1", "yp33333rppr", datetime.now(), datetime.now() + timedelta(hours=1)]
    db.insert(insert_query, insert_data)
