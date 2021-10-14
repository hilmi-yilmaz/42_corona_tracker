import readline
import sys
import os
from datetime import date, time, timedelta
from typing import List, Dict
from ..students import Student, InfectedStudent
from .time import *

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

def get_contact_suggestions(host: str):
	"""
	Makes a basic suggestion based on host (+1 and -1 location).
	"""
	host_list = list(host)
	contact_list = []
	if (host[6].isnumeric()):
		s = int(host[5:7])
		for i in [-1, 1]:
			host_list[5:7] = str(s + i)
			contact_list.append("".join(host_list))
	else:
		s = int(host[5])
		for i in [-1, 1]:
			host_list[5] = str(s + i)
			contact_list.append("".join(host_list))

	# If host not in hosts file, remove
	with open ("hosts") as f:
		data = f.read()
		contact_list = [contact for contact in contact_list if contact in data]
	return (contact_list)

def make_contact_suggestions(host: str):
	"""
	Interactive suggestion session.
	"""

	# Clear terminal screen
	os.system('cls' if os.name == 'nt' else 'clear')

	print("Infected student host: {}\n".format(host))

	# First make a suggestion to the user
	contact_hosts = get_contact_suggestions(host)

	print("Suggestions:")
	for contact in contact_hosts:
		print("--> {}".format(contact))

	print("\n1. Accept suggestions and continue.")
	print("2. Don't accept suggestions.")
	print("3. Accept and append to suggenstions.")

	while True:
		answer = input()
		if answer == "1" or answer == "2" or answer == "3":
			break

	if answer == "1":
		return (contact_hosts)
	elif answer == "2":
		contact_hosts = input("Host {}: ".format(host)).split(" ")
	elif answer == "3":
		contact_hosts +=  input("Host {}: ".format(host)).split(" ")
	return (contact_hosts)


def get_contact_hosts(infected_student, campus_id) -> Dict[str, List[str]]:
	"""
	Returns a mapping of infected hosts to contact hosts like:
	{"f1r1s1.codam.nl": [f1r1s2.codam.nl, f1r1s3.codam.nl], ...}

	Returns:
		contacts: (List[str]) list containing logins names of contact persons.
	"""

	i = 0
	map_host_to_contacts: Dict[str, List[str]] = {}
	for i in range(len(infected_student.session_id)):
		if infected_student.host[i] not in map_host_to_contacts:

			# Get contact hosts from user (+ suggentions)
			if campus_id == 14:
				contact_hosts = make_contact_suggestions(infected_student.host[i])
			else:
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

def get_contacts(data, contact_hosts, infected_student):
	"""
	Gets the contact students.
	"""
	contact_students: List[Student] = []
	for infected_host, contact_host in contact_hosts.items():
		for session in data:
			if session["host"] in contact_host and session["user"]["login"] != infected_student.login:
				i = is_in_students_list(contact_students, session["user"]["login"])
				if i == -1:
					student = Student(session["user"]["login"])
					student.append_session(session["id"], session["host"], session["begin_at"], session["end_at"])
					contact_students.append(student)
				else:
					if session["id"] not in contact_students[i].session_id:
						contact_students[i].append_session(session["id"], session["host"], session["begin_at"], session["end_at"])

	return (contact_students)

def get_overlap_between_contacts(contact_students: List[Student], contact_hosts: Dict[str, List[str]], infected_student: InfectedStudent):
	"""
	Calculate the overlap between the infected student and contact students.
	"""
	total_overlap: Dict[str, int] = {}
	output = []
	for j in range(len(infected_student.session_id)): # loop over infected student sessions
		c = contact_hosts[infected_student.host[j]] # list contains contact hosts for current infected session host
		for contact_student in contact_students: # loop over contact students
			total_overlap_seconds: int = 0
			for i in range(len(contact_student.session_id)): # loop over sessions of contact student
				if contact_student.host[i] not in c:
					continue
				overlap = get_overlap_time(contact_student.begin_at[i], contact_student.end_at[i], infected_student.begin_at[j], infected_student.end_at[j])
				if overlap.days >= 0:
					total_overlap_seconds += overlap.seconds
					output.append((contact_student.session_id[i], contact_student.login, contact_student.host[i], str(contact_student.begin_at[i].time()), str(contact_student.end_at[i].time()), str(contact_student.begin_at[i].date()), infected_student.host[j], str(overlap)))
			if contact_student.login in total_overlap:
				total_overlap[contact_student.login] += total_overlap_seconds
			else:
				total_overlap[contact_student.login] = total_overlap_seconds

	# Remove contacts with 0 overlapping time
	total_overlap = {login: overlap for login, overlap in total_overlap.items() if overlap > 0}
	return (total_overlap, output)

def get_student_sat_on_infected_host(data, infected_student) -> Dict[str, int]:
	"""
	Returns the student that sat on the computer where the infected host sat.
	"""
	student_sat_on_infected_host = {}
	for session in data:
		for i in range(len(infected_student.session_id)):		
			if session["host"] == infected_student.host[i] and session["user"]["login"] != infected_student.login:
				# student = Student(session["user"]["login"])
				# student.append_session(session["id"], session["host"], session["begin_at"], session["end_at"])
				time_elapsed = (str_to_datetime(session["begin_at"]) + timedelta(hours=2)) - infected_student.end_at[i]
				if time_elapsed.days >= 0:
					#print("login = {}, host = {}, begin_at = {}, time_elapsed = {}".format(session["user"]["login"], session["host"], str_to_datetime(session["begin_at"]) + timedelta(hours=2), time_elapsed))
					time_elapsed = time_elapsed.seconds + 86400 * time_elapsed.days
					if session["host"] in student_sat_on_infected_host:
						if time_elapsed < student_sat_on_infected_host[session["host"]][0]:
							student_sat_on_infected_host[session["host"]] = [time_elapsed, session["user"]["login"], infected_student.session_id[i]]
					else:
						student_sat_on_infected_host[session["host"]] = [time_elapsed, session["user"]["login"], infected_student.session_id[i]]
	return (student_sat_on_infected_host)
