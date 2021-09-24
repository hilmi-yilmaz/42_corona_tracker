from datetime import datetime, timedelta
from typing import List, Dict
import time

def get_contacts(api, infected_sessions, date_range):
	"""
	Outputs the users which sat close to the infected person.

	Arguments:
		None.

	Returns:
		None.
	"""

	i = 0

	for session in infected_sessions:
		
		print("Session {} on host {} from {} until {}".format(
			i, session["host"], session["begin_at"], session["end_at"]))

		contact_hosts: List[str] = input(
			"Which computers do you want to check?\nEnter the hostnames separated by spaces: ").split(" ")
		if session["host"] in contact_hosts:
			contact_hosts.remove(session["host"])
		
		for host in contact_hosts:
			contact_payload = {"filter[campus_id]": api.campus_id,
								"range[begin_at]": date_range, "page[size]": 100}
			contact_payload["filter[host]"] = host
			contact_data = api.get("locations", contact_payload)
			time.sleep(0.5)
			for loggins in contact_data:
				overlap = get_overlap_time(
					session["begin_at"], session["end_at"], loggins["begin_at"], loggins["end_at"])
				if overlap.days >= 0:
					print("{} was logged in {} (hours:minutes:seconds) sitting on computer {}.".format(
						loggins["user"]["login"], overlap, loggins["host"]))
		i += 1

def get_contact_hosts(infected_student) -> Dict[str, List[str]]:
	"""
	Returns a mapping of infected hosts to contact hosts like:
	{"f1r1s1.codam.nl": [f1r1s2.codam.nl, f1r1s3.codam.nl], ...}

	Returns:
		contacts: (List[str]) list containing logins names of contact persons.
	"""

	print("Which computers do you want to check?\nEnter the hostnames separated by spaces.")
	print("-------------------------------------------------------------------------------")
	i = 0
	map_host_to_contacts: Dict[str, List[str]] = {}
	for i in range(len(infected_student.session_id)):

		if infected_student.host[i] in map_host_to_contacts:
			contact_hosts = map_host_to_contacts[infected_student.host[i]]
		else:
			contact_hosts: List[str] = input("Host {}: ".format(infected_student.host[i])).split(" ")
			# Remove duplicate elements
			contact_hosts = list(dict.fromkeys(contact_hosts))
			# Remove host itself if given as input
			if infected_student.host[i] in contact_hosts:
				contact_hosts.remove(infected_student.host[i])
			# Add to dict
			map_host_to_contacts[infected_student.host[i]] = contact_hosts

		# Remove duplicate elements
		contact_hosts = list(dict.fromkeys(contact_hosts))

		i += 1

	return (map_host_to_contacts)

def is_in_students_list(contact_students: List, login: str):
	"""
	checks whether the login is already in the contacts students list.
	"""
	for i, student in enumerate(contact_students):
		if student.login == login:
			return (i)
	return (-1)

def get_date_range(day_positive, days_to_check):
	"""
	Gives a range for the inputted date.
	"""
	
	return ("{},{}".format((day_positive - timedelta(days=days_to_check)).strftime("%Y-%m-%dT%H:%M:%SZ"), day_positive.strftime("%Y-%m-%dT%H:%M:%SZ")))
	

def str_to_datetime(str):
	"""
	Convert string to datetime. This format is specific to the 42API responses.

	Arguments:
		datetime_str: (str) the datetime as a string.

	Returns:
		(datetime) containing the datetime equivalent of the input string.
	"""

	return (datetime.strptime(str, "%Y-%m-%dT%H:%M:%S.%fZ"))

def datetime_to_str(date_time):
	"""
	Convert datetime to string. This format is specific to the 42API responses.

	Arguments:
		date_time: (datetime) the datetime.

	Returns:
		(str) containing the string equivalent of the datetime object.
	"""

	return (date_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

def get_overlap_time(begin_at_infected, end_at_infected, begin_at_contact, end_at_contact):
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

	begin_at_infected = begin_at_infected
	begin_at_contact = begin_at_contact
	end_at_infected = end_at_infected
	end_at_contact = end_at_contact
	return (min(end_at_infected, end_at_contact) - max(begin_at_infected, begin_at_contact))

