import argparse
from datetime import datetime, timedelta
from typing import List, Dict

from corona_tracker_42.api42_wrapper import API42
from corona_tracker_42.students import InfectedStudent, Student
from corona_tracker_42.utils import *

# Parse the command line arguments
parser = argparse.ArgumentParser(
    description="List people that sat close to a recently infected person at Codam.")
parser.add_argument("infected_person_login", type=str,
                    help="The intra login of the infected person.")
parser.add_argument("day_positive", type=lambda s: datetime.strptime(s, '%d-%m-%Y').date(),
                    help="The day the person tested positive. Format: day-month-year e.g. 09-12-2021.")
parser.add_argument("days_to_check", type=int,
                    help="For how many previous days to check.")
args = parser.parse_args()

# Create an API42 object to make calls with
api = API42()

# Get data from the API from the past few days (add one so we can check contact that may have overlap but begin_at is the day before)
date_range: str = "{},{}".format((args.day_positive - timedelta(days=args.days_to_check)).strftime("%Y-%m-%dT%H:%M:%SZ"), args.day_positive.strftime("%Y-%m-%dT%H:%M:%SZ"))
payload = {"filter[campus_id]": api.campus_id, "range[begin_at]": date_range, "page[size]": 100}
data: List[Dict] = api.get("locations", payload)

# Create an object containing information on the student
infected_student = InfectedStudent(args.infected_person_login, args.day_positive, args.days_to_check)

# Get sessions on infected person
for session in data:
	if session["user"]["login"] == infected_student.login:
		infected_student.append_session(session["id"], session["host"], session["begin_at"], session["end_at"])


# Get contacts from the user
contacts: Dict[str, List[str]] = get_contact_hosts(infected_student)

# Get contacts persons
contact_students: List[Student] = []
for infected_host, contact in contacts.items():
	for session in data:
		if session["host"] in contact:
			i = is_in_students_list(contact_students, session["user"]["login"])
			if i == -1:
				student = Student(session["user"]["login"])
				student.append_session(session["id"], session["host"], session["begin_at"], session["end_at"])
				contact_students.append(student)
			else:
				contact_students[i].append_session(session["id"], session["host"], session["begin_at"], session["end_at"])

# Get the overlap times between the infected person and the contact persons

total_overlap: Dict[str, int] = {}
for j in range(len(infected_student.session_id)):
	for contact_student in contact_students:
		total_overlap_seconds: int = 0
		for i in range(len(contact_student.session_id)):
			overlap = get_overlap_time(contact_student.begin_at[i], contact_student.end_at[i], infected_student.begin_at[j], infected_student.end_at[j])
			if overlap.days >= 0:
				total_overlap_seconds += overlap.seconds
		if contact_student.login in total_overlap:
			total_overlap[contact_student.login] += total_overlap_seconds
		else:
			total_overlap[contact_student.login] = total_overlap_seconds

for login, overlap in total_overlap.items():
	print("{} logged in for {} next to {}".format(login, str(timedelta(seconds=overlap)), infected_student.login))

# def print_student(student):

# 	print("---------------------------")
# 	print(student.login)
# 	for i in range(len(student.session_id)):
# 		print("{} till {}".format(student.begin_at[i], student.end_at[i]))

# print_student(infected_student)
# print_student(contact_students[0])