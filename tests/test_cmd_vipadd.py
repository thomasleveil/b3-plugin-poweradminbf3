# -*- encoding: utf-8 -*-
# http://www.voidspace.org.uk/python/mock/mock.html
from mockito import when, verify
from b3.config import CfgConfigParser
from b3.parsers.frostbite2.protocol import CommandFailedError
from poweradminbf3 import Poweradminbf3Plugin
from tests import Bf3TestCase


class Test_cmd_vipadd(Bf3TestCase):
    def setUp(self):
        super(Test_cmd_vipadd, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""[commands]
vipadd: 0
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()


    def test_missing_parameter(self):
        self.superadmin.connects('superadmin')
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!vipadd')
        self.assertEqual(['Usage: !vipadd <player>'], self.superadmin.message_history)

    def test_non_existing_player(self):
        self.superadmin.connects('superadmin')
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!vipadd bar')
        self.assertEqual(['bar is now a VIP'], self.superadmin.message_history)


    def test_frostbite_error(self):
        self.joe.connects("joe")
        self.superadmin.connects('superadmin')
        when(self.console).write(('reservedSlotsList.add', 'Joe')).thenRaise(CommandFailedError(['f00']))
        self.superadmin.clearMessageHistory()
        self.superadmin.says("!vipadd joe")
        self.assertEqual(["Error: ['f00']"], self.superadmin.message_history)


    def test_nominal(self):
        when(self.console).write()
        self.joe.connects('Joe')
        self.superadmin.connects('superadmin')
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!vipadd joe')
        self.assertEqual(['Joe is now a VIP'], self.superadmin.message_history)
        verify(self.console).write(('reservedSlotsList.add', 'Joe'))

