# -*- encoding: utf-8 -*-
import unittest
from mock import Mock # http://www.voidspace.org.uk/python/mock/mock.html
import b3
from b3.config import XmlConfigParser
from b3.fake import fakeConsole, joe, moderator, superadmin
from b3.parsers.frostbite2.protocol import CommandFailedError
from tests import prepare_fakeparser_for_tests
from poweradminbf3 import Poweradminbf3Plugin

prepare_fakeparser_for_tests()


class Test_cmd_swap(unittest.TestCase):

    def setUp(self):
        self.conf = XmlConfigParser()
        self.conf.loadFromString("""
        <configuration plugin="poweradminbf3">
            <settings name="commands">
                <set name="swap">20</set>
            </settings>
        </configuration>
        """)
        self.p = Poweradminbf3Plugin(fakeConsole, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()

    def test_frostbite_error(self):

        joe.connects("joe")
        joe.team = b3.TEAM_BLUE
        joe.teamId = 1
        joe.squad = 1

        moderator.connects("moderator")
        moderator.team = b3.TEAM_RED
        moderator.teamId = 2
        moderator.squad = 2

        # simulate Frostbite error when moving a player
        self.p._movePlayer = Mock(side_effect=CommandFailedError(['SetTeamFailed']))

        superadmin.connects('superadmin')
        superadmin.says("!swap joe moder")

        self.assertEqual(1, len(superadmin.message_history))
        self.assertEqual("Error while trying to swap joe with moderator. (SetTeamFailed)", superadmin.message_history[0])

