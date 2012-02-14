# -*- encoding: utf-8 -*-
import time
from unittest import expectedFailure
from mock import Mock, patch # http://www.voidspace.org.uk/python/mock/mock.html
from b3.config import XmlConfigParser
from b3.parsers.frostbite2.protocol import CommandFailedError
from poweradminbf3 import Poweradminbf3Plugin
from tests.unittests import Bf3TestCase, Mockito



class Test_cmd_endround(Bf3TestCase):

    @classmethod
    def setUpClass(cls):
        Bf3TestCase.setUpClass()
        cls.sleep_patcher = patch.object(time, "sleep")
        cls.sleep_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.sleep_patcher.stop()

    def setUp(self):
        Bf3TestCase.setUp(self)
        self.conf = XmlConfigParser()
        self.conf.loadFromString("""
        <configuration plugin="poweradminbf3">
            <settings name="commands">
                <set name="endround">20</set>
            </settings>
        </configuration>
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()
        self.superadmin.connects('superadmin')


    def test_frostbite_error(self):
        self.console.write = Mockito(wraps=self.console.write)
        self.console.write.expect(('mapList.endRound', 'foo')).thenRaise(CommandFailedError(['InvalidArguments']))
        self.superadmin.message_history = []
        self.superadmin.says("!endround foo")
        self.console.write.verify_expected_calls()
        self.assertEqual(['Error: InvalidArguments'], self.superadmin.message_history)


    def test_no_argument(self):
        self.console.write = Mockito(wraps=self.console.write)
        self.superadmin.message_history = []
        self.superadmin.says("!endround")
        self.console.write.verify_expected_calls()
        self.assertEqual(['missing TeamID'], self.superadmin.message_history)


    def test_0(self):
        self.console.write = Mockito(wraps=self.console.write)
        self.console.write.expect(('mapList.endRound', '0'))
        self.superadmin.says("!endround 0")
        self.console.write.verify_expected_calls()


    def test_1(self):
        self.console.write = Mockito(wraps=self.console.write)
        self.console.write.expect(('mapList.endRound', '0'))
        self.superadmin.says("!endround 0")
        self.console.write.verify_expected_calls()


