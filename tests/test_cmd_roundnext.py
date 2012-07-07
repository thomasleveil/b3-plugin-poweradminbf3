# -*- encoding: utf-8 -*-
import time
from mock import patch, call
from b3.config import CfgConfigParser
from poweradminbf3 import Poweradminbf3Plugin
from tests import Bf3TestCase



class Test_cmd_roundnext(Bf3TestCase):

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
roundnext: 20
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()
        self.superadmin.connects('superadmin')


    def test_nominal(self):
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!roundnext')
        self.assertEqual([], self.superadmin.message_history)
        self.console.write.assert_has_calls([call(('mapList.runNextRound',))])
