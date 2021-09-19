import argparse
import readline
import time
from datetime import datetime, timedelta
from typing import Dict, List

from get_user_data import API42

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
		payload = {"filter[campus_id]": self.campus_id, "range[begin_at]": begin_at_range, "page[size]": 100}
		data = self.get("locations", payload)
		infected_person_all_sessions = [session for session in data if self.infected_person_login == session["user"]["login"]]
		return (infected_person_all_sessions)

	def get_contacts(self):
		"""
		a
		"""
		i = 0
		for infected_person_session in self.infected_person_all_sessions:
			print("Session {} on host {} from {} untill {}".format(i, infected_person_session["host"], infected_person_session["begin_at"], infected_person_session["end_at"]))
			contact_hosts: List[str] = input(
				"Which computers do you want to check?\nEnter the hostnames separated by spaces: ").split(" ")
			if infected_person_session["host"] in contact_hosts:
				contact_hosts.remove(infected_person_session["host"])
			for host in contact_hosts:
				contact_payload = {"filter[campus_id]": self.campus_id, "range[begin_at]": self.get_date_range(), "page[size]": 100}
				contact_payload["filter[host]"] = host
				contact_data = self.get("locations", contact_payload)
				for loggins in contact_data: # could be more people on same computer with overlap with infected person
					overlap = self.get_overlap_time(infected_person_session["begin_at"], infected_person_session["end_at"], loggins["begin_at"], loggins["end_at"])
					if overlap.days >= 0:
						print("{} was logged in {} (hours:minutes:seconds) sitting on computer {}.".format(
                    		loggins["user"]["login"], overlap, loggins["host"]))
					time.sleep(1)
			i += 1

	def get_date_range(self) -> str:
		return ("{},{}".format((self.day_positive - timedelta(days=self.days)).strftime("%Y-%m-%dT%H:%M:%SZ"), self.day_positive.strftime("%Y-%m-%dT%H:%M:%SZ")))

	def str_to_datetime(self, datetime_str):
		return (datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ"))
								  

	def get_overlap_time(self, begin_at_infected, end_at_infected, begin_at_contact, end_at_contact):
		begin_at_infected = self.str_to_datetime(begin_at_infected)
		begin_at_contact = self.str_to_datetime(begin_at_contact)
		end_at_infected = self.str_to_datetime(end_at_infected)
		end_at_contact = self.str_to_datetime(end_at_contact)
		return (min(end_at_infected, end_at_contact) - max(begin_at_infected, begin_at_contact))



if __name__ == "__main__":
	contact = GetContacts("rcappend", "18-09-2021", 3)
	contact.get_infected_person_sessions()