from datetime import date, datetime, timedelta
from typing import Dict, List
from .utils.time import *

class Student:

	def __init__(self, login):
		self.login: str = login
		self.session_id: List[int] = []
		self.host: List[str] = []
		self.begin_at: List[datetime] = []
		self.end_at: List[datetime] = []

	
	def append_session(self, session_id, host, begin_at, end_at):
		"""
		Get the sessions of this student for the past days.

		Arguments:
			data: List[Dict] containing response from API42 with login sessions.

		Returns:
			infected_sessions: (List[Dict]) contains all sessions of the student person for the past days.
		"""
		if end_at == None:
			print("The infected person is currently logged in.")
			return (False)
		self.session_id.append(session_id)
		self.host.append(host)
		self.begin_at.append(str_to_datetime(begin_at) + timedelta(hours=2))
		self.end_at.append(str_to_datetime(end_at) + timedelta(hours=2))
		return (True)

class InfectedStudent(Student):

	def __init__(self, login, day_positive, days_to_check):
		super().__init__(login)
		self.day_positive: date = day_positive
		self.days_to_check: int = days_to_check