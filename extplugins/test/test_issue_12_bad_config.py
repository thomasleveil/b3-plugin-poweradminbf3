# -*- encoding: utf-8 -*-
from test import prepare_fakeparser_for_tests
prepare_fakeparser_for_tests()

from b3.fake import fakeConsole
from poweradminbf3 import Poweradminbf3Plugin
from b3.config import XmlConfigParser



conf = XmlConfigParser()
conf.loadFromString("""
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


p = Poweradminbf3Plugin(fakeConsole, conf)
p.onLoadConfig()
p.onStartup()