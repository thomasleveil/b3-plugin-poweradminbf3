# -*- encoding: utf-8 -*-
from mock import patch, call, Mock
import time
from b3.config import CfgConfigParser
from poweradminbf3 import Poweradminbf3Plugin
from tests import Bf3TestCase

class Test_cmd_nuke(Bf3TestCase):
    def setUp(self):
        Bf3TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""[commands]
nuke: 20
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()

        self.sleep_patcher = patch.object(time, 'sleep')
        self.sleep_patcher.start()

        self.console.write = Mock()
        self.console.say = Mock()
        self.console.saybig = Mock()

        self.moderator.connects("moderator")
        self.moderator.teamId = 1

        self.joe.connects('joe')
        self.joe.teamId = 2



    def tearDown(self):
        Bf3TestCase.tearDown(self)
        self.sleep_patcher.stop()


    def test_no_argument(self):
        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!nuke")
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('missing parameter, try !help nuke', self.moderator.message_history[0])


    def test_bad_argument(self):
        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!nuke f00")
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('invalid parameter. expecting all, ru or us', self.moderator.message_history[0])


    def test_all(self):
        self.moderator.says("!nuke all")
        self.console.write.assert_has_calls([call(('admin.killPlayer', 'moderator')), call(('admin.killPlayer', 'joe'))])
        self.console.say.assert_has_calls([call('Killing all players')])
        self.console.saybig.assert_called_with('Incoming nuke warning')


    def test_all_with_reason(self):
        self.moderator.says("!nuke all base raping")
        self.console.write.assert_has_calls([call(('admin.killPlayer', 'moderator')), call(('admin.killPlayer', 'joe'))])
        self.console.say.assert_has_calls([call('Killing all players'), call('Nuke reason : base raping')])
        self.console.saybig.assert_called_with('Incoming nuke warning')


    def test_us(self):
        self.moderator.says("!nuke us")
        self.console.write.assert_has_calls([call(('admin.killPlayer', 'moderator'))])
        self.console.saybig.assert_called_with('Incoming nuke warning')


    def test_ru(self):
        self.moderator.says("!nuke ru")
        self.console.write.assert_has_calls([call(('admin.killPlayer', 'joe'))])
        self.console.saybig.assert_called_with('Incoming nuke warning')

