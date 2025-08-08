import pytz
import datetime as dt
from dateutil import parser
def parse_date_time_string_or_object_and_localize_to_timezone(datetime,timezone='UTC',returns='timestamp'):
    if not datetime:
        return None
    if type(datetime).__name__=='datetime':
        dt_obj=pytz.timezone(timezone).localize(datetime)
    if type(datetime).__name__=='str':
        if datetime=='use_current_date_time':

            dt_obj=pytz.timezone(timezone).localize(dt.datetime.now())
        else:
            if parser.parse(datetime).tzinfo is not None:
                _dt=parser.parse(datetime)
                dt_obj=_dt.replace(tzinfo=pytz.timezone(timezone))
            else:
                dt_obj=pytz.timezone(timezone).localize(parser.parse(datetime))
    if returns=='timestamp':
        return dt_obj.timestamp()
    else:
        return dt_obj

def parse_time_stamp_to_datetime_and_localize_to_timezone(timestamp,timezone='UTC'):
    timezone=pytz.timezone(timezone)
    return dt.datetime.fromtimestamp(timestamp,timezone)

def get_time_difference_between_two_datetime_objects(dt1,dt2):
    delta=dt2-dt1
    return delta.total_seconds()

def main(input,usage='clean',batch=None):
    if parse_date_time_string_or_object_and_localize_to_timezone(input):
        return True
    else:
        if parse_time_stamp_to_datetime_and_localize_to_timezone(input):
            return True
    return False
    
