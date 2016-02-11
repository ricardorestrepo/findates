import nose
import unittest

from findates import *

class HolidaysTestCase(unittest.TestCase):

    def dteq(self, datestr, y, m, d):
        return self.assertEqual(asdatetime(datestr), datetime.datetime(y, m, d))


    def test_asdatetime(self):
        self.dteq("4-Nov-1978", 1978, 11, 4)
        self.dteq("04-Nov-1978", 1978, 11, 4)
        self.dteq("4 Nov 1978", 1978, 11, 4)
        self.dteq("04 Nov 1978", 1978, 11, 4)
        self.dteq("4Nov1978", 1978, 11, 4)
        self.dteq("04Nov1978", 1978, 11, 4)
        self.dteq("19781104", 1978, 11, 4)

        self.dteq("1978-11-04", 1978, 11, 4)
        self.dteq("1978-11-4", 1978, 11, 4)
        self.dteq("1978-1-14", 1978, 1, 14)
        self.dteq("1978-1-4", 1978, 1, 4)

        self.dteq("04.11.1978", 1978, 11, 4)
        self.dteq("4.11.1978", 1978, 11, 4)
        self.dteq("04.11.1978", 1978, 11, 4)
        self.dteq("4.1.1978", 1978, 1, 4)

        self.dteq("11/04/78", 1978, 11, 4)
        self.dteq("11/4/78", 1978, 11, 4)
        self.dteq("1/23/78", 1978, 1, 23)
        self.dteq("1/4/78", 1978, 1, 4)

        self.dteq("11/04/1978", 1978, 11, 4)
        self.dteq("11/4/1978", 1978, 11, 4)
        self.dteq("1/14/1978", 1978, 1, 14)
        self.dteq("1/4/1978", 1978, 1, 4)

    def test_leapyear(self):
        self.assertTrue(leapyear(1980))
        self.assertFalse(leapyear(1900))
        self.assertTrue(leapyear(2000))
        self.assertTrue(leapyear(1600)) # before Gregorian calendar in Europe
        self.assertFalse(leapyear(1981))
        self.assertFalse(leapyear('1981-12-1'))
        self.assertFalse(leapyear(datetime.date(1981, 12, 1)))

    def test_iseom(self):
        self.assertTrue(iseom('31 Mar 2000'))
        self.assertFalse(iseom('30 Mar 2000'))
        self.assertFalse(iseom('28 Feb 2000'))
        self.assertTrue(iseom('28 Feb 1999'))
        self.assertTrue(iseom('29 Feb 2000'))
        self.assertTrue(iseom('31 Jan 2000'))
        self.assertTrue(iseom('30 Apr 2000'))
        self.assertTrue(iseom('31 May 2000'))
        self.assertTrue(iseom('30 Jun 2000'))
        self.assertTrue(iseom('31 Jul 2000'))
        self.assertTrue(iseom('31 Aug 2000'))
        self.assertTrue(iseom('30 Sep 2000'))
        self.assertTrue(iseom('31 Oct 2000'))
        self.assertTrue(iseom('30 Nov 2000'))
        self.assertTrue(iseom('31 Dec 2000'))

    def test_nweekday(self):
        self.assertEquals(lweekday(2011, 9, 6).day, 25)
        self.assertEquals(lweekday(2012, 1, 1).day, 31)
        self.assertEquals(nweekday(2011, 9, 1, 0).day, 5)
        self.assertEquals(nweekday(2012, 1, 1, 6).day, 1)
        self.assertEquals(nweekday(2012, 1, 1, 0).day, 2)
        self.assertEquals(nweekday(2012, 1, 2, 6).day, 8)
        self.assertEquals(nweekday(2012, 1, 2, 0).day, 9)

    def assertEaster(self, y, m, d):
        self.assertEqual(holidays.easter(y), datetime.datetime(y, m, d))


    def test_easter(self):
        self.assertEaster(1961, 4, 2)
        self.assertEaster(2009, 4, 12)
        self.assertEaster(2012, 4, 8)

    def test_calendar_specificDates(self):
        cl = holidays.get_calendar('us')
        # Test holidays on a specific date
        # Independence Day
        self.assertTrue(cl.is_holiday('4 Jul 2000'))

    def test_calendar_easterBased(self):
        cl = holidays.get_calendar('ca')
        # Easter-based holidays
        #    Easter
        self.assertTrue(cl.is_holiday('8 Apr 2012'))
        #    Good Friday
        self.assertTrue(cl.is_holiday('06 Apr 2012'))

    def test_calendar_nthWeekday(self):
        cl = holidays.get_calendar('ca')
        # Labour day
        self.assertTrue(cl.is_holiday('3 Sep 2012'))

    def test_moveRules(self):
        cl = holidays.get_calendar('ca')
        # In 2011 Christmas day was moved to Tuesday Dec 27th as it happened on Sunday
        # and Monday was a Boxing Day
        self.assertTrue(cl.is_holiday('27 Dec 2011'))
        # Canada Day in 2012 is on Sunday
        self.assertTrue(cl.is_holiday('02 Jul 2012'))

