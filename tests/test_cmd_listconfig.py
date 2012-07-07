# -*- encoding: utf-8 -*-
import os
from mock import patch
from b3.config import CfgConfigParser
from poweradminbf3 import Poweradminbf3Plugin
from tests import Bf3TestCase


class Test_cmd_listconfig(Bf3TestCase):

    def setUp(self):
        super(Test_cmd_listconfig, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""[commands]
listconfig: 40

[preferences]
config_path: %(script_dir)s
            """ % {'script_dir': os.path.abspath(
            os.path.join(os.path.dirname(__file__), '../extplugins/conf/serverconfigs'))})
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()
        self.admin.connects("admin")
        self.admin.clearMessageHistory()

    def test_nominal(self):
        with patch.object(os, "listdir") as listdir_mock:
            listdir_mock.return_value = ["junk.txt", "conf1.cfg", "conf2.cfg", "hardcore.cfg"]
            self.admin.says('!listconfig')
            self.assertEqual(['Available config files: conf1, conf2, hardcore'], self.admin.message_history)

    def test_no_config(self):
        with patch.object(os, "listdir") as listdir_mock:
            listdir_mock.return_value = ["junk.txt"]
            self.admin.says('!listconfig')
            self.assertEqual(['No server config files found'], self.admin.message_history)
