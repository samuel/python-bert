#!/usr/bin/env python

import unittest

from bert import erlang_encode, erlang_decode, Atom, Binary

erlang_term_binaries = [
    # nil
    ([], list, "\x83j"),
    # binary
    (Binary("foo"), Binary, '\x83m\x00\x00\x00\x03foo'),
    # atom
    (Atom("foo"), Atom, '\x83d\x00\x03foo'),
    # atom true
    (True, bool, '\x83d\x00\x04true'),
    # atom false
    (False, bool, '\x83d\x00\x05false'),
    # string
    ("foo", str, '\x83k\x00\x03foo'),
    # small integer
    (123, int, '\x83a{'),
    # integer
    (12345, int, '\x83b\x00\x0009'),
    # float
    (1.2345, float, '\x83c1.23449999999999993072e+00\x00\x00\x00\x00\x00'),
    # tuple
    ((Atom("foo"), "test", 123), tuple, '\x83h\x03d\x00\x03fook\x00\x04testa{'),
    # list
    ([1024, "test", 4.096], list, '\x83l\x00\x00\x00\x03b\x00\x00\x04\x00k\x00\x04testc4.09600000000000008527e+00\x00\x00\x00\x00\x00j'),
    # small big
    (12345678901234567890, long, '\x83n\x08\x00\xd2\n\x1f\xeb\x8c\xa9T\xab'),
    # large big
    (123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890,
     long, '\x83o\x00\x00\x01D\x00\xd2\n?\xce\x96\xf1\xcf\xacK\xf1{\xefa\x11=$^\x93\xa9\x88\x17\xa0\xc2\x01\xa5%\xb7\xe3Q\x1b\x00\xeb\xe7\xe5\xd5Po\x98\xbd\x90\xf1\xc3\xddR\x83\xd1)\xfc&\xeaH\xc31w\xf1\x07\xf3\xf33\x8f\xb7\x96\x83\x05t\xeci\x9cY"\x98\x98i\xca\x11bY=\xcc\xa1\xb4R\x1bl\x01\x86\x18\xe9\xa23\xaa\x14\xef\x11[}O\x14RU\x18$\xfe\x7f\x96\x94\xcer?\xd7\x8b\x9a\xa7v\xbd\xbb+\x07X\x94x\x7fI\x024.\xa0\xcc\xde\xef:\xa7\x89~\xa4\xafb\xe4\xc1\x07\x1d\xf3cl|0\xc9P`\xbf\xab\x95z\xa2DQf\xf7\xca\xef\xb0\xc4=\x11\x06*:Y\xf58\xaf\x18\xa7\x81\x13\xdf\xbdTl4\xe0\x00\xee\x93\xd6\x83V\xc9<\xe7I\xdf\xa8.\xf5\xfc\xa4$R\x95\xef\xd1\xa7\xd2\x89\xceu!\xf8\x08\xb1Zv\xa6\xd9z\xdb0\x88\x10\xf3\x7f\xd3sc\x98[\x1a\xac6V\x1f\xad0)\xd0\x978\xd1\x02\xe6\xfbH\x149\xdc).\xb5\x92\xf6\x91A\x1b\xcd\xb8`B\xc6\x04\x83L\xc0\xb8\xafN+\x81\xed\xec?;\x1f\xab1\xc1^J\xffO\x1e\x01\x87H\x0f.ZD\x06\xf0\xbak\xaagVH]\x17\xe6I.B\x14a2\xc1;\xd1+\xea.\xe4\x92\x15\x93\xe9\'E\xd0(\xcd\x90\xfb\x10'),
]

class ErlangTestCase(unittest.TestCase):
    def testDecode(self):
        for python, expected_type, erlang  in erlang_term_binaries:
            decoded = erlang_decode(erlang)
            self.failUnlessEqual(python, decoded)
            self.failUnless(isinstance(decoded, expected_type))

    def testEncode(self):
        for python, expected_type, erlang  in erlang_term_binaries:
            encoded = erlang_encode(python)
            self.failUnlessEqual(erlang, encoded)

if __name__ == '__main__':
    unittest.main()
