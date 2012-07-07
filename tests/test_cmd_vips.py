# -*- encoding: utf-8 -*-
from mock import call, Mock
from b3.config import CfgConfigParser
from poweradminbf3 import Poweradminbf3Plugin
from tests import Bf3TestCase


class Test_cmd_vips(Bf3TestCase):
    def setUp(self):
        Bf3TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""
[commands]
vips: mod
""")
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()

        self.console.say = Mock()
        self.console.saybig = Mock()

        self.moderator.connects("moderator")

        self.joe.connects('joe')
        self.joe.teamId = 2

        self.console.write.return_value = []


    def test_empty_vip_list(self):
        self.console.write.expect(('reservedSlotsList.list', 0)).thenReturn([])
        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!vips")
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('No VIP connected', self.moderator.message_history[0])
        self.console.write.assert_has_calls([call(('reservedSlotsList.list', 0))])


    def test_4_vips(self):
        self.console.write.expect(('reservedSlotsList.list', 0)).thenReturn(['name1', 'name2', 'name3', 'name2'])
        self.console.write.expect(('reservedSlotsList.list', 4)).thenReturn(['name4'])
        self.console.write.expect(('reservedSlotsList.list', 5)).thenReturn([])
        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!vips")
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('No VIP connected', self.moderator.message_history[0])
        self.console.write.assert_has_calls([call(('reservedSlotsList.list', 0))])
        self.console.write.assert_has_calls([call(('reservedSlotsList.list', 4))])
        self.console.write.assert_has_calls([call(('reservedSlotsList.list', 5))])


    def test_4_vips_one_is_connected(self):
        self.console.write.expect(('reservedSlotsList.list', 0)).thenReturn(['name1', 'name2', 'name3', 'Joe'])
        self.console.write.expect(('reservedSlotsList.list', 4)).thenReturn([])
        self.joe.connects("Joe")
        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!vips")
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('Connected VIPs: Joe', self.moderator.message_history[0])
        self.console.write.assert_has_calls([call(('reservedSlotsList.list', 0))])
        self.console.write.assert_has_calls([call(('reservedSlotsList.list', 4))])

