# -*- encoding: utf-8 -*-
import b3
from b3.config import XmlConfigParser
from b3.parsers.frostbite2.protocol import CommandFailedError
from poweradminbf3 import Poweradminbf3Plugin
from tests import Bf3TestCase


class Test_cmd_changeteam(Bf3TestCase):
    def setUp(self):
        super(Test_cmd_changeteam, self).setUp()
        self.conf = XmlConfigParser()
        self.conf.loadFromString("""
        <configuration plugin="poweradminbf3">
            <settings name="commands">
                <set name="changeteam">20</set>
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

        # simulate Frostbite error when moving a player
        self.console.write.expect(('admin.movePlayer', 'joe', 2, 0, 'true')).thenRaise(
            CommandFailedError(['SetTeamFailed']))

        self.superadmin.connects('superadmin')
        self.superadmin.message_history = []
        self.superadmin.says("!changeteam joe")

        self.assertEqual(1, self.joe.teamId)
        self.assertEqual(["Error, server replied ['SetTeamFailed']"], self.superadmin.message_history)


    def test_no_argument(self):
        self.superadmin.connects('superadmin')
        self.superadmin.message_history = []
        self.superadmin.says('!changeteam')
        self.assertEqual(['Invalid data, try !help changeteam'], self.superadmin.message_history)


    def test_unknown_player(self):
        self.superadmin.connects('superadmin')
        self.superadmin.message_history = []
        self.superadmin.says('!changeteam f00')
        self.assertEqual(['No players found matching f00'], self.superadmin.message_history)


    def test_trying_to_changeteam_on_an_higher_level_player(self):
        self.joe.connects('Joe')
        self.superadmin.connects('superadmin')
        self.superadmin.teamId = 2
        self.superadmin.squad = 1
        self.assertLess(self.joe.maxLevel, self.superadmin.maxLevel)
        self.joe.message_history = []

        self.joe.says('!changeteam god')

        self.assertEqual(2, self.superadmin.teamId)
        self.assertEqual(1, self.superadmin.squad)
        self.assertEqual(["You do not have sufficient access to use !changeteam"], self.joe.message_history)


    def test_ConquestLarge0(self):
        self.console.write.expect(('serverInfo',)).thenReturn(
            ['i3D.net - BigBrotherBot #3 (DE)', '0', '16', 'ConquestLarge0', 'MP_007', '0', '2',
             '2', '300', '300', '0', '', 'false', 'true', 'false', '197758', '197735', '', '', '', 'EU', 'AMS', 'DE'])
        self.console.getServerInfo()

        self.joe.connects('Joe')
        self.joe.teamId = 1
        self.superadmin.connects('superadmin')
        self.superadmin.message_history = []

        self.superadmin.says('!changeteam joe')
        self.assertEqual(2, self.joe.teamId)
        self.superadmin.says('!changeteam joe')
        self.assertEqual(1, self.joe.teamId)

        self.assertEqual(['Joe forced from team 1 to team 2', 'Joe forced from team 2 to team 1'],
            self.superadmin.message_history)


    def test_ConquestSmall0(self):
        self.console.write.expect(('serverInfo',)).thenReturn(
            ['i3D.net - BigBrotherBot #3 (DE)', '0', '16', 'ConquestSmall0', 'MP_001', '1', '2',
             '2', '250', '250', '0', '', 'false', 'true', 'false', '197774', '1', '', '', '', 'EU', 'AMS', 'DE'])
        self.console.getServerInfo()

        self.joe.connects('Joe')
        self.joe.teamId = 1
        self.superadmin.connects('superadmin')
        self.superadmin.message_history = []

        self.superadmin.says('!changeteam joe')
        self.assertEqual(2, self.joe.teamId)
        self.superadmin.says('!changeteam joe')
        self.assertEqual(1, self.joe.teamId)

        self.assertEqual(['Joe forced from team 1 to team 2', 'Joe forced from team 2 to team 1'],
            self.superadmin.message_history)


    def test_RushLarge0(self):
        # set the BF3 server
        # despite showing 0 teams in the serverInfo response, this gamemode has 2 teams (id 1 and 2)
        self.console.write.expect(('serverInfo',)).thenReturn(
            ['i3D.net - BigBrotherBot #3 (DE)', '0', '16', 'RushLarge0', 'MP_001', '0', '2',
             '0', '0', '', 'false', 'true', 'false', '197817', '2', '', '', '', 'EU', 'AMS', 'DE'])
        self.console.getServerInfo()

        self.joe.connects('Joe')
        self.joe.teamId = 1
        self.superadmin.connects('superadmin')
        self.superadmin.message_history = []

        self.superadmin.says('!changeteam joe')
        self.assertEqual(2, self.joe.teamId)
        self.superadmin.says('!changeteam joe')
        self.assertEqual(1, self.joe.teamId)

        self.assertEqual(['Joe forced from team 1 to team 2', 'Joe forced from team 2 to team 1'],
            self.superadmin.message_history)


    def test_SquadRush0(self):
        # despite showing 0 teams in the serverInfo response, this gamemode has 2 teams (id 1:attackers and 2:defenders)
        self.console.write.expect(('serverInfo',)).thenReturn(
            ['i3D.net - BigBrotherBot #3 (DE)', '0', '8', 'SquadRush0', 'MP_001', '1', '2',
             '0', '0', '', 'false', 'true', 'false', '197928', '0', '', '', '', 'EU', 'AMS', 'DE'])
        self.console.getServerInfo()

        self.joe.connects('Joe')
        self.joe.teamId = 1
        self.superadmin.connects('superadmin')
        self.superadmin.message_history = []

        self.superadmin.says('!changeteam joe')
        self.assertEqual(2, self.joe.teamId)
        self.superadmin.says('!changeteam joe')
        self.assertEqual(1, self.joe.teamId)

        self.assertEqual(['Joe forced from team 1 to team 2', 'Joe forced from team 2 to team 1'],
            self.superadmin.message_history)


    def test_SquadDeathMatch0(self):
        self.console.write.expect(('serverInfo',)).thenReturn(
            ['i3D.net - BigBrotherBot #3 (DE)', '0', '16', 'SquadDeathMatch0', 'MP_001', '0', '2',
             '4', '0', '0', '0', '0', '50', '', 'false', 'true', 'false', '198108', '0', '', '', '', 'EU', 'AMS', 'DE'])
        self.console.getServerInfo()
        self.joe.connects('Joe')
        self.joe.teamId = 1
        self.superadmin.connects('superadmin')
        self.superadmin.message_history = []

        self.superadmin.says('!changeteam joe')
        self.assertEqual(2, self.joe.teamId)
        self.superadmin.says('!changeteam joe')
        self.assertEqual(3, self.joe.teamId)
        self.superadmin.says('!changeteam joe')
        self.assertEqual(4, self.joe.teamId)
        self.superadmin.says('!changeteam joe')
        self.assertEqual(1, self.joe.teamId)

        self.assertEqual(['Joe forced from team 1 to team 2', 'Joe forced from team 2 to team 3',
                          'Joe forced from team 3 to team 4', 'Joe forced from team 4 to team 1'],
            self.superadmin.message_history)


    def test_TeamDeathMatch0(self):
        self.console.write.expect(('serverInfo',)).thenReturn(
            ['i3D.net - BigBrotherBot #3 (DE)', '0', '16', 'TeamDeathMatch0', 'MP_001', '1', '2',
             '2', '0', '0', '100', '', 'false', 'true', 'false', '198148', '0', '', '', '', 'EU', 'AMS', 'DE'])
        self.console.getServerInfo()

        self.joe.connects('Joe')
        self.joe.teamId = 1
        self.superadmin.connects('superadmin')
        self.superadmin.message_history = []

        self.superadmin.says('!changeteam joe')
        self.assertEqual(2, self.joe.teamId)
        self.superadmin.says('!changeteam joe')
        self.assertEqual(1, self.joe.teamId)

        self.assertEqual(['Joe forced from team 1 to team 2', 'Joe forced from team 2 to team 1'],
            self.superadmin.message_history)


class Test_issue_14(Bf3TestCase):
    def setUp(self):
        super(Test_issue_14, self).setUp()
        self.conf = XmlConfigParser()
        self.conf.loadFromString("""
            <configuration plugin="poweradminbf3">
                <settings name="commands">
                    <set name="changeteam">0</set>
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

        self.moderator.connects('moderator')
        self.moderator.teamId = 2

        self.console.write.expect(('admin.movePlayer', 'God', 1, 0, 'true'))
        self.moderator.says("!changeteam God")
        self.console.write.verify_expected_calls()


    def test_below__no_level_check_level(self):
        assert self.p.no_level_check_level == 20

        self.simon.connects("simon")
        self.simon.teamId = 1

        self.moderator.connects('moderator')
        self.moderator.teamId = 2

        self.simon.message_history = []
        self.simon.says("!changeteam modera")
        self.assertEqual(['Operation denied because Moderator is in the Moderator group'], self.simon.message_history)
