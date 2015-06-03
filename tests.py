#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import re
import unittest

from bert import BERTDecoder, BERTEncoder, Atom
from bert.codec import utc_to_datetime, datetime_to_utc

class TestDateConversion(unittest.TestCase):
    test_dates = [
        (datetime.datetime(1970, 1, 1, 0, 0, 0, 0), (0, 0)),
        (datetime.datetime(2009, 1, 8, 4, 27, 47), (1231388867, 0)),
        (datetime.datetime(2009, 10, 8, 4, 27, 47, 123), (1254976067, 123)),
        (datetime.datetime(2009, 1, 8, 4, 27, 47, 456), (1231388867, 456)),
    ]

    def testToDatetime(self):
        for dt, tstamp in self.test_dates:
            self.assertEqual(dt, utc_to_datetime(tstamp[0], tstamp[1]))

    def testFromDatetime(self):
        for dt, tstamp in self.test_dates:
            self.assertEqual(tstamp, datetime_to_utc(dt))

class BERTTestCase(unittest.TestCase):
    bert_tests = [
        # nil
        (None, ("bert", "nil")),
        # nested nil
        ([None, (None,)], [("bert", "nil"), (("bert", "nil"),)]),
        # unicode
        (u"Mitä kuuluu", ('bert', 'string', Atom('UTF-8'), u"Mitä kuuluu".encode('utf-8'))),
        # dict
        ({'foo': 'bar'}, ('bert', 'dict', [('foo', 'bar')])),
        # empty dict
        ({}, ('bert', 'dict', [])),
        # nested dict
        ({'foo': {'baz': 'bar'}}, ('bert', 'dict', [('foo', ('bert', 'dict', [('baz', 'bar')]))])),
        # empty tuple
        (tuple(), tuple()),
        # true
        (True, ('bert', 'true')),
        # false
        (False, ('bert', 'false')),
        # time
        (datetime.datetime.utcfromtimestamp(123*1000000+456).replace(microsecond=789), ('bert', 'time', 123, 456, 789)),
        # regex
        (re.compile('^c(a)t$', re.I|re.X), ('bert', 'regex', '^c(a)t$', (Atom('extended'), Atom('caseless')))),
        # other
        ([1, 2.0, ("foo", "bar")], [1, 2.0, ("foo", "bar")]),
    ]

    def testDecode(self):
        convert = BERTDecoder().convert
        for python, bert in self.bert_tests:
            self.assertEqual(python, convert(bert))

    def testEncode(self):
        convert = BERTEncoder().convert
        for python, bert in self.bert_tests:
            self.assertEqual(bert, convert(python))

if __name__ == '__main__':
    unittest.main()
