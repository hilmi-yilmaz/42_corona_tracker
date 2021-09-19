import argparse
from datetime import datetime
from corona_tracker_42.get_contacts import GetContacts

# Parse the command line arguments
parser = argparse.ArgumentParser(
    description="List people that sat close to a recently infected person at Codam.")
parser.add_argument("infected_person_login", type=str,
                    help="The intra login of the infected person.")
parser.add_argument("day_positive", type=lambda s: datetime.strptime(s, '%d-%m-%Y').date(),
                    help="The day the person tested positive. Format: day-month-year e.g. 09-12-2021.")
parser.add_argument("days", type=int,
                    help="For how many previous days to check.")
args = parser.parse_args()

contact = GetContacts(args.infected_person_login, args.day_positive, args.days)
contact.get_contacts()
