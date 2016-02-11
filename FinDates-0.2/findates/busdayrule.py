"""
Business day conventions on date rolling
Where to move payment if payment day falls on a holiday
"""

import datetime

import dateutils

def _roll_forward(dt, calendar):
    rolled = dt
    while calendar.is_holiday(rolled):
        rolled += datetime.timedelta(days = 1)
    return rolled


def _roll_backward(dt, calendar):
    rolled = dt
    while calendar.is_holiday(rolled):
        rolled -= datetime.timedelta(days = 1)
    return rolled


def rolldate(dt, calendar, convention):
    """ Roll date to the business day

    Roll date of the date to the business day according to the convention.
    For 'follow' convention, if date falls on a holiday, finds first working day after it
    For 'previous' convention, if date falls on a holiday, finds latest working day before it
    For 'modfollow' convention, if date falls on a holiday, finds first working day after it, unless date is the end of month in which case previous workday is found
    For 'previous' convention, if date falls on a holiday, finds latest working day before it, unless date is the beginning of month in which case following workday is found

    Parameters
    ----------
    dt: datetime.date, datetime.datetime or date string
    calendar: Calendar object that has is_holiday method
    convention: one of 'follow', 'previous', 'modfollow', 'modprevious'

    Returns
    -------
    datetime.datetime of the next business day according to the convention
    """
    convention = convention.lower()
    dt = dateutils.asdatetime(dt)
    rolled = dt
    if convention == "follow":
        rolled = _roll_forward(dt, calendar)
    elif convention == 'modfollow':
        rolled = _roll_forward(dt, calendar)
        if rolled.month > dt.month:
            rolled = _roll_backward(dt, calendar)
    elif convention == 'previous':
        rolled = _roll_backward(dt, calendar)
    elif convention == 'modprevious':
        rolled = _roll_backward(dt, calendar)
        if rolled.month < dt.month:
            rolled = _roll_forward(dt, calendar)
    return rolled

def lbusdate(year, month, calendar):
    """ Last business day of the month
    """
    dt = dateutils.eom(year, month)
    return _roll_backward(dt, calendar)

def fbusdate(year, month, calendar):
    """ First business day of the month
    """
    dt = datetime.datetime(year, month, 1)
    return _roll_forward(dt, calendar)