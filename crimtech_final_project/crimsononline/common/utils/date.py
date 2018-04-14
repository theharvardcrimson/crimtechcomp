from calendar import timegm


def to_js_timestamp(datetime):
    """Converts a python datetime.datetime object to a Javascript timestamp

    Assumes UTC. Returns a Javascript-compatible timestamp, specified in number
    of milliseconds since the 1 Jan 1970.
    """
    time_in_seconds = timegm(datetime.timetuple())
    time_in_ms = int(time_in_seconds) * 1000
    return time_in_ms
