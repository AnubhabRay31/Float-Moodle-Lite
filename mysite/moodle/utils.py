from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Uploada

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, uploadas):
		uploads_per_day = uploadas.filter(start_time__day=day)

		uploads_end_day = uploadas.filter(end_time__day=day)

		d = ''

		for upload in uploads_per_day:
			d += f'<li> {upload.title}-{upload.course_code}-(start) </li>'

		for upload in uploads_end_day:
			d += f'<li> {upload.title}-{upload.course_code}-(end) </li>'

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, uploadas):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, uploadas)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		uploads = Uploada.objects.filter(start_time__year=self.year, start_time__month=self.month)

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, uploads)}\n'
		return cal