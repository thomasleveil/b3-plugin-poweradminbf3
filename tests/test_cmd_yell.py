# -*- encoding: utf-8 -*-
from mock import patch
from b3.config import CfgConfigParser
from poweradminbf3 import Poweradminbf3Plugin
from tests import Bf3TestCase


class Test_config(Bf3TestCase):

    def test_no_preference(self):
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""[foo]""")
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.assertEqual(10, self.p._yell_duration)

    def test_yell_duration_int(self):
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""
[preferences]
yell_duration: 1
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.assertEqual(1.0, self.p._yell_duration)

    def test_yell_duration_float(self):
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""
[preferences]
yell_duration: 1.3
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.assertEqual(10, self.p._yell_duration)

    def test_yell_duration_too_low(self):
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""
[preferences]
yell_duration: 0.3
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.assertEqual(10, self.p._yell_duration)

    def test_yell_duration_junk(self):
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""
[preferences]
yell_duration: foo
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.assertEqual(10, self.p._yell_duration)

    def test_yell_duration_empty(self):
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""
[preferences]
yell_duration:
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.assertEqual(10, self.p._yell_duration)



class Test_cmd_yell(Bf3TestCase):

    def setUp(self):
        Bf3TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""[commands]
yell: 20

[preferences]
yell_duration: 2
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()


    def test_no_argument(self):
        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!yell")
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('missing parameter, try !help yell', self.moderator.message_history[0])

    def test_nominal(self):
        self.moderator.connects("moderator")
        with patch.object(self.console, "write") as write_mock:
            self.moderator.says("!yell changing map soon !")
        write_mock.assert_called_once_with(('admin.yell', 'changing map soon !', '2'))



class Test_cmd_yellteam(Bf3TestCase):

    def setUp(self):
        Bf3TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""[commands]
yellteam: 20

[preferences]
yell_duration: 2
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()


    def test_no_argument(self):
        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!yellteam")
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('missing parameter, try !help yellteam', self.moderator.message_history[0])

    def test_nominal(self):
        self.moderator.connects("moderator")
        self.moderator.teamId = 3
        with patch.object(self.console, "write") as write_mock:
            self.moderator.says("!yellteam changing map soon !")
        write_mock.assert_called_once_with(('admin.yell', 'changing map soon !', '2', 'team', '3'))



class Test_cmd_yellsquad(Bf3TestCase):

    def setUp(self):
        Bf3TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""[commands]
yellsquad: 20

[preferences]
yell_duration: 2
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()


    def test_no_argument(self):
        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!yellsquad")
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('missing parameter, try !help yellsquad', self.moderator.message_history[0])

    def test_nominal(self):
        self.moderator.connects("moderator")
        self.moderator.teamId = 3
        self.moderator.squad = 4
        with patch.object(self.console, "write") as write_mock:
            self.moderator.says("!yellsquad changing map soon !")
        write_mock.assert_called_once_with(('admin.yell', 'changing map soon !', '2', 'squad', '3', '4'))


class Test_cmd_yellplayer(Bf3TestCase):

    def setUp(self):
        Bf3TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""[commands]
yellplayer: 20

[preferences]
yell_duration: 2
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()


    def test_no_argument(self):
        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!yellplayer")
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('invalid parameters, try !help yellplayer', self.moderator.message_history[0])

    def test_nominal(self):
        self.joe.connects('joe')
        self.moderator.connects("moderator")
        with patch.object(self.console, "write") as write_mock:
            self.moderator.says("!yellplayer joe changing map soon !")
        write_mock.assert_called_once_with(('admin.yell', 'changing map soon !', '2', 'player', 'joe'))

