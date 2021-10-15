import os

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