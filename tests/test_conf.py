# -*- encoding: utf-8 -*-
import logging
from mock import Mock, call

from poweradminbf3 import Poweradminbf3Plugin, __file__ as poweradminbf3_file
from b3.config import XmlConfigParser

from tests import Bf3TestCase

class Test_conf(Bf3TestCase):

    def setUp(self):
        Bf3TestCase.setUp(self)
        self.conf = XmlConfigParser()
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        logger = logging.getLogger('output')
        logger.setLevel(logging.INFO)


class Test_common(Test_conf):

    def test_1(self):
        self.conf.loadFromString("""<configuration plugin="poweradminbf3"/>""")
        self.p.onLoadConfig()
        # should not raise any error

    def test_issue_12(self):
        """See https://github.com/courgette/b3-plugin-poweradminbf3/issues/12"""
        self.conf.loadFromString("""
            <configuration plugin="poweradminbf3">
              <settings name="commands">
                <set name="setmode-mode">60</set>

                <set name="roundnext-rnext">40</set>
                <set name="roundrestart-rrestart">40</set>
                <set name="kill">40</set>

                <set name="changeteam">20</set>
                <set name="swap">20</set>
                <set name="setnextmap-snmap">20</set>
              </settings>
              <settings name="messages">
                <set name="operation_denied">Operation denied</set>
                <set name="operation_denied_level">Operation denied because %(name)s is in the %(group)s group</set>
              </settings>
            </configuration>
        """)
        self.p._load_scrambler()
        # should not raise any error


class Test_load_scrambler__mode(Test_conf):

    def test_no_section(self):
        self.conf.loadFromString("""<configuration plugin="poweradminbf3"/>""")
        self.p._load_scrambler()
        self.assertFalse(self.p._autoscramble_rounds)
        self.assertFalse(self.p._autoscramble_maps)

    def test_no_option(self):
        self.conf.loadFromString("""<configuration plugin="poweradminbf3">
                <settings name="scrambler"/>
            </configuration>""")
        self.p._load_scrambler()
        self.assertFalse(self.p._autoscramble_rounds)
        self.assertFalse(self.p._autoscramble_maps)

    def test_empty_option(self):
        self.conf.loadFromString("""<configuration plugin="poweradminbf3">
                <settings name="scrambler">
                    <set name="mode"></set>
                </settings>
            </configuration>""")
        self.p._load_scrambler()
        self.assertFalse(self.p._autoscramble_rounds)
        self.assertFalse(self.p._autoscramble_maps)

    def test_bad_option(self):
        self.conf.loadFromString("""<configuration plugin="poweradminbf3">
                <settings name="scrambler">
                    <set name="mode">foo</set>
                </settings>
            </configuration>""")
        self.p._load_scrambler()
        self.assertFalse(self.p._autoscramble_rounds)
        self.assertFalse(self.p._autoscramble_maps)

    def test_off(self):
        self.conf.loadFromString("""<configuration plugin="poweradminbf3">
                <settings name="scrambler">
                    <set name="mode">off</set>
                </settings>
            </configuration>""")
        self.p._load_scrambler()
        self.assertFalse(self.p._autoscramble_rounds)
        self.assertFalse(self.p._autoscramble_maps)

    def test_round(self):
        self.conf.loadFromString("""<configuration plugin="poweradminbf3">
                <settings name="scrambler">
                    <set name="mode">round</set>
                </settings>
            </configuration>""")
        self.p._load_scrambler()
        self.assertTrue(self.p._autoscramble_rounds)
        self.assertFalse(self.p._autoscramble_maps)

    def test_map(self):
        self.conf.loadFromString("""<configuration plugin="poweradminbf3">
                <settings name="scrambler">
                    <set name="mode">map</set>
                </settings>
            </configuration>""")
        self.p._load_scrambler()
        self.assertFalse(self.p._autoscramble_rounds)
        self.assertTrue(self.p._autoscramble_maps)



