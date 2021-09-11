import sys
import time
from typing import List, Dict
from datetime import datetime
from mysql.connector import connect, Error

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
		except Error as err:
			sys.exit(f"Cannot connect to {self.db_name}: {err}")
		print(f"Succesfully connected to database {self.db_name}.")
		return (connection)

	def get_active_students(self, data: List[Dict]) -> List[Dict]:
		"""
		Get the currently active people.

		Arguments:
			data: list with user data from the 42 api

		Returns:
			currently_active: list of currently active session_id's 
		"""
		currently_active = [] # the people that are currently active, this can be compared to self.active
		for user in data:
			currently_active.append(user)
		return (currently_active)

	def get_recently_logged_off(self, currently_active: List[Dict]) -> List[Dict]:
		"""
		Get the session id that just logged off. This session will be put into the database.
		"""
		logged_off = list(set(self.active) - set(currently_active))
		return (logged_off)

	def read_data(self, query):
		self.cursor.execute(query)
		return (self.cursor.fetchall())

	def insert_data(self, who_logged_off: List[Dict]):
		# Create table if table doesn't exist yet
		self.extract_hosts(who_logged_off)

		# Insert user data
		for user in who_logged_off:
			host = user["host"][:-9]
			#begin_at = datetime.strptime(user["begin_at"],  "%Y-%m-%dT%H:%M:%S.%fZ")
			#end_at = datetime.strptime(user["end_at"],  "%Y-%m-%dT%H:%M:%S.%fZ")
			insert_login_session_query = """
			INSERT INTO {}
			(session_id, login, begin_at, end_at)
			VALUES (%s, %s, %s, %s)
			""".format(host)
			#print(insert_login_session_query)
			self.cursor.execute(insert_login_session_query, [user["id"], user["user"]["login"], user["begin_at"], user["end_at"]])
		self.connector.commit()
			

	def extract_hosts(self, data: List[Dict]):
		"""
		Extract the hosts from the data (for example f0r1s6.codam.nl).
		If there is no table for this specific host yet, create one.
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