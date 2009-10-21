#!/usr/bin/env python

import datetime
import re
import unittest

from bert import BERTDecoder

class BERTDecoderTest(unittest.TestCase):
    def setUp(self):
        self.decoder = BERTDecoder()

    def tearDown(self):
        pass

    def testNone(self):
        self.failUnlessEqual(None, self.convert(("bert", "nil")))

    def testNestedNone(self):
        self.failUnlessEqual([None, (None,)], self.convert([("bert", "nil"), (("bert", "nil"),)]))

    def testDict(self):
        self.failUnlessEqual({'foo': 'bar'}, self.convert(('bert', 'dict', [('foo', 'bar')])))

    def testEmptyDict(self):
        self.failUnlessEqual({}, self.convert(('bert', 'dict', [])))

    def testNestedDict(self):
        self.failUnlessEqual({'foo': {'baz': 'bar'}},
            self.convert(
                ('bert', 'dict', [
                    ('foo', ('bert', 'dict', [
                        ('baz', 'bar')]))])))

    def testTrue(self):
        self.failUnlessEqual(True, self.convert(('bert', 'true')))

    def testFalse(self):
        self.failUnlessEqual(False, self.convert(('bert', 'false')))

    def testTime(self):
        self.failUnlessEqual(datetime.timedelta(seconds=123*1000000+456, microseconds=789),
            self.convert(('bert', 'time', 123, 456, 789)))

    def testRegex(self):
        before = ('bert', 'regex', '^c(a)t$', ('caseless', 'extended'))
        # after = re.compile('^c(a)t$', re.I|re.X)
        # self.failUnlessEqual(after, self.convert(before))
        self.failUnlessEqual(str(type(self.convert(before))), "<type '_sre.SRE_Pattern'>")

    def testOther(self):
        """Conversion shouldn't change non-bert values"""
        before = [1, 2.0, ("foo", "bar")]
        self.failUnlessEqual(before, self.convert(before))

    def convert(self, term):
        return self.decoder.convert(term)

if __name__ == '__main__':
    unittest.main()
