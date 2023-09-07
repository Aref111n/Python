import datetime
import time
from dateutil import parser

def get_unix_timestamp(year, month, day):
    date_obj = datetime.date(year, month, day)
    timestamp = time.mktime(date_obj.timetuple())
    return int(timestamp)


def extract_date_components(date_string):
    month_mapping = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
    }

    # Remove leading text if present
    date_string = date_string.replace("Date: ", "")

    parsed_date = parser.parse(date_string)

    day = parsed_date.day
    month_abbreviation = parsed_date.strftime("%b")
    month = month_mapping[month_abbreviation]
    year = parsed_date.year
    hour = parsed_date.hour
    minute = parsed_date.minute
    second = parsed_date.second

    return day, month, year, hour, minute, second
