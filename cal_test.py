import calendar

# strings to add to the output HTML to set styles
to_prepend = '''
<html>
<head>
<style>
td.inactive {
    background-color: linen;
}
</style>
</head>
'''

to_append = '''
</html>
'''


# Subclass a calendar - we will change how it returns dates, HTMLCalendar since you want it similar to github
class ActivityCalendar(calendar.HTMLCalendar):
    def __init__(self, starting_day=calendar.SUNDAY, dates_activity={}):
        # in this example dates_activity is just a list of ints to keep it simple, could pass in a dict of dates/counts
        super(ActivityCalendar, self).__init__(starting_day)
        self.current_month = None
        self.current_year = None
        self.parsed_dates_activity = {}
        self.add_activity_dates(dates_activity)

    def add_activity_dates(self, dates_activity):
        for key in dates_activity.keys():
            count = dates_activity[key]
            month, date, year = (int(s) for s in key.split(r'/'))
            if year not in self.parsed_dates_activity.keys():
                self.parsed_dates_activity[year] = {}
            if month not in self.parsed_dates_activity[year].keys():
                self.parsed_dates_activity[year][month] = {}
            if date not in self.parsed_dates_activity[year][month].keys():
                self.parsed_dates_activity[year][month][date] = count
            else:
                # Add count if multiple entries of same day
                self.parsed_dates_activity[year][month][date] += count

    def formatyear(self, theyear, width=3):
        self.current_year = theyear
        return super(ActivityCalendar, self).formatyear(theyear, width)

    def formatmonth(self, theyear, themonth, withyear=True):
        self.current_year = theyear
        self.current_month = themonth
        return super(ActivityCalendar, self).formatmonth(theyear, themonth, withyear)

    def formatday(self, day, weekday):
        # Override the formatday method to check if the day is in our list of active days and sets the css class
        if day == 0: # calendar leaves the 0th index as a 'blank day'
            return '<td class="noday"&nbsp;</td>'
        css = 'class="inactive"'
        if day in self.parsed_dates_activity[self.current_year][self.current_month].keys():
            count = self.parsed_dates_activity[self.current_year][self.current_month][day]
            # set color depending on count -- this doesn't look very good, but its a start
            count = 255 if count > 255 else count
            css = 'bgcolor="rgb(%s, %s, %s)"' % (count, count - count/2, count/2)
        return '<td %s><a href="%s">%d</a></td>' % (css, weekday, day)

    def add_activity(self, date, count):
        # add a date of activity
        self.add_activity_dates({date: count})

# Create HTML for an ActivityCalendar, sunday the first day of the week, arbitrary activity
my_cal = ActivityCalendar(calendar.SUNDAY, {"08/29/2015": 100,
                                            "08/30/2015": 5,
                                            "09/03/2015": 210,
                                            "09/04/2015": 20,
                                            "09/06/2015": 245})
html = my_cal.formatmonth(2015, 8, True)
html += r'<br>'
html += my_cal.formatmonth(2015, 9, True)
html = to_prepend + html  # prepend the css and html tags
print html


my_cal.add_activity("08/20/2015", 200)
my_cal.add_activity("09/09/2015", 40)
# add to an existing day to test add count
my_cal.add_activity("09/04/2015", 80)

html = my_cal.formatmonth(2015, 8, True)
html += r'<br>'
html += my_cal.formatmonth(2015, 9, True)
html += to_append  # append closing html tag
print html
