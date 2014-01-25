import redisdl
import subprocess
import unittest
import json
import os.path
from . import util

unicode_dump = {u'akey': {u'type': u'string', u'value': u'\u041c\u043e\u0441\u043a\u0432\u0430'}, u'lvar': {u'type': u'list', u'value': [u'\u041c\u043e\u0441\u043a\u0432\u0430']}, u'svar': {u'type': u'set', u'value': [u'\u041c\u043e\u0441\u043a\u0432\u0430']}, u'zvar': {u'type': u'zset', u'value': [[u'\u041c\u043e\u0441\u043a\u0432\u0430', 1.0]]}, u'hvar': {u'type': u'hash', u'value': {u'hkey': u'\u041c\u043e\u0441\u043a\u0432\u0430'}}}

class ProgramTest(unittest.TestCase):
    def setUp(self):
        import redis
        self.r = redis.Redis()
        for key in self.r.keys('*'):
            self.r.delete(key)

        self.program = os.path.join(os.path.dirname(__file__), '..', 'redisdl.py')

    def test_dump(self):
        path = os.path.join(os.path.dirname(__file__), 'fixtures', 'dump.json')
        with open(path) as f:
            dump = f.read()

        redisdl.loads(dump)

        redump = subprocess.check_output([self.program])

        expected = json.loads(dump)
        actual = json.loads(redump)

        self.assertEqual(expected, actual)

    def test_dump_unicode(self):
        redisdl.loads(json.dumps(unicode_dump))

        redump = subprocess.check_output([self.program])

        actual = json.loads(redump)

        self.assertEqual(unicode_dump, actual)

    def test_load(self):
        path = os.path.join(os.path.dirname(__file__), 'fixtures', 'dump.json')
        with open(path) as f:
            dump = f.read()

        subprocess.check_call([self.program, '-l', path])

        redump = redisdl.dumps()

        expected = json.loads(dump)
        actual = json.loads(redump)

        self.assertEqual(expected, actual)

    def test_load_unicode(self):
        path = os.path.join(os.path.dirname(__file__), 'fixtures', 'dump-unicode.json')
        with open(path) as f:
            dump = f.read()

        subprocess.check_call([self.program, '-l', path])

        redump = redisdl.dumps()

        actual = json.loads(redump)

        self.maxDiff = None
        self.assertEqual(unicode_dump, actual)
