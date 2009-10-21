#!/usr/bin/env python

import unittest

from bert import ErlangTermDecoder, Atom, Binary

class ErlangDecoderTest(unittest.TestCase):
    def setUp(self):
        self.decoder = ErlangTermDecoder()

    def testNil(self):
        decoded = self.decode([131, 106])
        self.failUnlessEqual([], decoded)
        self.failUnless(isinstance(decoded, list))

    def testBinary(self):
        decoded = self.decode([131,109,0,0,0,3,102,111,111])
        self.failUnlessEqual("foo", decoded)
        self.failUnless(isinstance(decoded, Binary))

    def testAtom(self):
        decoded = self.decode([131,100,0,3,102,111,111])
        self.failUnlessEqual("foo", decoded)
        self.failUnless(isinstance(decoded, Atom))

    def testAtomFalse(self):
        decoded = self.decode([131,100,0,4,116,114,117,101])
        self.failUnlessEqual(True, decoded)

    def testAtomFalse(self):
        decoded = self.decode([131,100,0,5,102,97,108,115,101])
        self.failUnlessEqual(False, decoded)

    def testString(self):
        decoded = self.decode([131,107,0,3,102,111,111])
        self.failUnlessEqual("foo", decoded)

    def testSmallInteger(self):
        decoded = self.decode([131,97,123])
        self.failUnlessEqual(123, decoded)

    def testInteger(self):
        decoded = self.decode([131,98,0,0,48,57])
        self.failUnlessEqual(12345, decoded)

    def testFloat(self):
        decoded = self.decode([131,99,49,46,50,51,52,52,57,57,57,57,57,57,57,57,57,57,57,57,51,48,55,50,101,43,48,48,0,0,0,0,0])
        self.failUnlessEqual(1.2345, decoded)

    def testFloat(self):
        decoded = self.decode([131,99,49,46,50,51,52,52,57,57,57,57,57,57,57,57,57,57,57,57,51,48,55,50,101,43,48,48,0,0,0,0,0])
        self.failUnlessEqual(1.2345, decoded)

    def testTuple(self):
        decoded = self.decode([131,104,3,100,0,3,102,111,111,107,0,4,116,101,115,116,97,123])
        self.failUnless(isinstance(decoded, tuple))
        self.failUnlessEqual(("foo", "test", 123), decoded)

    def testList(self):
        decoded = self.decode([131,108,0,0,0,3,98,0,0,4,0,107,0,4,116,101,115,116,99,
            52,46,48,57,54,48,48,48,48,48,48,48,48,48,48,48,48,48,
            56,53,50,55,101,43,48,48,0,0,0,0,0,106])
        self.failUnless(isinstance(decoded, list))
        self.failUnlessEqual([1024, "test", 4.096], decoded)

    def testSmallBig(self):
        decoded = self.decode([131,110,8,0,210,10,31,235,140,169,84,171])
        self.failUnlessEqual(12345678901234567890, decoded)

    def testLargeBig(self):
        decoded = self.decode([131,111,0,0,1,68,0,210,10,63,206,150,241,207,172,75,241,
            123,239,97,17,61,36,94,147,169,136,23,160,194,1,165,37,
            183,227,81,27,0,235,231,229,213,80,111,152,189,144,241,
            195,221,82,131,209,41,252,38,234,72,195,49,119,241,7,
            243,243,51,143,183,150,131,5,116,236,105,156,89,34,152,
            152,105,202,17,98,89,61,204,161,180,82,27,108,1,134,24,
            233,162,51,170,20,239,17,91,125,79,20,82,85,24,36,254,
            127,150,148,206,114,63,215,139,154,167,118,189,187,43,7,
            88,148,120,127,73,2,52,46,160,204,222,239,58,167,137,
            126,164,175,98,228,193,7,29,243,99,108,124,48,201,80,96,
            191,171,149,122,162,68,81,102,247,202,239,176,196,61,17,
            6,42,58,89,245,56,175,24,167,129,19,223,189,84,108,52,
            224,0,238,147,214,131,86,201,60,231,73,223,168,46,245,
            252,164,36,82,149,239,209,167,210,137,206,117,33,248,8,
            177,90,118,166,217,122,219,48,136,16,243,127,211,115,99,
            152,91,26,172,54,86,31,173,48,41,208,151,56,209,2,230,
            251,72,20,57,220,41,46,181,146,246,145,65,27,205,184,96,
            66,198,4,131,76,192,184,175,78,43,129,237,236,63,59,31,
            171,49,193,94,74,255,79,30,1,135,72,15,46,90,68,6,240,
            186,107,170,103,86,72,93,23,230,73,46,66,20,97,50,193,
            59,209,43,234,46,228,146,21,147,233,39,69,208,40,205,
            144,251,16])
        self.failUnlessEqual(123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890, decoded)


    def decode(self, binaryterm):
        if isinstance(binaryterm, (list, tuple)):
            binaryterm = "".join(chr(x) for x in binaryterm)
        return self.decoder.decode(binaryterm)

if __name__ == '__main__':
    unittest.main()
