def create_exception_report_entry(log):
    """
    Parses a log entry to create a standardized exception report dictionary.

    Args:
        log (dict): The log entry dictionary.

    Returns:
        dict: A dictionary containing parsed exception information.
    """
    # Initialize variables with default values
    exception_name = 'Unknown'
    exception_message = 'No specific message'
    traceback_info = log.get('traceback', 'N/A')

    # Get the potential exception information from the 'string' key
    exception_info = log.get('string')

    # Handle the two primary cases for exception_info
    if isinstance(exception_info, dict):
        # Case 1: exception_info is a dictionary
        exception_name = exception_info.get('name', log.get('type', 'Unknown'))
        
        # Safely extract the message, handling different formats
        message_data = exception_info.get('args') or exception_info.get('message')
        if isinstance(message_data, (list, tuple)):
            exception_message = ' '.join(map(str, message_data))
        elif isinstance(message_data, str):
            exception_message = message_data
    elif isinstance(exception_info, str):
        # Case 2: exception_info is a string, treat it as the message
        exception_message = exception_info
        exception_name = log.get('type', 'Unknown')
    
    # Fallback to keys directly in the main log for additional info
    if exception_name == 'Unknown' and log.get('name'):
        exception_name = log.get('name')
    if exception_message == 'No specific message' and log.get('message'):
        exception_message = log.get('message')

    # Construct the final report dictionary
    return {
        "type": log.get('type', 'Exception'),
        "name": exception_name,
        "message": exception_message,
        "traceback": traceback_info
    }

def make_datetimes_timezone_aware(dt1,  timezone_str='UTC'):
    import datetime
    import pytz
    """
    Converts two datetime objects to be timezone-aware in the specified timezone.

    If a datetime object is naive (has no timezone information), it will be
    localized to the given timezone. If it is already timezone-aware, it will
    be converted to the given timezone.

    Args:
        dt1 (datetime.datetime): The first datetime object.
        dt2 (datetime.datetime): The second datetime object.
        timezone_str (str): The IANA timezone string (e.g., 'UTC', 'America/New_York',
                            'Europe/London'). Defaults to 'UTC'.

    Returns:
        tuple: A tuple containing the two timezone-aware datetime objects (dt1_aware, dt2_aware).

    Raises:
        pytz.UnknownTimeZoneError: If the provided timezone_str is not a valid IANA timezone.
        TypeError: If dt1 or dt2 are not datetime.datetime objects.
    """
    if not isinstance(dt1, datetime.datetime):
        raise TypeError("Both dt1 and dt2 must be datetime.datetime objects.")

    try:
        target_timezone = pytz.timezone(timezone_str)
    except pytz.UnknownTimeZoneError:
        raise pytz.UnknownTimeZoneError(f"Unknown timezone: '{timezone_str}'. "
                                       "Please provide a valid IANA timezone string.")

    # Helper function to process a single datetime object
    def process_datetime(dt_obj, tz):
        if dt_obj.tzinfo is None or dt_obj.tzinfo.utcoffset(dt_obj) is None:
            # Naive datetime: localize it
            return tz.localize(dt_obj)
        else:
            # Timezone-aware datetime: convert it to the target timezone
            return dt_obj.astimezone(tz)

    dt1_aware = process_datetime(dt1, target_timezone)
    

    return dt1_aware