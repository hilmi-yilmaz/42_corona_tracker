import sys
import time
from typing import List, Dict
from datetime import datetime, timedelta
from mysql.connector import connect, Error


class DatabaseOperations:
	"""
	Handles all operations related to the mysql database.
	Including connecting to the database,
	inserting and reading data from the database.

	Arguments:
		db_name: (str) name of the database to create if not exist, or connect to if exists.
		user: (str) mysql user
		password: (str) mysql password
	"""

	def __init__(self, db_name, user, password):
		self.db_name = db_name
		self.user = user
		self.password = password
		self.connector = self.connect_to_database()
		self.cursor = self.connector.cursor()
		self.active = []

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
		logged_in = []
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
		logged_off: List[Dict] = []
		# print(self.active)
		for user in self.active:
			if user not in logged_in:
				logged_off.append(user)
		return (logged_off)

	def read_data(self, query: str):
		"""
		Query data from the database.

		Arguments:
			query: (str) contains parameters for the query.

		Returns:
			None.
		"""
		self.cursor.execute(query)
		return (self.cursor.fetchall())

	def insert_data(self, who_logged_off: List[Dict]) -> None:
		""" 
		Inserts the people who logged off into the database.

		Arguments:
			who_logged_off: (List[Dict]) contains users who logged off.

		Returns:
			None.
		"""
		for user in who_logged_off:
			host: str = user["host"][:-9]
			begin_at = datetime.strptime(user["begin_at"], "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=2)
			end_at = datetime.strptime(user["end_at"], "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=2)
			print(f"begin_at: {begin_at}")
			print(f"end_at: {end_at}")
			insert_login_session_query: str = """
			INSERT INTO {}
			(session_id, login, begin_at, end_at)
			VALUES (%s, %s, %s, %s)
			""".format(host)
			print(f"insert_login_session_query = {insert_login_session_query}")
			self.cursor.execute(insert_login_session_query, [
				user["id"], user["user"]["login"], begin_at, end_at])
		self.connector.commit()

	def remove_old_data(self, x: int, time_frame: str):
		"""
		Removes data from the database that is 'days_old' days old.

		Arguments:
			x: (int) amount of time in timeframe.
			time_frame: (str) can any of week, day, hour.

		Returns:
			None.
		"""

		# Get all the tables first
		response = self.read_data("show tables")
		all_tables = [table for (table, ) in response]

		for table in all_tables:
			query_delete_old_data = """
			delete from {} where begin_at < date_sub(now(), interval {} {})
			""".format(table, x, "hour")
			self.cursor.execute(query_delete_old_data)
			self.connector.commit()
