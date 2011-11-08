# -*- encoding: utf-8 -*-
from test import prepare_fakeparser_for_tests
prepare_fakeparser_for_tests()

from b3.fake import fakeConsole, joe, simon, superadmin, moderator
from poweradminbf3 import Poweradminbf3Plugin
from b3.config import XmlConfigParser


conf = XmlConfigParser()
conf.loadFromString("""
<configuration plugin="poweradminbf3">
  <settings name="commands">
    <set name="swap">40</set>
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
moderator.connects('moderator')
moderator.teamId = 2
moderator.squad = 5
superadmin.connects('superadmin')
superadmin.teamId = 2
superadmin.squad = 6
print "Joe's group is " +  joe.maxGroup.name
print "Simon's group is " + simon.maxGroup.name
print "Moderator's group is " + moderator.maxGroup.name
print "superadmin's group is " +  superadmin.maxGroup.name



print "\n\n####################################### test superadmin says !swap joe"
superadmin.teamId = 2
superadmin.squad = 6
print "superadmin.teamId: %s, squad: %s" % (superadmin.teamId, superadmin.squad)
joe.teamId = 1
joe.squad = 7
print "joe.teamId: %s, squad: %s" % (joe.teamId, joe.squad)
superadmin.says('!swap joe')



print "\n\n####################################### test !swap joe simon"
simon.teamId = 1
simon.squad = 6
print "simon.teamId: %s, squad: %s" % (simon.teamId, simon.squad)
joe.teamId = 1
joe.squad = 6
print "joe.teamId: %s, squad: %s" % (joe.teamId, joe.squad)
superadmin.says("!swap joe simon")



print "\n\n####################################### test !swap joe simon"
print "simon.teamId: %s, squad: %s" % (simon.teamId, simon.squad)
joe.squad = 2
print "joe.teamId: %s, squad: %s" % (joe.teamId, joe.squad)
superadmin.says("!swap joe simon")

