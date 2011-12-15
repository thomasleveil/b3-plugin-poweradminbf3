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
    <set name="unlockmode">40</set>
  </settings>
</configuration>
""")

p = Poweradminbf3Plugin(fakeConsole, conf)
p.onLoadConfig()
p.onStartup()

superadmin.connects('superadmin')


print "\n\n####################################### !unlockmode"
superadmin.says('!unlockmode')
superadmin.says('@unlockmode')

print "\n\n####################################### !unlockmode junk"
superadmin.says('!unlockmode junk')
superadmin.says('@unlockmode junk')

print "\n\n####################################### !unlockmode all"
superadmin.says('!unlockmode all')
superadmin.says('@unlockmode all')

print "\n\n####################################### !unlockmode common"
superadmin.says('!unlockmode common')

print "\n\n####################################### !unlockmode stats"
superadmin.says('!unlockmode stats')

print "\n\n####################################### !unlockmode none"
superadmin.says('!unlockmode none')


