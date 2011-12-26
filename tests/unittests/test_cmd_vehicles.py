# -*- encoding: utf-8 -*-
import unittest
from mock import Mock # http://www.voidspace.org.uk/python/mock/mock.html
import b3
from b3.config import XmlConfigParser
from b3.cvar import Cvar
from b3.fake import fakeConsole, moderator
from b3.parsers.frostbite2.protocol import CommandFailedError
from tests import prepare_fakeparser_for_tests
from poweradminbf3 import Poweradminbf3Plugin

prepare_fakeparser_for_tests()


class Test_cmd_vehicles(unittest.TestCase):

    def setUp(self):
        self.conf = XmlConfigParser()
        self.conf.loadFromString("""
        <configuration plugin="poweradminbf3">
            <settings name="commands">
                <set name="vehicles">20</set>
            </settings>
        </configuration>
        """)
        self.p = Poweradminbf3Plugin(fakeConsole, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()


    def test_no_argument_true(self):
        # simulate Frostbite error when changing vehicleSpawnAllowed
        def getCvar_proxy(var_name):
            if var_name == 'vehicleSpawnAllowed':
                return Cvar('vehicleSpawnAllowed', value='true')
            else:
                return Mock()
        self.p.console.getCvar = Mock(side_effect=getCvar_proxy)

        moderator.connects("moderator")
        moderator.message_history = []
        moderator.says("!vehicles")
        self.assertEqual(1, len(moderator.message_history))
        self.assertEqual("Vehicle spawn is [ON]", moderator.message_history[0])


    def test_no_argument_false(self):
        # simulate Frostbite error when changing vehicleSpawnAllowed
        def getCvar_proxy(var_name):
            if var_name == 'vehicleSpawnAllowed':
                return Cvar('vehicleSpawnAllowed', value='false')
            else:
                return Mock()
        self.p.console.getCvar = Mock(side_effect=getCvar_proxy)

        moderator.connects("moderator")
        moderator.message_history = []
        moderator.says("!vehicles")
        self.assertEqual(1, len(moderator.message_history))
        self.assertEqual("Vehicle spawn is [OFF]", moderator.message_history[0])


    def test_no_argument_error(self):
        # simulate Frostbite error when changing vehicleSpawnAllowed
        def getCvar_proxy(var_name):
            if var_name == 'vehicleSpawnAllowed':
                raise CommandFailedError(['foo'])
            else:
                return Mock()
        self.p.console.getCvar = Mock(side_effect=getCvar_proxy)

        moderator.connects("moderator")
        moderator.message_history = []
        moderator.says("!vehicles")
        self.assertEqual(1, len(moderator.message_history))
        self.assertEqual("Vehicle spawn is [unknown]", moderator.message_history[0])


    def test_with_argument_foo(self):
        # simulate Frostbite error when changing vehicleSpawnAllowed
        def setCvar_proxy(var_name, value):
            if var_name == 'vehicleSpawnAllowed':
                raise CommandFailedError(['InvalidArguments'])
            else:
                return Mock()
        self.p.console.setCvar = Mock(side_effect=setCvar_proxy)
        self.p.console.getCvar = Mock(return_value='bar')

        moderator.connects("moderator")
        moderator.message_history = []
        moderator.says("!vehicles foo")
        self.assertIn("unexpected value 'foo'. Available modes : on, off", moderator.message_history)
        self.assertIn("Vehicle spawn is [unknown]", moderator.message_history)


    def test_with_argument_on(self):
        self.p.console.setCvar = Mock()
        moderator.connects("moderator")
        moderator.message_history = []
        moderator.says("!vehicles on")
        self.assertIn("vehicle spawn is now [ON]", moderator.message_history)
        self.p.console.setCvar.assert_called_with('vehicleSpawnAllowed','true')


    def test_with_argument_off(self):
        self.p.console.setCvar = Mock()
        moderator.connects("moderator")
        moderator.message_history = []
        moderator.says("!vehicles off")
        self.assertIn("vehicle spawn is now [OFF]", moderator.message_history)
        self.p.console.setCvar.assert_called_with('vehicleSpawnAllowed','false')
