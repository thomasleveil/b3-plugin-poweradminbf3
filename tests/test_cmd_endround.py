# -*- encoding: utf-8 -*-
import time
# http://www.voidspace.org.uk/python/mock/mock.html
from mock import patch
from b3.config import CfgConfigParser
from poweradminbf3 import Poweradminbf3Plugin
from tests import Bf3TestCase, Mockito



class Test_cmd_endround(Bf3TestCase):

    @classmethod
    def setUpClass(cls):
        Bf3TestCase.setUpClass()
        cls.sleep_patcher = patch.object(time, "sleep")
        cls.sleep_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.sleep_patcher.stop()

    def setUp(self):
        Bf3TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""[commands]
endround: 20
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()
        self.superadmin.connects('superadmin')


    def test_frostbite_error(self):
        self.console.write = Mockito(wraps=self.console.write)
        self.console.write.expect(('serverInfo',)).thenReturn(['i3D.net - BigBrotherBot #3 (DE)', '0', '16', 'ConquestLarge0', 'MP_007', '0', '2',
                                                               '2', '300', '300', '0', '', 'false', 'true', 'false', '105473', '105450', '', '', '', 'EU', 'AMS', 'DE'])
        self.console.write.expect(('mapList.endRound', '1'))
        self.superadmin.message_history = []
        self.superadmin.says("!endround")

        self.assertEqual([], self.superadmin.message_history)
        self.console.write.verify_expected_calls()


    def test_no_argument_team1_winning(self):
        self.console.write = Mockito(wraps=self.console.write)
        self.console.write.expect(('mapList.endRound', '1'))
        self.console.write.expect(('serverInfo',)).thenReturn(['i3D.net - BigBrotherBot #3 (DE)', '0', '16', 'ConquestLarge0', 'MP_007', '0', '2',
                                                               '2', '800', '90', '0', '', 'true', 'true', 'false', '105473', '105450', '', '', '', 'EU', 'AMS', 'DE'])
        self.superadmin.message_history = []
        self.superadmin.says("!endround")
        self.console.write.verify_expected_calls()
        self.assertEqual([], self.superadmin.message_history)

    def test_no_argument_team2_winning(self):
        self.console.write = Mockito(wraps=self.console.write)
        self.console.write.expect(('mapList.endRound', '2'))
        self.console.write.expect(('serverInfo',)).thenReturn(['i3D.net - BigBrotherBot #3 (DE)', '0', '16', 'ConquestLarge0', 'MP_007', '0', '2',
                                                               '2', '400', '1300', '0', '', 'true', 'true', 'false', '105473', '105450', '', '', '', 'EU', 'AMS', 'DE'])

        self.superadmin.message_history = []
        self.superadmin.says("!endround")
        self.console.write.verify_expected_calls()
        self.assertEqual([], self.superadmin.message_history)
        self.assertEqual([], self.superadmin.message_history)


    def test_no_argument_team4_winning(self):
        self.console.write = Mockito(wraps=self.console.write)
        self.console.write.expect(('mapList.endRound', '4'))
        self.console.write.expect(('serverInfo',)).thenReturn(['i3D.net - BigBrotherBot #3 (DE)', '0', '16', 'ConquestLarge0', 'MP_007', '0', '2',
                                                               '4', '400', '1300', '45', '1651' '0', '', 'true', 'true', 'false', '105473', '105450', '', '', '', 'EU', 'AMS', 'DE'])

        self.superadmin.message_history = []
        self.superadmin.says("!endround")
        self.console.write.verify_expected_calls()
        self.assertEqual([], self.superadmin.message_history)



    def test_0(self):
        self.console.write = Mockito(wraps=self.console.write)
        self.console.write.expect(('mapList.endRound', '0'))
        self.superadmin.message_history = []
        self.superadmin.says("!endround 0")
        self.console.write.verify_expected_calls()
        self.assertEqual([], self.superadmin.message_history)



    def test_1(self):
        self.console.write = Mockito(wraps=self.console.write)
        self.console.write.expect(('mapList.endRound', '1'))
        self.superadmin.message_history = []
        self.superadmin.says("!endround 1")
        self.console.write.verify_expected_calls()
        self.assertEqual([], self.superadmin.message_history)
