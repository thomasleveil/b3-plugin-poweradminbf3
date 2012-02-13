# -*- encoding: utf-8 -*-
# http://www.voidspace.org.uk/python/mock/mock.html
from mock import Mock
import b3
from b3.config import XmlConfigParser
from b3.parsers.frostbite2.protocol import CommandFailedError
from poweradminbf3 import Poweradminbf3Plugin
from unittests import Bf3TestCase


class Test_cmd_unlockmode(Bf3TestCase):
    def setUp(self):
        super(Test_cmd_unlockmode, self).setUp()
        self.conf = XmlConfigParser()
        self.conf.loadFromString("""
        <configuration plugin="poweradminbf3">
            <settings name="commands">
                <set name="unlockmode">40</set>
            </settings>
        </configuration>
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()


    def test_get_current_unlockmode(self):
        self.superadmin.connects('superadmin')
        self.console.write.expect(('vars.unlockMode',)).thenReturn(['f00'])
        self.superadmin.message_history = []
        self.superadmin.says('!unlockmode')
        self.console.write.verify_expected_calls()
        self.assertEqual(['Current unlock mode is [f00]'], self.superadmin.message_history)


    def test_bad_argument(self):
        self.superadmin.connects('superadmin')
        self.console.write.expect(('vars.unlockMode',)).thenReturn(['foobar'])
        self.superadmin.message_history = []
        self.superadmin.says('!unlockmode junk')
        self.console.write.verify_expected_calls()
        self.assertEqual(
            ["unexpected value 'junk'. Available modes : all, common, stats, none", 'Current unlock mode is [foobar]'],
            self.superadmin.message_history)


    def test_all(self):
        self.superadmin.connects('superadmin')
        self.console.write.expect(('vars.unlockMode', 'all'))
        self.superadmin.message_history = []
        self.superadmin.says('!unlockmode all')
        self.console.write.verify_expected_calls()
        self.assertEqual(['Unlock mode set to all'], self.superadmin.message_history)


    def test_common(self):
        self.superadmin.connects('superadmin')
        self.console.write.expect(('vars.unlockMode', 'common'))
        self.superadmin.message_history = []
        self.superadmin.says('!unlockmode common')
        self.console.write.verify_expected_calls()
        self.assertEqual(['Unlock mode set to common'], self.superadmin.message_history)


    def test_stats(self):
        self.superadmin.connects('superadmin')
        self.console.write.expect(('vars.unlockMode', 'stats'))
        self.superadmin.message_history = []
        self.superadmin.says('!unlockmode stats')
        self.console.write.verify_expected_calls()
        self.assertEqual(['Unlock mode set to stats'], self.superadmin.message_history)


    def test_none(self):
        self.superadmin.connects('superadmin')
        self.console.write.expect(('vars.unlockMode', 'none'))
        self.superadmin.message_history = []
        self.superadmin.says('!unlockmode none')
        self.console.write.verify_expected_calls()
        self.assertEqual(['Unlock mode set to none'], self.superadmin.message_history)

