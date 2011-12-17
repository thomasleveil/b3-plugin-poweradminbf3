# -*- encoding: utf-8 -*-
import os
import b3
import time
from tests import prepare_fakeparser_for_tests
prepare_fakeparser_for_tests()

from b3.fake import fakeConsole

from poweradminbf3 import Poweradminbf3Plugin

from b3.config import XmlConfigParser

conf = XmlConfigParser()
conf.setXml("""
<configuration plugin="poweradminbf3">
    <settings name="configmanager">
        <set name="status">on</set>
    </settings>
</configuration>
""")
# make B3 think it has a config file on the filesystem
conf.fileName = os.path.join(os.path.dirname(__file__), '../extplugins/conf/plugin_poweradminbf3.xml')

time.sleep(.5)
print "-"*50
p = Poweradminbf3Plugin(fakeConsole, conf)
p.onLoadConfig()
p.onStartup()

def my_getNextMap():
    return nextmap

def my_getHardName(mapname):
    return "MP_007"

fakeConsole.getNextMap = my_getNextMap
fakeConsole.getHardName = my_getHardName


assert p._configmanager is True

print "------------------------ should load b3_main.cfg"
nextmap = "Caspian Border (Squad Deathmatch)"
fakeConsole.queueEvent(b3.events.Event(b3.events.EVT_GAME_ROUND_END, None))

# create a file "b3_teamdeathmatch0.cfg" in config folder to test below
#time.sleep(1)

#print "------------------------ should load b3_teamdeathmatch0.cfg"
#nextmap = "Caspian Border (Team Deathmatch)"
#fakeConsole.queueEvent(b3.events.Event(b3.events.EVT_GAME_ROUND_END, None))