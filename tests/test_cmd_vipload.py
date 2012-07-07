# -*- encoding: utf-8 -*-
from b3.config import CfgConfigParser
from b3.parsers.frostbite2.protocol import CommandFailedError
from poweradminbf3 import Poweradminbf3Plugin
from tests import Bf3TestCase

class Test_cmd_vipload(Bf3TestCase):
    def setUp(self):
        Bf3TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""[commands]
vipload: 20
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()

        self.moderator.connects("moderator")

        self.console.write.return_value = []


    def test_nominal(self):
        self.console.write.expect(('reservedSlotsList.load',)).thenReturn([])
        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!vipload")
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('VIP list loaded from disk (0 name loaded)', self.moderator.message_history[0])
        self.console.write.verify_expected_calls()

    def test_nominal_2(self):
        self.console.write.expect(('reservedSlotsList.list', 0)).thenReturn(['foo', 'bar'])
        self.console.write.expect(('reservedSlotsList.list', 2)).thenReturn([])
        self.console.write.expect(('reservedSlotsList.load',)).thenReturn([])
        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!vipload")
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('VIP list loaded from disk (2 names loaded)', self.moderator.message_history[0])
        self.console.write.verify_expected_calls()

    def test_frostbite_error(self):
        self.console.write.expect(('reservedSlotsList.load',)).thenRaise(CommandFailedError(['f00']))
        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!vipload")
        self.assertEqual(["Error: f00"], self.moderator.message_history)
        self.console.write.verify_expected_calls()
