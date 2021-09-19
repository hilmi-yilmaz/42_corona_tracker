import readline
import time
from datetime import datetime, timedelta
from typing import Dict, List
from .api42_wrapper import API42

class GetContacts(API42):
	"""
	Contains functions to get contact persons for an infected person.
	"""

	def __init__(self, infected_person_login, day_positive, days):
		super().__init__()
		self.infected_person_login = infected_person_login
		self.day_positive = day_positive
		self.days = days
		self.infected_person_all_sessions = self.get_infected_person_sessions()

	def get_infected_person_sessions(self):
		"""
		Get the sessions for the infected persons for the past days.

		Arguments:{"filter[campus_id]": self.campus_id, "range[begin_at]": begin_at_range, "page[size]": 100}
				days: (int) how much previous days to check for.

		Returns:
				infected_person_all_sessions: (List[Dict]) contains all sessions of the infected person for the past days.
		"""

		begin_at_range = self.get_date_range()
		print(begin_at_range)
		payload = {"filter[campus_id]": self.campus_id,
				   "range[begin_at]": begin_at_range, "page[size]": 100}
		data = self.get("locations", payload)
		infected_person_all_sessions = [
			session for session in data if self.infected_person_login == session["user"]["login"]]
		return (infected_person_all_sessions)

	def get_contacts(self):
		"""
		Outputs the users which sat close to the infected person.

		Arguments:
				None.

		Returns:
				None.
		"""

		i = 0
		for infected_person_session in self.infected_person_all_sessions:
			print("Session {} on host {} from {} until {}".format(
				i, infected_person_session["host"], infected_person_session["begin_at"], infected_person_session["end_at"]))
			contact_hosts: List[str] = input(
				"Which computers do you want to check?\nEnter the hostnames separated by spaces: ").split(" ")
			if infected_person_session["host"] in contact_hosts:
				contact_hosts.remove(infected_person_session["host"])
			for host in contact_hosts:
				contact_payload = {"filter[campus_id]": self.campus_id,
								   "range[begin_at]": self.get_date_range(), "page[size]": 100}
				contact_payload["filter[host]"] = host
				contact_data = self.get("locations", contact_payload)
				time.sleep(1)
				for loggins in contact_data:
					overlap = self.get_overlap_time(
						infected_person_session["begin_at"], infected_person_session["end_at"], loggins["begin_at"], loggins["end_at"])
					if overlap.days >= 0:
						print("{} was logged in {} (hours:minutes:seconds) sitting on computer {}.".format(
							loggins["user"]["login"], overlap, loggins["host"]))
					time.sleep(1)
			i += 1

	def get_date_range(self) -> str:
		"""
		Calculates the range to pass to the API.

		Arguments:
				None.

		Returns:
				(str) representing a range which can be passed as parameter to the API.
		"""

		return ("{},{}".format((self.day_positive - timedelta(days=self.days)).strftime("%Y-%m-%dT%H:%M:%SZ"), self.day_positive.strftime("%Y-%m-%dT%H:%M:%SZ")))

	def str_to_datetime(self, datetime_str):
		"""
		Convert string to datetime. This format is specific to the 42API responses.

		Arguments:
				datetime_str: (str) the datetime as a string.

		Returns:
				(datetime) containing the datetime equivalent of the input string.
		"""

		return (datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ"))

	def get_overlap_time(self, begin_at_infected, end_at_infected, begin_at_contact, end_at_contact):
		"""
		Calculates the overlap time between 2 login sessions.

		Arguments:
				begin_at_infected: (datetime) begin time of infected person.
				end_at_infected: (datetime) end time of infected person.
				begin_at_contact: (datetime) begin time of contact person.
				end_at_contact: (datetime) end time of contact person.

		Returns:
				(datetime) the overlap time.
		"""

		begin_at_infected = self.str_to_datetime(begin_at_infected)
		begin_at_contact = self.str_to_datetime(begin_at_contact)
		end_at_infected = self.str_to_datetime(end_at_infected)
		end_at_contact = self.str_to_datetime(end_at_contact)
		return (min(end_at_infected, end_at_contact) - max(begin_at_infected, begin_at_contact))


if __name__ == "__main__":
	contact = GetContacts("rcappend", "18-09-2021", 3)
	contact.get_infected_person_sessions()
