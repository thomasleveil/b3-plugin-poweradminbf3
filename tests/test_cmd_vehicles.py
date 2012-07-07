# -*- encoding: utf-8 -*-
from mock import Mock # http://www.voidspace.org.uk/python/mock/mock.html
from b3.config import CfgConfigParser
from b3.cvar import Cvar
from b3.parsers.frostbite2.protocol import CommandFailedError
from poweradminbf3 import Poweradminbf3Plugin
from tests import Bf3TestCase


class Test_cmd_vehicles(Bf3TestCase):

    def setUp(self):
        Bf3TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""[commands]
vehicles: 20
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
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

        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!vehicles")
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual("Vehicle spawn is [ON]", self.moderator.message_history[0])


    def test_no_argument_false(self):
        # simulate Frostbite error when changing vehicleSpawnAllowed
        def getCvar_proxy(var_name):
            if var_name == 'vehicleSpawnAllowed':
                return Cvar('vehicleSpawnAllowed', value='false')
            else:
                return Mock()
        self.p.console.getCvar = Mock(side_effect=getCvar_proxy)

        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!vehicles")
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual("Vehicle spawn is [OFF]", self.moderator.message_history[0])


    def test_no_argument_error(self):
        # simulate Frostbite error when changing vehicleSpawnAllowed
        def getCvar_proxy(var_name):
            if var_name == 'vehicleSpawnAllowed':
                raise CommandFailedError(['foo'])
            else:
                return Mock()
        self.p.console.getCvar = Mock(side_effect=getCvar_proxy)

        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!vehicles")
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual("Vehicle spawn is [unknown]", self.moderator.message_history[0])


    def test_with_argument_foo(self):
        # simulate Frostbite error when changing vehicleSpawnAllowed
        def setCvar_proxy(var_name, value):
            if var_name == 'vehicleSpawnAllowed':
                raise CommandFailedError(['InvalidArguments'])
            else:
                return Mock()
        self.p.console.setCvar = Mock(side_effect=setCvar_proxy)
        self.p.console.getCvar = Mock(return_value='bar')

        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!vehicles foo")
        self.assertIn("unexpected value 'foo'. Available modes : on, off", self.moderator.message_history)
        self.assertIn("Vehicle spawn is [unknown]", self.moderator.message_history)


    def test_with_argument_on(self):
        self.p.console.setCvar = Mock()
        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!vehicles on")
        self.assertIn("vehicle spawn is now [ON]", self.moderator.message_history)
        self.p.console.setCvar.assert_called_with('vehicleSpawnAllowed','true')


    def test_with_argument_off(self):
        self.p.console.setCvar = Mock()
        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!vehicles off")
        self.assertIn("vehicle spawn is now [OFF]", self.moderator.message_history)
        self.p.console.setCvar.assert_called_with('vehicleSpawnAllowed','false')
