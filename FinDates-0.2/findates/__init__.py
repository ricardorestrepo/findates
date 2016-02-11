"""
FinDates
========

Provides
    1. Utility functions to work with dates missing from 'datetime' and 'calendar'
    2. Calendar class to define holiday calendars for various countries, regions, and
       exchanges with natural language
    3. Day counting conventions to calculate year fractions between dates
    4. Business day rolling conventions (FOLLOW, MODFOLLOW, PREVIOUS, MODPREVIOUS)

"""

from dateutils import *
from busdayrule import *
from daycount import *
from holidays import *