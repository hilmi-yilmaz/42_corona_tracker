from datetime import date, datetime, timedelta
from typing import List, Dict

def check_input(day_positive: date, days_to_check: int):
	"""
	Checks input from user.
	"""
	if not (check_day_positive(day_positive) and check_days_to_check(days_to_check)):
		return (False)
	return (True)

def check_day_positive(day_positive: date):
	"""
	Checks that the day_positive is present or past (not future).
	"""
	now = datetime.now().date()
	if day_positive > now:
		return (False)
	return (True)

def check_days_to_check(days_to_check: int):
	"""
	days_to_check has to be 0 or bigger.
	"""
	if days_to_check < 0:
		return (False)
	return (True)
	