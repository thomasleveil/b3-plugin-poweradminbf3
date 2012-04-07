# -*- encoding: utf-8 -*-
import os
from mock import Mock, patch # http://www.voidspace.org.uk/python/mock/

from poweradminbf3 import Poweradminbf3Plugin, __file__ as poweradminbf3_file
from b3.config import XmlConfigParser

from tests import Bf3TestCase

class Test_conf(Bf3TestCase):

    def setUp(self):
        Bf3TestCase.setUp(self)
        self.conf = XmlConfigParser()

    def test_1(self):
        self.conf.loadFromString("""<configuration plugin="poweradminbf3"/>""")
        p = Poweradminbf3Plugin(self.console, self.conf)
        p.onLoadConfig()
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
        p = Poweradminbf3Plugin(self.console, self.conf)
        p.onLoadConfig()
        # should not raise any error