class RolldateTestCase(unittest.TestCase):
    def test_rolldate(self):
        cal = holidays.get_calendar('ca')
        # test conventions on non-EOM holiday (Sat and Sun)
        self.assertEquals(busdayrule.rolldate('21 Jan 2012', cal, 'follow'), datetime.datetime(2012, 1, 23))
        self.assertEquals(busdayrule.rolldate('22 Jan 2012', cal, 'follow'), datetime.datetime(2012, 1, 23))
        self.assertEquals(busdayrule.rolldate('21 Jan 2012', cal, 'modfollow'), datetime.datetime(2012, 1, 23))
        self.assertEquals(busdayrule.rolldate('22 Jan 2012', cal, 'modfollow'), datetime.datetime(2012, 1, 23))

        self.assertEquals(busdayrule.rolldate('21 Jan 2012', cal, 'previous'), datetime.datetime(2012, 1, 20))
        self.assertEquals(busdayrule.rolldate('22 Jan 2012', cal, 'previous'), datetime.datetime(2012, 1, 20))
        self.assertEquals(busdayrule.rolldate('21 Jan 2012', cal, 'modprevious'), datetime.datetime(2012, 1, 20))
        self.assertEquals(busdayrule.rolldate('22 Jan 2012', cal, 'modprevious'), datetime.datetime(2012, 1, 20))

        # do not move non-holidays
        self.assertEquals(busdayrule.rolldate('23 Jan 2012', cal, 'follow'), datetime.datetime(2012, 1, 23))
        self.assertEquals(busdayrule.rolldate('23 Jan 2012', cal, 'previous'), datetime.datetime(2012, 1, 23))
        self.assertEquals(busdayrule.rolldate('23 Jan 2012', cal, 'modfollow'), datetime.datetime(2012, 1, 23))
        self.assertEquals(busdayrule.rolldate('23 Jan 2012', cal, 'modprevious'), datetime.datetime(2012, 1, 23))

        # EOM holidays
        self.assertEquals(busdayrule.rolldate('1 Apr 2012', cal, 'follow'), datetime.datetime(2012, 4, 2))
        self.assertEquals(busdayrule.rolldate('1 Apr 2012', cal, 'previous'), datetime.datetime(2012, 3, 30))
        self.assertEquals(busdayrule.rolldate('1 Apr 2012', cal, 'modprevious'), datetime.datetime(2012, 4, 2))
        self.assertEquals(busdayrule.rolldate('30 Jun 2012', cal, 'modfollow'), datetime.datetime(2012, 6, 29))

        self.assertEquals(busdayrule.lbusdate(2012, 6, cal), datetime.datetime(2012, 6, 29))
        self.assertEquals(busdayrule.lbusdate(2012, 1, cal), datetime.datetime(2012, 1, 31))
        self.assertEquals(busdayrule.fbusdate(2012, 1, cal), datetime.datetime(2012, 1, 3))
        self.assertEquals(busdayrule.fbusdate(2012, 4, cal), datetime.datetime(2012, 4, 2))
        self.assertEquals(busdayrule.fbusdate(2012, 2, cal), datetime.datetime(2012, 2, 1))

