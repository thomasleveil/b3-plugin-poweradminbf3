# -*- encoding: utf-8 -*-
import time
from mock import patch, call
from b3.config import XmlConfigParser
from poweradminbf3 import Poweradminbf3Plugin
from tests import Bf3TestCase



class Test_cmd_punkbuster(Bf3TestCase):

    def setUp(self):
        Bf3TestCase.setUp(self)
        self.conf = XmlConfigParser()
        self.conf.loadFromString("""
        <configuration plugin="poweradminbf3">
            <settings name="commands">
                <set name="punkbuster-punk">20</set>
            </settings>
        </configuration>
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()
        self.superadmin.connects('superadmin')


    def test_pb_inactive(self):
        self.console.write.expect(('punkBuster.isActive',)).thenReturn(['false'])
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!punkbuster test')
        self.assertEqual(['Punkbuster is not active'], self.superadmin.message_history)
        self.console.write.verify_expected_calls()

    def test_pb_active(self):
        self.console.write.expect(('punkBuster.isActive',)).thenReturn(['true'])
        self.console.write.expect(('punkBuster.pb_sv_command', 'test'))
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!punkbuster test')
        self.assertEqual([], self.superadmin.message_history)
        self.console.write.verify_expected_calls()

    def test_pb_active(self):
        self.console.write.expect(('punkBuster.isActive',)).thenReturn(['true'])
        self.console.write.expect(('punkBuster.pb_sv_command', 'test'))
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!punk test')
        self.assertEqual([], self.superadmin.message_history)
        self.console.write.verify_expected_calls()
