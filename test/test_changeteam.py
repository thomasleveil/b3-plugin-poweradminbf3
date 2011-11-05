# -*- encoding: utf-8 -*-
from test import prepare_fakeparser_for_tests
prepare_fakeparser_for_tests()

from b3.fake import fakeConsole, joe, simon, superadmin
from poweradminbf3 import Poweradminbf3Plugin
from b3.config import XmlConfigParser


conf = XmlConfigParser()
conf.loadFromString("""
<configuration plugin="poweradminbf3">
  <settings name="commands">
    <set name="changeteam-ct">40</set>
  </settings>
</configuration>
""")

p = Poweradminbf3Plugin(fakeConsole, conf)
p.onLoadConfig()
p.onStartup()

simon.connects("simon")
simon.teamId = 1
simon.squad = 7
joe.connects('Joe')
joe.teamId = 1
joe.squad = 7
superadmin.connects('superadmin')
superadmin.teamId = 2
superadmin.squad = 6
print "Joe's group is " +  joe.maxGroup.name
print "Simon's group is " + simon.maxGroup.name
print "superadmin's group is " +  superadmin.maxGroup.name


print "#"*80 ###################################### test !changeteam
superadmin.says("!changeteam joe")
p._adminPlugin._commands["changeteam"].level = 0,100
joe.says("!ct god")
joe.says("!changeteam simon")

