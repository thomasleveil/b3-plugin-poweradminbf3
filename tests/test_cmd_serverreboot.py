# -*- encoding: utf-8 -*-
import time
from mock import patch
from mockito import when, verify
from b3.config import CfgConfigParser
from b3.parsers.frostbite2.protocol import CommandFailedError
from poweradminbf3 import Poweradminbf3Plugin
from tests import Bf3TestCase

@patch.object(time, 'sleep')
class Test_cmd_serverreboot(Bf3TestCase):
    def setUp(self):
        super(Test_cmd_serverreboot, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""[commands]
serverreboot: 100
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()


    def test_nominal(self, sleep_mock):
        when(self.console).write()
        self.superadmin.connects("god")
        self.superadmin.says("!serverreboot")
        verify(self.console).write(('admin.shutDown',))

    def test_frostbite_error(self, sleep_mock):
        when(self.console).write(('admin.shutDown',)).thenRaise(CommandFailedError(['fOO']))
        self.superadmin.connects("god")
        self.superadmin.message_history = []
        self.superadmin.says("!serverreboot")
        self.assertEqual(['Error: fOO'], self.superadmin.message_history)

