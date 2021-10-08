from typing import List, Tuple, Dict
from datetime import timedelta

def print_header(string: str, file):
	print((20 + len(string)) * "#", file=file)
	print("#" + (18 + len(string)) * " " + "#", file=file)
	print("#{}{}{}#".format(" " * 9, string, " " * 9), file=file)
	print("#" + (18 + len(string)) * " " + "#", file=file)
	print((20 + len(string)) * "#", file=file)
	print("", file=file)

def print_overlap_sessions(output: List[Tuple], file):
	for session in output:
		print("{0[0]:<15} {0[1]:<15} {0[2]:<20} {0[3]:<15} {0[4]:<15} {0[5]:<15} {0[6]:<25} {0[7]:<15}".format(session), file=file)
	print("", file=file)

def print_risky_students(risky_students: Dict[str, List], infected_student, file):
	"""
	risky_students example = {'f1r6s19.codam.nl': ['13:05:50', 'dnoom'], 'f1r2s13.codam.nl': ['0:21:36', 'bprovoos'], 'f1r2s11.codam.nl': ['13:06:00', 'bprovoos']}
	"""
	if not risky_students:
		print("None.", file=file)
	infected_hosts = list(set(infected_student.host))
	for host in infected_hosts:
		if host in risky_students:
			print("{:<15} sat on {} (infected person session id = {}) after {} hours passed.".format(risky_students[host][1], host, risky_students[host][2],str(timedelta(seconds=risky_students[host][0]))), file=file)
	print("", file=file)

def print_student(student, file):

	print(f"Sessions of {student.login}", file=file)
	for i in range(len(student.session_id)):
		print("\t-------------------------", file=file)
		print(f"\tSession ID : {student.session_id[i]}",  file=file)
		print(f"\tHost       : {student.host[i]}",  file=file)
		print(f"\tBegin_at   : {student.begin_at[i].time()}", file=file)
		print(f"\tEnd_at     : {student.end_at[i].time()}", file=file)
		if (student.begin_at[i].date() == student.end_at[i].date()):
			print(f"\tDate       : {student.begin_at[i].date()}", file=file)
		else:
			print(f"\tDate       : {student.begin_at[i].date()} | {student.end_at[i].date()}", file=file)
		
	print("", file=file)

def print_data(total_overlap, output, infected_student, contact_students, risky_students):

	with open ("out.txt", 'w') as f:
		print_header("Summary of total login times", file=f)
		for login, overlap in total_overlap.items():
			print("{:<15} logged in for a total of {:<10} hours next to {}".format(login, str(timedelta(seconds=overlap)), infected_student.login), file=f)
		print("", file=f)
		print_header("Table containing sessions overlapping with infected person ({})".format(infected_student.login), file=f)
		print("{:<15} {:<15} {:<20} {:<15} {:<15} {:<15} {:<25} {:<15}".format("session_id", "login", "host", "begin_time", "end_time", "date", "host_infected_person", "overlap"), file=f)
		print("{}".format(134 * "-"), file=f)
		print_overlap_sessions(output, f)
		print_header("Student that sat on infected host", file=f)
		print_risky_students(risky_students, infected_student, file=f)
		print_header("Sessions of infected student", file=f)
		print_student(infected_student, f)
		print_header("Sessions of contact students", file=f)
		for contact, overlap in total_overlap.items():
			for student in contact_students:
				if student.login == contact:
					print_student(student, f)