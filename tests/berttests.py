#!/usr/bin/env python

import datetime
import re
import unittest

from bert import BERTDecoder, BERTEncoder

bert_tests = [
    # nil
    (None, ("bert", "nil")),
    # nested nil
    ([None, (None,)], [("bert", "nil"), (("bert", "nil"),)]),
    # dict
    ({'foo': 'bar'}, ('bert', 'dict', [('foo', 'bar')])),
    # empty dict
    ({}, ('bert', 'dict', [])),
    # nested dict
    ({'foo': {'baz': 'bar'}}, ('bert', 'dict', [('foo', ('bert', 'dict', [('baz', 'bar')]))])),
    # true
    (True, ('bert', 'true')),
    # false
    (False, ('bert', 'false')),
    # time
    (datetime.datetime.utcfromtimestamp(123*1000000+456).replace(microsecond=789), ('bert', 'time', 123, 456, 789)),
    # regex
    # (re.compile('^c(a)t$', re.I|re.X), ('bert', 'regex', '^c(a)t$', ('caseless', 'extended'))),
    # other
    ([1, 2.0, ("foo", "bar")], [1, 2.0, ("foo", "bar")]),
]

class BERTTestCase(unittest.TestCase):
    def testDecode(self):
        convert = BERTDecoder().convert
        for python, bert in bert_tests:
            self.failUnlessEqual(python, convert(bert))

    def testEncode(self):
        convert = BERTEncoder().convert
        for python, bert in bert_tests:
            self.failUnlessEqual(bert, convert(python))

    def testRegex(self):
        convert = BERTDecoder().convert
        before = ('bert', 'regex', '^c(a)t$', ('caseless', 'extended'))
        # after = re.compile('^c(a)t$', re.I|re.X)
        # self.failUnlessEqual(after, self.convert(before))
        self.failUnlessEqual(str(type(convert(before))), "<type '_sre.SRE_Pattern'>")

if __name__ == '__main__':
    unittest.main()
