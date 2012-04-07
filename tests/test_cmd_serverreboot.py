# -*- encoding: utf-8 -*-
import time
from mock import patch
from b3.config import XmlConfigParser
from b3.parsers.frostbite2.protocol import CommandFailedError
from poweradminbf3 import Poweradminbf3Plugin
from tests import Bf3TestCase

@patch.object(time, 'sleep')
class Test_cmd_serverreboot(Bf3TestCase):
    def setUp(self):
        super(Test_cmd_serverreboot, self).setUp()
        self.conf = XmlConfigParser()
        self.conf.loadFromString("""
        <configuration plugin="poweradminbf3">
            <settings name="commands">
                <set name="serverreboot">100</set>
            </settings>
        </configuration>
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()


    def test_nominal(self, sleep_mock):
        self.console.write.expect(('admin.shutDown',))
        self.superadmin.connects("god")
        self.superadmin.says("!serverreboot")
        self.console.write.verify_expected_calls()

    def test_frostbite_error(self, sleep_mock):
        self.console.write.expect(('admin.shutDown',)).thenRaise(CommandFailedError(['fOO']))
        self.superadmin.connects("god")
        self.superadmin.message_history = []
        self.superadmin.says("!serverreboot")
        self.console.write.verify_expected_calls()
        self.assertEqual(['Error: fOO'], self.superadmin.message_history)

