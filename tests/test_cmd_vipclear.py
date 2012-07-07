# -*- encoding: utf-8 -*-
from b3.config import CfgConfigParser
from b3.parsers.frostbite2.protocol import CommandFailedError
from poweradminbf3 import Poweradminbf3Plugin
from tests import Bf3TestCase

class Test_cmd_vipclear(Bf3TestCase):
    def setUp(self):
        Bf3TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""[commands]
vipclear: 20
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()

        self.moderator.connects("moderator")

        self.console.write.return_value = []


    def test_nominal(self):
        self.console.write.expect(('reservedSlotsList.clear',)).thenReturn([])
        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!vipclear")
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('VIP list is now empty', self.moderator.message_history[0])
        self.console.write.verify_expected_calls()

    def test_frostbite_error(self):
        self.console.write.expect(('reservedSlotsList.clear',)).thenRaise(CommandFailedError(['f00']))
        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!vipclear")
        self.assertEqual(["Error: f00"], self.moderator.message_history)
        self.console.write.verify_expected_calls()
