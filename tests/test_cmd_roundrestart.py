# -*- encoding: utf-8 -*-
import time
from mock import patch, call
from mockito import verify, when
from b3.config import CfgConfigParser
from poweradminbf3 import Poweradminbf3Plugin
from tests import Bf3TestCase



class Test_cmd_roundrestart(Bf3TestCase):

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
roundrestart: 20
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()
        self.superadmin.connects('superadmin')


    def test_nominal(self):
        when(self.console).write()
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!roundrestart')
        self.assertEqual([], self.superadmin.message_history)
        verify(self.console).write(('mapList.restartRound',))
