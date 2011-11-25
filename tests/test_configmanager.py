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

# reduce the delay before configmanager loads the config files
p._configmanager_delay = .01

assert p._configmanager is True

print "------------------------ should load b3_main.cfg "
fakeConsole.game.mapName = 'MP_001'
fakeConsole.game.gameType = 'SillyGameType'
fakeConsole.queueEvent(b3.events.Event(b3.events.EVT_GAME_ROUND_START, None))

time.sleep(1)
print "------------------------ should load b3_conquestsmall0.cfg"
fakeConsole.game.mapName = 'MP_001'
fakeConsole.game.gameType = 'ConquestSmall0'
fakeConsole.queueEvent(b3.events.Event(b3.events.EVT_GAME_ROUND_START, None))

time.sleep(1)
print "------------------------ should load b3_conquestsmall0_mp_012"
fakeConsole.game.mapName = 'MP_012'
fakeConsole.game.gameType = 'ConquestSmall0'
fakeConsole.queueEvent(b3.events.Event(b3.events.EVT_GAME_ROUND_START, None))
