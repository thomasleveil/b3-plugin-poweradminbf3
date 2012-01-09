# -*- encoding: utf-8 -*-
import unittest
from b3.config import XmlConfigParser
from b3.fake import fakeConsole, moderator
from tests import prepare_fakeparser_for_tests
from poweradminbf3 import Poweradminbf3Plugin

prepare_fakeparser_for_tests()


class Test_cmd_autoassign(unittest.TestCase):

    def setUp(self):
        self.conf = XmlConfigParser()
        self.conf.loadFromString("""
        <configuration plugin="poweradminbf3">
            <settings name="commands">
                <set name="autoassign">20</set>
            </settings>
        </configuration>
        """)
        self.p = Poweradminbf3Plugin(fakeConsole, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()


    def test_no_argument_while_off(self):
        self.p._autoassign = False
        moderator.connects("moderator")
        moderator.message_history = []
        moderator.says("!autoassign")
        self.assertEqual(1, len(moderator.message_history))
        self.assertEqual("Autoassign is currently off, use !autoassign on to turn on", moderator.message_history[0])


    def test_no_argument_while_on(self):
        self.p._autoassign = True
        moderator.connects("moderator")
        moderator.message_history = []
        moderator.says("!autoassign")
        self.assertEqual(1, len(moderator.message_history))
        self.assertEqual("Autoassign is currently on, use !autoassign off to turn off", moderator.message_history[0])


    def test_with_argument_foo(self):
        moderator.connects("moderator")
        moderator.message_history = []
        moderator.says("!autoassign foo")
        self.assertIn("invalid data. Expecting on or off", moderator.message_history)


    def test_with_argument_on(self):
        self.p._autoassign = False
        moderator.connects("moderator")
        moderator.message_history = []
        moderator.says("!autoassign on")
        self.assertIn("Autoassign now enabled", moderator.message_history)
        self.assertTrue(self.p._autoassign)


    def test_with_argument_off_with_autobalance_on(self):
        self.p._autoassign = True
        self.p._autobalance = True
        moderator.connects("moderator")
        moderator.message_history = []
        moderator.says("!autoassign off")
        self.assertIn("Autoassign now disabled", moderator.message_history)
        self.assertFalse(self.p._autoassign)
        self.assertIn("Autobalance now disabled", moderator.message_history)
        self.assertFalse(self.p._autobalance)


    def test_with_argument_off_with_autobalance_off(self):
        self.p._autoassign = True
        self.p._autobalance = False
        moderator.connects("moderator")
        moderator.message_history = []
        moderator.says("!autoassign off")
        self.assertIn("Autoassign now disabled", moderator.message_history)
        self.assertFalse(self.p._autoassign)
        self.assertNotIn("Autobalance now disabled", moderator.message_history)
        self.assertFalse(self.p._autobalance)
