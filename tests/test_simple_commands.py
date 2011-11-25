# -*- encoding: utf-8 -*-
from tests import prepare_fakeparser_for_tests
prepare_fakeparser_for_tests()

from b3.fake import fakeConsole, superadmin
from poweradminbf3 import Poweradminbf3Plugin
from b3.config import XmlConfigParser



conf = XmlConfigParser()
conf.loadFromString("""
<configuration plugin="poweradminbf3">
  <settings name="commands">
    <set name="punkbuster-pb">100</set>
    <set name="roundnext-rnext">40</set>
    <set name="roundrestart-rrestart">40</set>
  </settings>
</configuration>
""")

p = Poweradminbf3Plugin(fakeConsole, conf)
p.onLoadConfig()
p.onStartup()

superadmin.connects('superadmin')

print "\n\n####################################### test basic commands. They should all work"
superadmin.says("!roundnext")
superadmin.says("!rnext")
superadmin.says("!roundrestart")
superadmin.says("!rrestart")
superadmin.says("!punkbuster")
superadmin.says("!pb some command")