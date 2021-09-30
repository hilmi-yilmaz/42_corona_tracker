import readline
import sys
from datetime import date, timedelta
from typing import List, Dict
from ..students import Student, InfectedStudent
from .time import get_overlap_time

def get_data(api, day_positive: date, days_to_check: int) -> List[Dict]:
	"""
	Get data from the past few days.
	"""
	date_range: str = "{},{}".format((day_positive - timedelta(days=days_to_check)).strftime("%Y-%m-%dT%H:%M:%SZ"), day_positive.strftime("%Y-%m-%dT%H:%M:%SZ"))
	payload = {"filter[campus_id]": api.campus_id, "range[begin_at]": date_range, "page[size]": 100}
	data: List[Dict] = api.get("locations", payload)
	if not data:
		print("No data available. No one was logged in between {}".format(date_range))
	return (data)

def get_infected_student_sessions(data: List[Dict], infected_student: InfectedStudent):

	for session in data:
		if session["user"]["login"] == infected_student.login:
			res = infected_student.append_session(session["id"], session["host"], session["begin_at"], session["end_at"])
			if res == -1: # infected student is currently online
				break

	# If no sessions of infected user, exit program
	if not infected_student.session_id:
		print("Infected person has no sessions in given time period.")
		sys.exit(1)

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
		if infected_student.host[i] not in map_host_to_contacts:
			contact_hosts = input("Host {}: ".format(infected_student.host[i])).split(" ")
			# Remove duplicate elements
			contact_hosts = list(dict.fromkeys(contact_hosts))
			# Remove host itself if given as input
			if infected_student.host[i] in contact_hosts:
				contact_hosts.remove(infected_student.host[i])
			# Add to dict
			map_host_to_contacts[infected_student.host[i]] = contact_hosts
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

def get_contacts(data, contact_hosts):
	"""
	Gets the contact hosts.
	"""
	contact_students: List[Student] = []
	for infected_host, contact_host in contact_hosts.items():
		print("------------------------- contact_host = {}".format(contact_host))
		for session in data:
			if session["host"] in contact_host:
				i = is_in_students_list(contact_students, session["user"]["login"])
				if i == -1:
					student = Student(session["user"]["login"])
					student.append_session(session["id"], session["host"], session["begin_at"], session["end_at"])
					contact_students.append(student)
					print("Append new student: {} {}".format(session["user"]["login"], session["id"]))
				else:
					if session["id"] not in contact_students[i].session_id:
						contact_students[i].append_session(session["id"], session["host"], session["begin_at"], session["end_at"])
						print("Appending session to {} {}".format(session["user"]["login"], session["id"]))

	return (contact_students)

def get_overlap_between_contacts(contact_students: List[Student], infected_student: InfectedStudent):

	total_overlap: Dict[str, int] = {}
	for j in range(len(infected_student.session_id)): # loop over infected student sessions
		print("session {} on {}.".format(infected_student.session_id[j], infected_student.host[j]))
		for contact_student in contact_students: # loop over contact students
			print("contact_student = {}".format(contact_student.login))
			total_overlap_seconds: int = 0
			for i in range(len(contact_student.session_id)): # loop over sessions of contact student
				#print("overlap {}, {}".format(contact_student.session_id[i]))
				overlap = get_overlap_time(contact_student.begin_at[i], contact_student.end_at[i], infected_student.begin_at[j], infected_student.end_at[j])
				if overlap.days >= 0:
					total_overlap_seconds += overlap.seconds
					print("session: {}, {} sat on {} between {} and {} which overlaps with {} for {} hours".format(contact_student.session_id[i], contact_student.login, contact_student.host[i], contact_student.begin_at[i], contact_student.end_at[i], infected_student.login, overlap))
			if contact_student.login in total_overlap:
				total_overlap[contact_student.login] += total_overlap_seconds
			else:
				total_overlap[contact_student.login] = total_overlap_seconds

	total_overlap = {login: overlap for login, overlap in total_overlap.items() if overlap > 0}
	return (total_overlap)