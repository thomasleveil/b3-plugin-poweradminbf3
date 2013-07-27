# -*- encoding: utf-8 -*-
# http://www.voidspace.org.uk/python/mock/mock.html
from mockito import when, verify
from b3.config import CfgConfigParser
from b3.parsers.frostbite2.protocol import CommandFailedError
from poweradminbf3 import Poweradminbf3Plugin
from tests import Bf3TestCase


class Test_cmd_kill(Bf3TestCase):
    def setUp(self):
        super(Test_cmd_kill, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""[commands]
kill: 0
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()


    def test_frostbite_error(self):
        self.joe.connects("joe")
        self.superadmin.connects('superadmin')
        when(self.console).write(('admin.killPlayer', 'joe')).thenRaise(CommandFailedError(['f00']))

        self.superadmin.message_history = []
        self.superadmin.says("!kill joe")
        self.assertEqual(["Error: ['f00']"], self.superadmin.message_history)


    def test_frostbite_error_SoldierNotAlive(self):
        self.joe.connects("joe")
        self.superadmin.connects('superadmin')
        when(self.console).write(('admin.killPlayer', 'joe')).thenRaise(CommandFailedError(['SoldierNotAlive']))

        self.superadmin.message_history = []
        self.superadmin.says("!kill joe")
        self.assertEqual(['Joe is already dead'], self.superadmin.message_history)


    def test_superadmin_kills_joe(self):
        # GIVEN
        when(self.console).write()
        self.joe.connects('Joe')
        self.superadmin.connects('superadmin')
        self.joe.clearMessageHistory()
        self.superadmin.clearMessageHistory()
        # WHEN
        self.superadmin.says('!kill joe')
        # THEN
        verify(self.console).write(('admin.killPlayer', 'Joe'))
        self.assertEqual([], self.superadmin.message_history)
        self.assertEqual(['Killed by admin'], self.joe.message_history)

    def test_joe_kills_superadmin(self):
        self.joe.connects('Joe')
        self.superadmin.connects('superadmin')
        self.joe.message_history = []
        self.joe.says('!kill God')
        self.assertEqual(['Operation denied because God is in the Super Admin group'], self.joe.message_history)


    def test_superadmin_kills_simon(self):
        # GIVEN
        when(self.console).write()
        self.simon.connects('Simon')
        self.superadmin.connects('superadmin')
        self.simon.clearMessageHistory()
        self.superadmin.clearMessageHistory()
        # WHEN
        self.superadmin.says('!kill simon')
        verify(self.console).write(('admin.killPlayer', self.simon.name))
        # THEN
        self.assertEqual([], self.superadmin.message_history)
        self.assertEqual(['Killed by admin'], self.simon.message_history)