# -*- encoding: utf-8 -*-
# http://www.voidspace.org.uk/python/mock/mock.html
from b3.config import XmlConfigParser
from b3.parsers.frostbite2.protocol import CommandFailedError
from poweradminbf3 import Poweradminbf3Plugin
from tests import Bf3TestCase


class Test_cmd_vipremove(Bf3TestCase):
    def setUp(self):
        super(Test_cmd_vipremove, self).setUp()
        self.conf = XmlConfigParser()
        self.conf.loadFromString("""
        <configuration plugin="poweradminbf3">
            <settings name="commands">
                <set name="vipremove">0</set>
            </settings>
        </configuration>
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()
        self.console.write.return_value = []


    def test_missing_parameter(self):
        self.superadmin.connects('superadmin')
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!vipremove')
        self.assertEqual(['Usage: !vipremove <player>'], self.superadmin.message_history)


    def test_non_existing_player(self):
        self.superadmin.connects('superadmin')
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!vipremove joe')
        self.assertEqual(["No VIP named 'joe' found"], self.superadmin.message_history)


    def test_frostbite_error(self):
        self.joe.connects("joe")
        self.superadmin.connects('superadmin')
        self.console.write.expect(('reservedSlotsList.remove', u'Joe')).thenRaise(CommandFailedError(['f00']))
        self.superadmin.clearMessageHistory()
        self.superadmin.says("!vipremove joe")
        self.console.write.verify_expected_calls()
        self.assertEqual(["Error: f00"], self.superadmin.message_history)
        self.console.write.verify_expected_calls()


    def test_frostbite_error_PlayerNotInList(self):
        self.joe.connects("joe")
        self.superadmin.connects('superadmin')
        self.console.write.expect(('reservedSlotsList.remove', u'Joe')).thenRaise(CommandFailedError(['PlayerNotInList']))
        self.superadmin.clearMessageHistory()
        self.superadmin.says("!vipremove joe")
        self.console.write.verify_expected_calls()
        self.assertEqual(["There is no VIP named 'Joe'"], self.superadmin.message_history)
        self.console.write.verify_expected_calls()


    def test_nominal_on_connected_player(self):
        self.joe.connects('Joe')
        self.superadmin.connects('superadmin')
        self.superadmin.clearMessageHistory()
        self.console.write.expect(('reservedSlotsList.remove', 'Joe'))
        self.superadmin.says('!vipremove jo')
        self.assertEqual(['VIP privileges removed for Joe'], self.superadmin.message_history)
        self.console.write.verify_expected_calls()


    def test_nominal_on_not_connected_player(self):
        self.console.write.expect(('reservedSlotsList.list', 0)).thenReturn(['Joe'])
        self.console.write.expect(('reservedSlotsList.list', 1)).thenReturn([])
        self.console.write.expect(('reservedSlotsList.remove', 'joe'))
        self.superadmin.connects('superadmin')
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!vipremove joe')
        self.assertEqual(['VIP privileges removed for joe'], self.superadmin.message_history)
        self.console.write.verify_expected_calls()


    def test_no_right(self):
        self.console.write.expect(('reservedSlotsList.list', 0)).thenReturn(['Joe'])
        self.joe.connects('Joe')
        self.joe.save()
        self.superadmin.connects('God')
        self.joe.clearMessageHistory()
        self.joe.says('!vipremove God')
        self.assertEqual(['Operation denied because God is in the Super Admin group'], self.joe.message_history)

