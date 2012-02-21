# -*- encoding: utf-8 -*-
# http://www.voidspace.org.uk/python/mock/mock.html
from mock import Mock
import b3
from b3.config import XmlConfigParser
from b3.parsers.frostbite2.protocol import CommandFailedError
from poweradminbf3 import Poweradminbf3Plugin
from tests.unittests import Bf3TestCase


class Test_cmd_swap(Bf3TestCase):

    def setUp(self):
        super(Test_cmd_swap, self).setUp()
        self.conf = XmlConfigParser()
        self.conf.loadFromString("""
        <configuration plugin="poweradminbf3">
            <settings name="commands">
                <set name="swap">20</set>
            </settings>
        </configuration>
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()


    def test_frostbite_error(self):

        self.joe.connects("joe")
        self.joe.team = b3.TEAM_BLUE
        self.joe.teamId = 1
        self.joe.squad = 1

        self.moderator.connects("moderator")
        self.moderator.team = b3.TEAM_RED
        self.moderator.teamId = 2
        self.moderator.squad = 2

        # simulate Frostbite error when moving a player
        self.p._movePlayer = Mock(side_effect=CommandFailedError(['SetTeamFailed']))

        self.superadmin.connects('superadmin')
        self.superadmin.message_history = []
        self.superadmin.says("!swap joe moder")

        self.assertEqual(1, len(self.superadmin.message_history))
        self.assertEqual("Error while trying to swap joe with moderator. (SetTeamFailed)", self.superadmin.message_history[0])


    def test_superadmin_swap_joe(self):

        self.joe.connects('Joe')
        self.joe.teamId = 1
        self.joe.squad = 7

        self.superadmin.connects('superadmin')
        self.superadmin.teamId = 2
        self.superadmin.squad = 6

        self.superadmin.message_history = []
        self.superadmin.says('!swap joe')
        self.assertEqual(1, self.superadmin.teamId)
        self.assertEqual(7, self.superadmin.squad)
        self.assertEqual(2, self.joe.teamId)
        self.assertEqual(6, self.joe.squad)


    def test_superadmin_swap_joe_from_same_squad(self):

        self.joe.connects('Joe')
        self.joe.teamId = 2
        self.joe.squad = 6

        self.superadmin.connects('superadmin')
        self.superadmin.teamId = 2
        self.superadmin.squad = 6

        self.superadmin.message_history = []
        self.superadmin.says('!swap joe')
        self.assertEqual(['both players are in the same team and squad. Cannot swap'], self.superadmin.message_history)
        self.assertEqual(2, self.superadmin.teamId)
        self.assertEqual(6, self.superadmin.squad)
        self.assertEqual(2, self.joe.teamId)
        self.assertEqual(6, self.joe.squad)


    def test_superadmin_swap_players_from_same_team_and_squad(self):
        self.joe.connects('joe')
        self.joe.teamId = 1
        self.joe.squad = 6

        self.simon.connects('simon')
        self.simon.teamId = 1
        self.simon.squad = 6

        self.superadmin.connects('superadmin')
        self.superadmin.message_history = []
        self.superadmin.says("!swap joe simon")

        self.assertEqual(['both players are in the same team and squad. Cannot swap'], self.superadmin.message_history)
        self.assertEqual(1, self.simon.teamId)
        self.assertEqual(6, self.simon.squad)
        self.assertEqual(1, self.joe.teamId)
        self.assertEqual(6, self.joe.squad)


    def test_superadmin_swap_players_from_same_team_and_but_different_squads(self):
        self.joe.connects('joe')
        self.joe.teamId = 1
        self.joe.squad = 6

        self.simon.connects('simon')
        self.simon.teamId = 1
        self.simon.squad = 2

        self.superadmin.connects('superadmin')
        self.superadmin.message_history = []
        self.superadmin.says("!swap joe simon")

        self.assertEqual(1, self.simon.teamId)
        self.assertEqual(6, self.simon.squad)
        self.assertEqual(1, self.joe.teamId)
        self.assertEqual(2, self.joe.squad)
        self.assertEqual(['swapped player joe with simon'], self.superadmin.message_history)


class Test_issue_14(Bf3TestCase):

    def setUp(self):
        super(Test_issue_14, self).setUp()
        self.conf = XmlConfigParser()
        self.conf.loadFromString("""
            <configuration plugin="poweradminbf3">
                <settings name="commands">
                    <set name="swap">0</set>
                </settings>
                <settings name="preferences">
                    <set name="no_level_check_level">20</set>
                </settings>
            </configuration>
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()


    def test_above__no_level_check_level(self):

        assert self.p.no_level_check_level == 20

        self.superadmin.connects('God')
        self.superadmin.teamId = 2
        self.superadmin.squad = 6

        self.moderator.connects('moderator')
        self.moderator.teamId = 2
        self.moderator.squad = 5

        self.console.write.expect(('admin.movePlayer', 'God', 2, 5, 'true'))
        self.moderator.says("!swap God")
        self.console.write.verify_expected_calls()

    def test_below__no_level_check_level(self):

        assert self.p.no_level_check_level == 20

        self.simon.connects("simon")
        self.simon.teamId = 1
        self.simon.squad = 7

        self.moderator.connects('moderator')
        self.moderator.teamId = 2
        self.moderator.squad = 5

        self.simon.message_history = []
        self.simon.says("!swap modera")
        self.assertEqual(['Operation denied because Moderator is in the Moderator group'], self.simon.message_history)
