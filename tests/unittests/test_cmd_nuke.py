# -*- encoding: utf-8 -*-
from mock import patch, call
import time
from b3.config import XmlConfigParser
from poweradminbf3 import Poweradminbf3Plugin
from tests.unittests import Bf3TestCase
from unittests import Mockito

class Test_cmd_nuke(Bf3TestCase):
    def setUp(self):
        Bf3TestCase.setUp(self)
        self.conf = XmlConfigParser()
        self.conf.loadFromString("""
        <configuration plugin="poweradminbf3">
            <settings name="commands">
                <set name="nuke">20</set>
            </settings>
        </configuration>
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()

        self.sleep_patcher = patch.object(time, 'sleep')
        self.sleep_patcher.start()

        self.moderator.connects("moderator")
        self.moderator.teamId = 1

        self.joe.connects('joe')
        self.joe.teamId = 2

        self.console.getPlayerList = Mockito()
        self.console.getPlayerList.expect().thenReturn({self.moderator.cid: self.moderator, self.joe.cid: self.joe})

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


    def test_us(self):
        self.moderator.says("!nuke us")
        self.console.write.assert_has_calls([call(('admin.killPlayer', 'moderator'))])


    def test_ru(self):
        self.moderator.says("!nuke ru")
        self.console.write.assert_has_calls([call(('admin.killPlayer', 'joe'))])

