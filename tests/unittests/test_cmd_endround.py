# -*- encoding: utf-8 -*-
import unittest, time
from mock import Mock, patch # http://www.voidspace.org.uk/python/mock/mock.html
from b3.config import XmlConfigParser
from b3.fake import fakeConsole, superadmin
from b3.parsers.frostbite2.protocol import CommandFailedError
from b3.parsers.frostbite2.rcon import Rcon
from tests import prepare_fakeparser_for_tests
from poweradminbf3 import Poweradminbf3Plugin



class Test_cmd_endround(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        prepare_fakeparser_for_tests()
        cls.sleep_patcher = patch.object(time, "sleep")
        cls.sleep_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.sleep_patcher.stop()

    def setUp(self):
        self.conf = XmlConfigParser()
        self.conf.loadFromString("""
        <configuration plugin="poweradminbf3">
            <settings name="commands">
                <set name="endround">20</set>
            </settings>
        </configuration>
        """)
        self.p = Poweradminbf3Plugin(fakeConsole, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()

    def test_frostbite_error(self):
        # simulate Frostbite error

        original_write = self.p.console.write
        def myWrite(data):
            if type(data) in (tuple, list):
                if data[0] == 'mapList.endRound':
                    raise CommandFailedError(['InvalidArguments'])
            return original_write(data)
        self.p.console.write = Mock(side_effect=myWrite)

        superadmin.connects('superadmin')
        superadmin.message_history = []
        superadmin.says("!endround 0")

        self.assertEqual(1, len(superadmin.message_history), "expecting 1 message instead of %r" % superadmin.message_history)
        self.assertEqual("Error: InvalidArguments", superadmin.message_history[0])


    def test_no_argument(self):
        superadmin.connects('superadmin')
        superadmin.message_history = []
        superadmin.says("!endround")
        self.assertEqual(1, len(superadmin.message_history), "expecting 1 message instead of %r" % superadmin.message_history)
        self.assertEqual("missing TeamID", superadmin.message_history[0])

    def test_nominal_0(self):
        self.p.console.write = Mock()
        superadmin.connects('superadmin')
        superadmin.message_history = []
        superadmin.says("!endround 0")
        self.assertEqual(0, len(superadmin.message_history), "expecting 0 message instead of %r" % superadmin.message_history)
        self.p.console.write.assert_called_once_with(('mapList.endRound', '0'))


    def test_nominal_1(self):
        self.p.console.write = Mock()
        superadmin.connects('superadmin')
        superadmin.message_history = []
        superadmin.says("!endround 1")
        self.assertEqual(0, len(superadmin.message_history), "expecting 0 message instead of %r" % superadmin.message_history)
        self.p.console.write.assert_called_once_with(('mapList.endRound', '1'))

