# -*- encoding: utf-8 -*-
from tests import prepare_fakeparser_for_tests
prepare_fakeparser_for_tests()

from b3.fake import fakeConsole, joe, simon, superadmin, FakeClient
from poweradminbf3 import Poweradminbf3Plugin
from b3.config import XmlConfigParser


conf = XmlConfigParser()
conf.loadFromString("""
<configuration plugin="poweradminbf3">
  <settings name="commands">
    <set name="changeteam-ct">0</set>
  </settings>
</configuration>
""")

p = Poweradminbf3Plugin(fakeConsole, conf)
p.onLoadConfig()
p.onStartup()

simon.connects("simon")
simon.teamId = 1
joe.connects('Joe')
joe.teamId = 1
jack = FakeClient(fakeConsole, name="Jack", exactName="Jack", guid="azerazerzarazrzae", groupBits=1)
jack.connects('Jack')
jack.teamId = 1
superadmin.connects('superadmin')
superadmin.teamId = 2
print "Joe's group is " +  joe.maxGroup.name
print "Jack's group is " +  jack.maxGroup.name
print "Simon's group is " + simon.maxGroup.name
print "superadmin's group is " +  superadmin.maxGroup.name


print "\n\n####################################### test !changeteam"
superadmin.says("!changeteam joe")


print "\n\n####################################### Joe should not be able to !changeteam a higher level player"
assert joe.maxLevel < superadmin.maxLevel
joe.says("!ct god")

print "\n\n####################################### Joe should be able to !changeteam a lower level player"
assert joe.maxLevel > simon.maxLevel
joe.says("!changeteam simon")

print "\n\n####################################### Jack should be able to !changeteam an equal level player"
assert joe.maxLevel == jack.maxLevel
jack.says("!changeteam joe")

