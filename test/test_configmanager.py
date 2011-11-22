# -*- encoding: utf-8 -*-
import b3
import os, time
from test import prepare_fakeparser_for_tests
prepare_fakeparser_for_tests()

from b3.fake import fakeConsole
from b3.fake import admin

from poweradminbf3 import Poweradminbf3Plugin

from b3.config import XmlConfigParser

conf = XmlConfigParser()
conf.setXml("""
<configuration plugin="poweradminbf3">
    <settings name="configmanager">
        <set name="status">on</set>
    </settings>
    <settings name="preferences">
        <set name="config_path">%(script_dir)s</set>
    </settings>
</configuration>
""" % {'script_dir': os.path.abspath(os.path.join(os.path.dirname(__file__), '../extplugins/conf/serverconfigs'))})

p = Poweradminbf3Plugin(fakeConsole, conf)
p.onLoadConfig()
p.onStartup()

fakeConsole.game.mapName = 'MP_001'
fakeConsole.game.gameType = 'Conquest64'

fakeConsole.queueEvent(b3.events.Event(b3.events.EVT_GAME_ROUND_START, None))


