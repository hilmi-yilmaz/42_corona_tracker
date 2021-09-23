import argparse
from datetime import datetime, timedelta
from typing import List, Dict

from corona_tracker_42.api42_wrapper import API42
from corona_tracker_42.get_contacts import InfectedStudent
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

# contact = GetContacts(args.infected_person_login, args.day_positive, args.days)
# contact.get_contacts()

# Create an API42 object to make calls with
api = API42()

# Get data from the API from the past few days
date_range: str = "{},{}".format((args.day_positive - timedelta(days=args.days_to_check)).strftime("%Y-%m-%dT%H:%M:%SZ"), args.day_positive.strftime("%Y-%m-%dT%H:%M:%SZ"))
print(date_range)
payload = {"filter[campus_id]": api.campus_id, "range[begin_at]": date_range, "page[size]": 100}
data: List[Dict] = api.get("locations", payload)

# Create an object containing information on the student
infected_student = InfectedStudent(args.infected_person_login, args.day_positive, args.days_to_check)

# Get sessions of the infected person
infected_student.get_sessions(data)

print(infected_student.login)
print(infected_student.session_id)
print(infected_student.host)
print(infected_student.begin_at)
print(infected_student.end_at)
print(infected_student.day_positive)
print(infected_student.days_to_check)


# Get the student who sat close to the infected person
#date_range_contacts = "{},{}".format((student.day_positive - timedelta(days=student.days_to_check + 1)).strftime("%Y-%m-%dT%H:%M:%SZ"), student.day_positive.strftime("%Y-%m-%dT%H:%M:%SZ"))
#get_contacts(api, infected_sessions, date_range_contacts)





