# -*- encoding: utf-8 -*-
import unittest
from mock import Mock, patch # http://www.voidspace.org.uk/python/mock/mock.html
from b3.config import XmlConfigParser
from b3.fake import fakeConsole, moderator
from tests import prepare_fakeparser_for_tests
from poweradminbf3 import Poweradminbf3Plugin

prepare_fakeparser_for_tests()


class Test_cmd_autobalance(unittest.TestCase):

    def setUp(self):
        self.conf = XmlConfigParser()
        self.conf.loadFromString("""
        <configuration plugin="poweradminbf3">
            <settings name="commands">
                <set name="autobalance">20</set>
            </settings>
        </configuration>
        """)
        self.p = Poweradminbf3Plugin(fakeConsole, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()


    def test_no_argument_while_off(self):
        self.p._autobalance = False
        moderator.connects("moderator")
        moderator.message_history = []
        moderator.says("!autobalance")
        self.assertEqual(1, len(moderator.message_history))
        self.assertEqual("Autobalance is currently off, use !autobalance on to turn on", moderator.message_history[0])


    def test_no_argument_while_on(self):
        self.p._autobalance = True
        moderator.connects("moderator")
        moderator.message_history = []
        moderator.says("!autobalance")
        self.assertEqual(1, len(moderator.message_history))
        self.assertEqual("Autobalance is currently on, use !autobalance off to turn off", moderator.message_history[0])


    def test_with_argument_foo(self):
        moderator.connects("moderator")
        moderator.message_history = []
        moderator.says("!autobalance foo")
        self.assertIn("invalid data. Expecting on, off or now", moderator.message_history)


    def test_with_argument_now(self):
        self.p.run_autobalance = Mock()
        moderator.connects("moderator")
        moderator.message_history = []
        moderator.says("!autobalance now")
        self.p.run_autobalance.assert_called_once()


    def test_with_argument_on_while_currently_off_and_autoassign_off(self):
        self.p._autobalance = False
        self.p._autoassign = False
        self.p._one_round_over = False
        moderator.connects("moderator")
        moderator.message_history = []
        moderator.says("!autobalance on")
        self.assertIn("Autobalance will be enabled on next round start", moderator.message_history)
        self.assertIn("Autoassign now enabled", moderator.message_history)
        self.assertTrue(self.p._autobalance)
        self.assertTrue(self.p._autoassign)


    @patch("b3.cron.Cron")
    def test_with_argument_on_while_currently_off_and_one_round_is_over(self, MockCron):
        self.p._autobalance = False
        self.p._one_round_over = True
        self.p._cronTab_autobalance = None
        self.p.console.cron.__add__ = Mock()
        moderator.connects("moderator")
        moderator.message_history = []
        moderator.says("!autobalance on")
        self.assertIn("Autobalance now enabled", moderator.message_history)
        self.assertTrue(self.p._autobalance)
        self.assertIsNotNone(self.p._cronTab_autobalance)
        self.p.console.cron.__add__.assert_called_once_with(self.p._cronTab_autobalance)


    @patch("b3.cron.Cron")
    def test_with_argument_on_while_currently_off_and_no_round_is_over(self, MockCron):
        self.p._autobalance = False
        self.p._one_round_over = False
        self.p._cronTab_autobalance = None
        self.p.console.cron.__add__ = Mock()
        moderator.connects("moderator")
        moderator.message_history = []
        moderator.says("!autobalance on")
        self.assertIn("Autobalance will be enabled on next round start", moderator.message_history)
        self.assertTrue(self.p._autobalance)
        self.assertIsNone(self.p._cronTab_autobalance)
        self.assertFalse(self.p.console.cron.__add__.called)


    def test_with_argument_on_while_already_on(self):
        self.p._autobalance = True
        moderator.connects("moderator")
        moderator.message_history = []
        moderator.says("!autobalance on")
        self.assertEqual(["Autobalance is already enabled"], moderator.message_history)
        self.assertTrue(self.p._autobalance)


    @patch("b3.cron.Cron")
    def test_with_argument_off_while_currently_on(self, MockCron):
        self.p._autobalance = True
        self.p.console.cron.__sub__ = Mock()
        self.p._cronTab_autobalance = Mock()
        moderator.connects("moderator")
        moderator.message_history = []
        moderator.says("!autobalance off")
        self.assertEqual(["Autobalance now disabled"], moderator.message_history)
        self.assertFalse(self.p._autobalance)
        self.p.console.cron.__sub__.assert_called_once_with(self.p._cronTab_autobalance)


    def test_with_argument_off_while_already_off(self):
        self.p._autobalance = False
        moderator.connects("moderator")
        moderator.message_history = []
        moderator.says("!autobalance off")
        self.assertEqual(["Autobalance now disabled"], moderator.message_history)
        self.assertFalse(self.p._autobalance)
