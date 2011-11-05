# -*- encoding: utf-8 -*-
from test import prepare_fakeparser_for_tests

prepare_fakeparser_for_tests()

from b3.fake import fakeConsole, superadmin, FakeConsole
from poweradminbf3 import Poweradminbf3Plugin
from b3.config import XmlConfigParser



conf = XmlConfigParser()
conf.loadFromString("""
<configuration plugin="poweradminbf3">
  <settings name="commands">
    <set name="setnextmap-snmap">20</set>
  </settings>
</configuration>
""")

p = Poweradminbf3Plugin(fakeConsole, conf)
p.onLoadConfig()
p.onStartup()

superadmin.connects('superadmin')

print "#"*80 ###################################### test basic commands
superadmin.says('!setnextmap')


print "\n"*2 +  "="*50 + " case map name not recognised"
def my_getMapsSoundingLike_3_suggestions(mapname): return ['map #1', 'map #2', 'map #3']
fakeConsole.getMapsSoundingLike = my_getMapsSoundingLike_3_suggestions
superadmin.says('!snmap somemap')


def my_getMapsSoundingLike_map_found(mapname): return ['MAP_001']
fakeConsole.getMapsSoundingLike = my_getMapsSoundingLike_map_found

def my_getEasyName(mapId):
    return "MAP #1"
fakeConsole.getEasyName = my_getEasyName

bf3_server_responses = {
    ('mapList.list',): [1, 3, 'MAP_001', 'gamemode1', 3],
    ('mapList.getRounds',): [0, 1],
    ('mapList.getMapIndices', ): [0, 0]
}
original_write_function = fakeConsole.write
def my_write_function(data, *args):
    if data in bf3_server_responses:
        #print "BF3(%r) --> %r" % (data, bf3_server_responses[data])
        return bf3_server_responses[data]
    else:
        return original_write_function(data, *args)
fakeConsole.write = my_write_function


print "\n\n====================================== case empty map rotation list"
bf3_server_responses = {
    ('mapList.list',): [0, 3],
    ('mapList.getRounds',): [0, 1],
    ('mapList.getMapIndices', ): [0, 0]
}
superadmin.says('!snmap somemap')


print "\n\n====================================== case wanted map in current map rotation list"
bf3_server_responses = {
    ('mapList.list',): [5, 3,
                        'MAP_A','gamode_A','1',
                        'MAP_B','gamemode_B','1',
                        'MAP_001','gamemode1','1',
                        'MAP_C','gamdemode_C','1',
                        'MAP_D','gamemode_D','1'],
    ('mapList.getRounds',): [0, 1],
    ('mapList.getMapIndices', ): [0, 1]
}
superadmin.says('!snmap somemap')

print "\n\n====================================== case wanted map in current map rotation list, wanted map is already the next map"
bf3_server_responses = {
    ('mapList.list',): [5, 3,
                        'MAP_A','gamode_A','1',
                        'MAP_B','gamemode_B','1',
                        'MAP_001','gamemode1','1',
                        'MAP_C','gamdemode_C','1',
                        'MAP_D','gamemode_D','1'],
    ('mapList.getRounds',): [0, 1],
    ('mapList.getMapIndices', ): [0, 2]
}
superadmin.says('!snmap somemap')


print "\n\n====================================== case wanted map in current map rotation list multiple times"
bf3_server_responses = {
    ('mapList.list',): [10, 3,
                        'MAP_A','gamemode','1',
                        'MAP_B','gamemode','1',
                        'MAP_001','gamemode','1', #2
                        'MAP_C','gamemode','1',
                        'MAP_D','gamemode','1',
                        'MAP_E','gamemode','1',
                        'MAP_001','gamemode','1', #6
                        'MAP_F','gamemode','1',
                        'MAP_G','gamemode','1',
                        'MAP_H','gamemode','1',
    ],
    ('mapList.getRounds',): [0, 1],
    ('mapList.getMapIndices', ): [0, 1]
}
superadmin.says('!snmap somemap')
bf3_server_responses[('mapList.getMapIndices', )] = [2, 3]
superadmin.says('!snmap somemap')
bf3_server_responses[('mapList.getMapIndices', )] = [6, 7]
superadmin.says('!snmap somemap')