class Test_load_scrambler__strategy(Test_conf):

    def setUp(self):
        super(Test_load_scrambler__strategy, self).setUp()
        self.setSTragegy_mock = self.p._scrambler.setStrategy = Mock(name="setStrategy", wraps=self.p._scrambler.setStrategy)

    def test_no_section(self):
        self.conf.loadFromString("""<configuration plugin="poweradminbf3"/>""")
        self.p._load_scrambler()
        self.setSTragegy_mock.assert_called_once_with('random')

    def test_no_option(self):
        self.conf.loadFromString("""<configuration plugin="poweradminbf3">
                <settings name="scrambler"/>
            </configuration>""")
        self.p._load_scrambler()
        self.setSTragegy_mock.assert_called_once_with('random')

    def test_empty_option(self):
        self.conf.loadFromString("""<configuration plugin="poweradminbf3">
                <settings name="scrambler">
                    <set name="strategy"></set>
                </settings>
            </configuration>""")
        self.p._load_scrambler()
        self.setSTragegy_mock.assert_has_calls([call(''), call('random')])

    def test_bad_option(self):
        self.conf.loadFromString("""<configuration plugin="poweradminbf3">
                <settings name="scrambler">
                    <set name="strategy">foo</set>
                </settings>
            </configuration>""")
        self.p._load_scrambler()
        self.setSTragegy_mock.assert_has_calls([call('foo'), call('random')])


    def test_random(self):
        self.conf.loadFromString("""<configuration plugin="poweradminbf3">
                <settings name="scrambler">
                    <set name="strategy">random</set>
                </settings>
            </configuration>""")
        self.p._load_scrambler()
        self.setSTragegy_mock.assert_called_once_with('random')

    def test_score(self):
        self.conf.loadFromString("""<configuration plugin="poweradminbf3">
                <settings name="scrambler">
                    <set name="strategy">score</set>
                </settings>
            </configuration>""")
        self.p._load_scrambler()
        self.setSTragegy_mock.assert_called_once_with('score')




class Test_load_scrambler__gamemodes_blacklist(Test_conf):

    def test_no_section(self):
        self.conf.loadFromString("""<configuration plugin="poweradminbf3"/>""")
        self.p._load_scrambler()
        self.assertEqual([], self.p._autoscramble_gamemode_blacklist)

    def test_no_option(self):
        self.conf.loadFromString("""<configuration plugin="poweradminbf3">
                <settings name="scrambler"/>
            </configuration>""")
        self.p._load_scrambler()
        self.assertEqual([], self.p._autoscramble_gamemode_blacklist)

    def test_empty_option(self):
        self.conf.loadFromString("""<configuration plugin="poweradminbf3">
                <settings name="scrambler">
                    <set name="gamemodes_blacklist"></set>
                </settings>
            </configuration>""")
        self.p._load_scrambler()
        self.assertEqual([], self.p._autoscramble_gamemode_blacklist)

    def test_bad_option(self):
        self.conf.loadFromString("""<configuration plugin="poweradminbf3">
                <settings name="scrambler">
                    <set name="gamemodes_blacklist">foo</set>
                </settings>
            </configuration>""")
        self.p._load_scrambler()
        self.assertEqual([], self.p._autoscramble_gamemode_blacklist)


    def test_one_valid_gamemode(self):
        self.conf.loadFromString("""<configuration plugin="poweradminbf3">
                <settings name="scrambler">
                    <set name="gamemodes_blacklist">SquadRush0</set>
                </settings>
            </configuration>""")
        self.p._load_scrambler()
        self.assertEqual(['SquadRush0'], self.p._autoscramble_gamemode_blacklist)

    def test_multiple_valid_gamemode(self):
        self.conf.loadFromString("""<configuration plugin="poweradminbf3">
                <settings name="scrambler">
                    <set name="gamemodes_blacklist">SquadRush0|SquadDeathMatch0</set>
                </settings>
            </configuration>""")
        self.p._load_scrambler()
        self.assertEqual(['SquadRush0', 'SquadDeathMatch0'], self.p._autoscramble_gamemode_blacklist)

    def test_mix_valid_and_invalid_gamemode(self):
        self.conf.loadFromString("""<configuration plugin="poweradminbf3">
                <settings name="scrambler">
                    <set name="gamemodes_blacklist">SquadRush0,SquadDeathMatch0 foo | Rush3 ; bar ! Conquest4</set>
                </settings>
            </configuration>""")
        self.p._load_scrambler()
        self.assertEqual(['SquadRush0', 'SquadDeathMatch0', 'Rush3', 'Conquest4'], self.p._autoscramble_gamemode_blacklist)
