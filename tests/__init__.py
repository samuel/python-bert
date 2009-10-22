
import datetime
import unittest

from bert.converters import utc_to_datetime, datetime_to_utc

class TestDateConversion(unittest.TestCase):
    test_dates = [
        (datetime.datetime(1970, 1, 1, 0, 0, 0, 0), (0, 0)),
        (datetime.datetime(2009, 1, 8, 4, 27, 47), (1231388867, 0)),
        (datetime.datetime(2009, 10, 8, 4, 27, 47, 123), (1254976067, 123)),
        (datetime.datetime(2009, 1, 8, 4, 27, 47, 456), (1231388867, 456)),
    ]

    def testToDatetime(self):
        for dt, tstamp in self.test_dates:
            self.failUnlessEqual(dt, utc_to_datetime(tstamp[0], tstamp[1]))

    def testFromDatetime(self):
        for dt, tstamp in self.test_dates:
            self.failUnlessEqual(tstamp, datetime_to_utc(dt))
