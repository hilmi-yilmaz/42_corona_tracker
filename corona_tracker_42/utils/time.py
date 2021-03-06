from datetime import datetime, timedelta

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
