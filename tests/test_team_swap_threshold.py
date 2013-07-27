# -*- encoding: utf-8 -*-
from mock import Mock, patch
from tests import Bf3TestCase, logging_disabled
from b3.config import CfgConfigParser
from poweradminbf3 import Poweradminbf3Plugin


class Test_config(Bf3TestCase):
    default_value = 3
    minimum_value = 2

    def assert_config_value(self, expected, conf_value):
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""
[preferences]
team_swap_threshold: %s
                    """ % conf_value)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.assertEqual(expected, self.p._team_swap_threshold)

    def test_default_value(self):
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""[foo]""")
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.assertEqual(self.default_value, self.p._team_swap_threshold)

    def test_nominal(self):
        self.assert_config_value(6, '6')

    def test_value_too_low(self):
        self.assert_config_value(self.minimum_value, '1')

    def test_negative_value(self):
        self.assert_config_value(self.minimum_value, '-2')

    def test_float(self):
        self.assert_config_value(self.default_value, '3.54')

    def test_junk(self):
        self.assert_config_value(self.default_value, 'junk')



class Test_autoassign(Bf3TestCase):

    def setUp(self):
        super(Test_autoassign, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""
[preferences]
no_autoassign_level: 20
autoassign: On
team_swap_threshold: 2
        """)
        with logging_disabled():
            self.p = Poweradminbf3Plugin(self.console, self.conf)
            self.p.onLoadConfig()
            self.p.onStartup()
        self.assertTrue(self.p._autoassign)
        self.assertEqual(20, self.p._no_autoassign_level)

        def my_write(data):
            if data[0] == 'admin.movePlayer':
                self.console.routeFrostbitePacket(['player.onTeamChange', data[1], data[2], data[3]])
                return ['OK']
            else:
                return Mock()

        self.write_patcher = patch.object(self.console, "write", side_effect=my_write)
        self.write_mock = self.write_patcher.start()

    def tearDown(self):
        Bf3TestCase.tearDown(self)
        self.write_patcher.stop()

    def count_teams(self):
        clients_teams = [c.teamId for c in self.console.clients.getList()]
        return clients_teams.count(1), clients_teams.count(2), clients_teams.count(3), clients_teams.count(4)


    def test_players_join(self):
        self.p._one_round_over = self.p._scramblingdone = True

        self.assertEqual((0,0,0,0), self.count_teams())

        self.moderator.teamId = 1
        self.moderator.connects('moderator')
        self.assertEqual((1,0,0,0), self.count_teams())

        self.reg.teamId = 1
        self.reg.connects('reg')
        self.assertEqual((2,0,0,0), self.count_teams())

        self.joe.teamId = 1
        self.joe.connects('joe')
        self.assertEqual((2,1,0,0), self.count_teams())

        self.superadmin.teamId = 1
        self.superadmin.connects('god')
        self.assertEqual((3,1,0,0), self.count_teams())

        self.simon.teamId = 1
        self.simon.connects('simon')
        self.assertEqual((3,2,0,0), self.count_teams())


    def test_players_changes_team(self):
        self.p._one_round_over = self.p._scramblingdone = True

        self.assertEqual((0,0,0,0), self.count_teams())

        self.moderator.teamId = 1
        self.reg.teamId = 1
        self.superadmin.teamId = 1
        self.joe.teamId = 2
        self.simon.teamId = 2

        self.moderator.connects('moderator')
        self.reg.connects('reg')
        self.superadmin.connects('god')
        self.joe.connects('joe')
        self.simon.connects('simon')

        self.assertEqual((3,2,0,0), self.count_teams())

        self.p.autoassign = Mock(wraps=self.p.autoassign)
        self.simon.changes_team(1)
        self.assertTrue(self.p.autoassign.called)
        self.console.write.assert_called_with(('admin.movePlayer', 'simon', 2, 0, 'true'))
        self.assertEqual((3,2,0,0), self.count_teams())


    def test_players_changes_team__huge_swap_threshold(self):
        self.p._one_round_over = self.p._scramblingdone = True
        self.p._team_swap_threshold = 10

        self.assertEqual((0,0,0,0), self.count_teams())

        self.moderator.teamId = 1
        self.reg.teamId = 1
        self.superadmin.teamId = 1
        self.joe.teamId = 2
        self.simon.teamId = 2

        self.moderator.connects('moderator')
        self.reg.connects('reg')
        self.superadmin.connects('god')
        self.joe.connects('joe')
        self.simon.connects('simon')

        self.assertEqual((3,2,0,0), self.count_teams())

        self.p.autoassign = Mock(wraps=self.p.autoassign)
        self.simon.changes_team(1)
        self.assertTrue(self.p.autoassign.called)
        self.assertEqual((4,1,0,0), self.count_teams())


