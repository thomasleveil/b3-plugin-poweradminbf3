# -*- encoding: utf-8 -*-
# http://www.voidspace.org.uk/python/mock/mock.html
from mock import Mock
import b3
from b3.config import XmlConfigParser
from b3.parsers.frostbite2.protocol import CommandFailedError
from poweradminbf3 import Poweradminbf3Plugin
from unittests import Bf3TestCase


class Test_cmd_kill(Bf3TestCase):
    def setUp(self):
        super(Test_cmd_kill, self).setUp()
        self.conf = XmlConfigParser()
        self.conf.loadFromString("""
        <configuration plugin="poweradminbf3">
            <settings name="commands">
                <set name="kill">0</set>
            </settings>
        </configuration>
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()


    def test_frostbite_error(self):
        self.joe.connects("joe")
        self.superadmin.connects('superadmin')
        self.console.write.expect(('admin.killPlayer', 'joe')).thenRaise(CommandFailedError(['f00']))

        self.superadmin.message_history = []
        self.superadmin.says("!kill joe")
        self.console.write.verify_expected_calls()
        self.assertEqual(["Error: ['f00']"], self.superadmin.message_history)


    def test_frostbite_error_SoldierNotAlive(self):
        self.joe.connects("joe")
        self.superadmin.connects('superadmin')
        self.console.write.expect(('admin.killPlayer', 'joe')).thenRaise(CommandFailedError(['SoldierNotAlive']))

        self.superadmin.message_history = []
        self.superadmin.says("!kill joe")
        self.console.write.verify_expected_calls()
        self.assertEqual(['Joe is already dead'], self.superadmin.message_history)


    def test_superadmin_kills_joe(self):
        self.joe.connects('Joe')
        self.superadmin.connects('superadmin')
        self.console.write.expect(('admin.killPlayer', 'Joe'))

        self.superadmin.says('!kill joe')
        self.console.write.verify_expected_calls()

    def test_joe_kills_superadmin(self):
        self.joe.connects('Joe')
        self.superadmin.connects('superadmin')
        self.joe.message_history = []
        self.joe.says('!kill God')
        self.assertEqual(['Operation denied because God is in the Super Admin group'], self.joe.message_history)

