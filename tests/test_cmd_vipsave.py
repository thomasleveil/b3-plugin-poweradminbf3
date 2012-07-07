# -*- encoding: utf-8 -*-
from b3.config import CfgConfigParser
from b3.parsers.frostbite2.protocol import CommandFailedError
from poweradminbf3 import Poweradminbf3Plugin
from tests import Bf3TestCase

class Test_cmd_vipsave(Bf3TestCase):
    def setUp(self):
        Bf3TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""[commands]
vipsave: 20
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()

        self.moderator.connects("moderator")

        self.console.write.return_value = []


    def test_nominal(self):
        self.console.write.expect(('reservedSlotsList.save',)).thenReturn([])
        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!vipsave")
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('VIP list saved to disk (0 name written)', self.moderator.message_history[0])
        self.console.write.verify_expected_calls()

    def test_nominal_2(self):
        self.console.write.expect(('reservedSlotsList.list', 0)).thenReturn(['foo', 'bar'])
        self.console.write.expect(('reservedSlotsList.list', 2)).thenReturn([])
        self.console.write.expect(('reservedSlotsList.save',)).thenReturn([])
        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!vipsave")
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('VIP list saved to disk (2 names written)', self.moderator.message_history[0])
        self.console.write.verify_expected_calls()

    def test_frostbite_error(self):
        self.console.write.expect(('reservedSlotsList.save',)).thenRaise(CommandFailedError(['f00']))
        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!vipsave")
        self.assertEqual(["Error: f00"], self.moderator.message_history)
        self.console.write.verify_expected_calls()