class DaycountTestCase(unittest.TestCase):
    def test_daycount_actact(self):
        self.assertEquals(daydiff('1 Dec 2002', '2 Dec 2002', 'actual/actual'), 1)
        self.assertEquals(daydiff('1 Dec 2002', '31 Dec 2002', 'actual/actual'), 30)
        self.assertEquals(daydiff('1 Jan 2002', '1 Jan 2003', 'actual/actual'), 365)
        self.assertEquals(daydiff('1 Jan 2004', '1 Jan 2005', 'actual/actual'), 366)
        self.assertEquals(daydiff('1 Jan 2004', '1 Jan 2006', 'actual/actual'), 731)
        self.assertEquals(yearfrac('1 Jan 2004', '1 Jan 2005', 'actual/actual'), 1.0)
        self.assertEquals(yearfrac('1 Jan 2003', '1 Jan 2004', 'actual/actual'), 1.0)

    def test_daycount_act365fixed(self):
        self.assertEquals(daydiff('1 Dec 2002', '2 Dec 2002', 'actual/365 fixed'), 1)
        self.assertEquals(daydiff('1 Dec 2002', '31 Dec 2002', 'actual/365 fixed'), 30)
        self.assertEquals(daydiff('1 Jan 2002', '1 Jan 2003', 'actual/365 fixed'), 365)
        self.assertEquals(daydiff('1 Jan 2004', '1 Jan 2005', 'actual/365 fixed'), 366)
        self.assertEquals(daydiff('1 Jan 2004', '1 Jan 2006', 'actual/365 fixed'), 731)
        self.assertGreater(yearfrac('1 Jan 2004', '1 Jan 2005', 'actual/365 fixed'), 1.0)
        self.assertEquals(yearfrac('1 Jan 2003', '1 Jan 2004', 'actual/365 fixed'), 1.0)

    def test_daycount_act365L(self):
        self.assertEquals(daydiff('1 Dec 2002', '2 Dec 2002', 'actual/365L'), 1)
        self.assertEquals(daydiff('1 Dec 2002', '31 Dec 2002', 'actual/365L'), 30)
        self.assertEquals(daydiff('1 Jan 2002', '1 Jan 2003', 'actual/365L'), 365)
        self.assertEquals(daydiff('1 Jan 2004', '1 Jan 2005', 'actual/365L'), 366)
        self.assertEquals(daydiff('1 Jan 2004', '1 Jan 2006', 'actual/365L'), 731)
        # 2004 is leap year so according to 365L plain, so we weill have 366 days
        # but denominator will be 365
        self.assertGreater(yearfrac('1 Jan 2004', '1 Jan 2005', 'actual/365L'), 1.0)
        # 2004 is leap year so according to 365L plain, we take denominator as 366
        self.assertLess(yearfrac('1 Jan 2003', '1 Jan 2004', 'actual/365L'), 1.0)
        # however if frequency is set to 'yearly', this works only if 29 feb is in the date rance
        self.assertEquals(yearfrac('1 Jan 2003', '1 Jan 2004', 'actual/365L', frequency='yearly'), 1.0)
        # between two non-leap years it is just 1.0
        self.assertEquals(yearfrac('1 Jan 2002', '1 Jan 2003', 'actual/365L'), 1.0)

    def test_daycount_actact_afb(self):
        self.assertEquals(daydiff('1 Dec 2002', '2 Dec 2002', 'actual/actual afb'), 1)
        self.assertEquals(daydiff('1 Dec 2002', '31 Dec 2002', 'actual/actual afb'), 30)
        self.assertEquals(daydiff('1 Jan 2002', '1 Jan 2003', 'actual/actual afb'), 365)
        self.assertEquals(daydiff('1 Jan 2004', '1 Jan 2005', 'actual/actual afb'), 366)
        self.assertEquals(daydiff('1 Jan 2004', '1 Jan 2006', 'actual/actual afb'), 731)

        self.assertEquals(yearfrac('1 Jan 2004', '1 Jan 2005', 'actual/actual afb'), 1.0)
        self.assertEquals(yearfrac('1 Jan 2003', '1 Jan 2004', 'actual/actual afb'), 1.0)
        self.assertEquals(yearfrac('1 Jan 2003', '1 Jan 2004', 'actual/actual afb'), 1.0)
        # 28/365 < 29/366
        self.assertLess(yearfrac('1 Feb 2003', '1 Mar 2003', 'actual/actual afb'),
                        yearfrac('1 Feb 2004', '1 Mar 2004', 'actual/actual afb'))

    def test_daycount_act360fixed(self):
        self.assertEquals(daydiff('1 Dec 2002', '2 Dec 2002', 'actual/360'), 1)
        self.assertEquals(daydiff('1 Dec 2002', '31 Dec 2002', 'actual/360'), 30)
        self.assertEquals(daydiff('1 Jan 2002', '1 Jan 2003', 'actual/360'), 365)
        self.assertEquals(daydiff('1 Jan 2004', '1 Jan 2005', 'actual/360'), 366)
        self.assertEquals(daydiff('1 Jan 2004', '1 Jan 2006', 'actual/360'), 731)
        self.assertGreater(yearfrac('1 Jan 2004', '1 Jan 2005', 'actual/360'), 1.0)
        self.assertGreater(yearfrac('1 Jan 2003', '1 Jan 2004', 'actual/360'), 1.0)

    def test_daycount_30e360(self):
        self.assertEquals(daydiff('1 Dec 2002', '31 Dec 2002', '30e/360'), 29)
        # difference between two end-of months (neither of which is February) in 30e/360 is 30
        self.assertEquals(daydiff('30 Nov 2002', '31 Dec 2002', '30e/360'), 30)
        self.assertEquals(daydiff('31 Aug 2002', '30 Sep 2002', '30e/360'), 30)

        self.assertEquals(daydiff('28 Feb 2002', '31 Mar 2002', '30e/360'), 32)
        self.assertEquals(daydiff('29 Feb 2004', '31 Mar 2004', '30e/360'), 31)
        self.assertEquals(daydiff('31 Jan 2002', '28 Feb 2002', '30e/360'), 28)
        self.assertEquals(daydiff('31 Jan 2004', '29 Feb 2004', '30e/360'), 29)

    def test_daycount_30360us(self):
        self.assertEquals(daydiff('1 Dec 2002', '31 Dec 2002', '30/360 us'), 30)
        # difference between two end-of months (neither of which is February)
        self.assertEquals(daydiff('30 Nov 2002', '31 Dec 2002', '30/360 us'), 30)
        self.assertEquals(daydiff('31 Aug 2002', '30 Sep 2002', '30/360 us'), 30)

        self.assertEquals(daydiff('28 Feb 2002', '31 Mar 2002', '30/360 us'), 33)
        self.assertEquals(daydiff('29 Feb 2004', '31 Mar 2004', '30/360 us'), 32)
        self.assertEquals(daydiff('31 Jan 2002', '28 Feb 2002', '30/360 us'), 28)
        self.assertEquals(daydiff('31 Jan 2004', '29 Feb 2004', '30/360 us'), 29)

    def test_daycount_30360us_eom(self):
        self.assertEquals(daydiff('1 Dec 2002', '31 Dec 2002', '30/360 us', eom=True), 30)
        # difference between two end-of months (neither of which is February)
        self.assertEquals(daydiff('30 Nov 2002', '31 Dec 2002', '30/360 us', eom=True), 30)
        self.assertEquals(daydiff('31 Aug 2002', '30 Sep 2002', '30/360 us', eom=True), 30)

        self.assertEquals(daydiff('28 Feb 2002', '31 Mar 2002', '30/360 us', eom=True), 30)
        self.assertEquals(daydiff('29 Feb 2004', '31 Mar 2004', '30/360 us', eom=True), 30)
        self.assertEquals(daydiff('31 Jan 2002', '28 Feb 2002', '30/360 us', eom=True), 28)
        self.assertEquals(daydiff('31 Jan 2004', '29 Feb 2004', '30/360 us', eom=True), 29)

        self.assertEquals(daydiff('29 Feb 2004', '28 Feb 2005', '30/360 us', eom=True), 360)
        self.assertEquals(daydiff('28 Feb 2003', '29 Feb 2004', '30/360 us', eom=True), 360)
        self.assertEquals(daydiff('28 Feb 2003', '28 Feb 2004', '30/360 us', eom=True), 358)

    def test_daycount_30e360isda(self):
        self.assertEquals(daydiff('1 Dec 2002', '31 Dec 2002', '30e/360 isda'), 29)
        # difference between two end-of months (neither of which is February)
        self.assertEquals(daydiff('30 Nov 2002', '31 Dec 2002', '30e/360 isda'), 30)
        self.assertEquals(daydiff('31 Aug 2002', '30 Sep 2002', '30e/360 isda'), 30)

        self.assertEquals(daydiff('28 Feb 2002', '31 Mar 2002', '30e/360 isda'), 30)
        self.assertEquals(daydiff('29 Feb 2004', '31 Mar 2004', '30e/360 isda'), 30)
        self.assertEquals(daydiff('31 Jan 2002', '28 Feb 2002', '30e/360 isda'), 28)
        self.assertEquals(daydiff('31 Jan 2004', '29 Feb 2004', '30e/360 isda'), 29)

    def test_daycount_30eplus360(self):
        self.assertEquals(daydiff('1 Dec 2002', '31 Dec 2002', '30e+/360'), 30)
        # difference between two end-of months (neither of which is February)
        self.assertEquals(daydiff('30 Nov 2002', '31 Dec 2002', '30e+/360'), 31)
        self.assertEquals(daydiff('31 Aug 2002', '30 Sep 2002', '30e+/360'), 30)

        self.assertEquals(daydiff('28 Feb 2002', '31 Mar 2002', '30e+/360'), 33)
        self.assertEquals(daydiff('29 Feb 2004', '31 Mar 2004', '30e+/360'), 32)
        self.assertEquals(daydiff('31 Jan 2002', '28 Feb 2002', '30e+/360'), 28)
        self.assertEquals(daydiff('31 Jan 2004', '29 Feb 2004', '30e+/360'), 29)


if __name__ == "__main__":
    nose.main()
