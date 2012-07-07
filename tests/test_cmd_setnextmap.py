# -*- encoding: utf-8 -*-
# http://www.voidspace.org.uk/python/mock/mock.html
import logging
from b3.config import CfgConfigParser
from poweradminbf3 import Poweradminbf3Plugin
from tests import Bf3TestCase, Mockito


class Test_cmd_setnextmap(Bf3TestCase):
    def setUp(self):
        super(Test_cmd_setnextmap, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""[commands]
setnextmap-snmap: 20
        """)
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()

        logging.getLogger('output').setLevel(logging.DEBUG)
        self.console.game.gameType = 'currentGamemode'


    def test_no_argument(self):
        self.superadmin.connects('superadmin')
        self.superadmin.message_history = []
        self.superadmin.says('!setnextmap')
        self.assertEqual(['Invalid or missing data, try !help setnextmap'], self.superadmin.message_history)


    def test_my_getMapsSoundingLike_3_suggestions(self):
        self.console.getMapsSoundingLike = Mockito(wraps=self.console.getMapsSoundingLike)
        self.console.getMapsSoundingLike.expect('somemap').thenReturn(['map #1', 'map #2', 'map #3'])
        self.superadmin.connects('superadmin')
        self.superadmin.message_history = []
        self.superadmin.says('!setnextmap somemap')
        self.console.getMapsSoundingLike.verify_expected_calls()
        self.assertEqual(['do you mean : map #1, map #2, map #3 ?'], self.superadmin.message_history)

    def test_my_getMapsSoundingLike_finds_the_map(self):
        self.console.getMapsSoundingLike = Mockito(wraps=self.console.getMapsSoundingLike)
        self.console.getMapsSoundingLike.expect('somemap').thenReturn('MAP_001')

        self.console.write.expect(('mapList.list',)).thenReturn([5, 3,
                                                                 'MAP_A', 'gamode_A', '1',
                                                                 'MAP_B', 'gamemode_B', '1',
                                                                 'MAP_001', 'gamemode1', '1',
                                                                 'MAP_C', 'gamdemode_C', '1',
                                                                 'MAP_D', 'gamemode_D', '1'])
        self.console.write.expect(('mapList.getRounds',)).thenReturn([0, 1])
        self.console.write.expect(('mapList.getMapIndices',)).thenReturn([0, 1])

        self.superadmin.connects('superadmin')
        self.superadmin.message_history = []
        self.superadmin.says('!setnextmap somemap')
        self.console.getMapsSoundingLike.verify_expected_calls()
        self.assertEqual(['next map set to MAP_001'], self.superadmin.message_history)

    def test_empty_list(self):
        self.console.getMapsSoundingLike = Mockito(wraps=self.console.getMapsSoundingLike)
        self.console.getMapsSoundingLike.expect('map1').thenReturn('MAP_001')

        self.console.write.expect(('mapList.list',)).thenReturn([0, 3])
        self.console.write.expect(('mapList.getRounds',)).thenReturn([0, 1])

        self.console.write.expect(('mapList.add', 'MAP_001', 'currentGamemode', 1, 0))
        self.console.write.expect(('mapList.setNextMapIndex', 0))

        self.superadmin.connects('superadmin')
        self.superadmin.message_history = []
        self.superadmin.says('!snmap map1')
        self.console.getMapsSoundingLike.verify_expected_calls()
        self.console.write.verify_expected_calls()
        self.assertEqual(['next map set to MAP_001'], self.superadmin.message_history)


    def test_wanted_map_is_not_in_list(self):
        self.console.getMapsSoundingLike = Mockito(wraps=self.console.getMapsSoundingLike)
        self.console.getMapsSoundingLike.expect('map1').thenReturn('MAP_001')

        self.console.write.expect(('mapList.list',)).thenReturn([4, 3,
                                                                 'MAP_A', 'gamode_A', '1',
                                                                 'MAP_B', 'gamemode_B', '1',
                                                                 'MAP_C', 'gamdemode_C', '1',
                                                                 'MAP_D', 'gamemode_D', '1'])
        self.console.write.expect(('mapList.getRounds',)).thenReturn([0, 1])
        self.console.write.expect(('mapList.getMapIndices',)).thenReturn([4, 1])

        self.console.write.expect(('mapList.add', 'MAP_001', 'currentGamemode', 1, 5))
        self.console.write.expect(('mapList.setNextMapIndex', 5))

        self.superadmin.connects('superadmin')
        self.superadmin.message_history = []
        self.superadmin.says('!snmap map1')
        self.console.getMapsSoundingLike.verify_expected_calls()
        self.console.write.verify_expected_calls()
        self.assertEqual(['next map set to MAP_001'], self.superadmin.message_history)


    def test_wanted_map_is_in_list(self):
        self.console.getMapsSoundingLike = Mockito(wraps=self.console.getMapsSoundingLike)
        self.console.getMapsSoundingLike.expect('map1').thenReturn('MAP_001')

        self.console.write.expect(('mapList.list',)).thenReturn([5, 3,
                                                                 'MAP_A', 'gamode_A', '1',
                                                                 'MAP_B', 'gamemode_B', '1',
                                                                 'MAP_001', 'gamemode1', '1',
                                                                 'MAP_C', 'gamdemode_C', '1',
                                                                 'MAP_D', 'gamemode_D', '1'])
        self.console.write.expect(('mapList.getRounds',)).thenReturn([0, 1])
        self.console.write.expect(('mapList.getMapIndices',)).thenReturn([0, 1])

        self.console.write.expect(('mapList.setNextMapIndex', 2))

        self.superadmin.connects('superadmin')
        self.superadmin.message_history = []
        self.superadmin.says('!snmap map1')
        self.console.getMapsSoundingLike.verify_expected_calls()
        self.console.write.verify_expected_calls()
        self.assertEqual(['next map set to MAP_001'], self.superadmin.message_history)


    def test_wanted_map_is_already_the_next_map(self):
        self.console.getMapsSoundingLike = Mockito(wraps=self.console.getMapsSoundingLike)
        self.console.getMapsSoundingLike.expect('map1').thenReturn('MAP_001')

        self.console.write.expect(('mapList.list',)).thenReturn([5, 3,
                                                                 'MAP_A', 'gamode_A', '1',
                                                                 'MAP_B', 'gamemode_B', '1',
                                                                 'MAP_001', 'gamemode1', '1',
                                                                 'MAP_C', 'gamdemode_C', '1',
                                                                 'MAP_D', 'gamemode_D', '1'])
        self.console.write.expect(('mapList.getRounds',)).thenReturn([0, 1])
        self.console.write.expect(('mapList.getMapIndices',)).thenReturn([0, 2])

        self.console.write.expect(('mapList.setNextMapIndex', 2))

        self.superadmin.connects('superadmin')
        self.superadmin.message_history = []
        self.superadmin.says('!snmap map1')
        self.console.getMapsSoundingLike.verify_expected_calls()
        self.console.write.verify_expected_calls()
        self.assertEqual(['next map set to MAP_001'], self.superadmin.message_history)


    def test_wanted_map_is_in_the_list_multiple_times(self):
        self.console.getMapsSoundingLike = Mockito(wraps=self.console.getMapsSoundingLike)
        self.console.getMapsSoundingLike.expect('map1').thenReturn('MAP_001')

        self.console.write.expect(('mapList.list',)).thenReturn([10, 3,
                                                                 'MAP_A', 'gamemode', '1',
                                                                 'MAP_B', 'gamemode', '1',
                                                                 'MAP_001', 'gamemode', '1', #2
                                                                 'MAP_C', 'gamemode', '1',
                                                                 'MAP_D', 'gamemode', '1',
                                                                 'MAP_E', 'gamemode', '1',
                                                                 'MAP_001', 'gamemode', '1', #6
                                                                 'MAP_F', 'gamemode', '1',
                                                                 'MAP_G', 'gamemode', '1',
                                                                 'MAP_H', 'gamemode', '1',
                                                                 ])
        self.console.write.expect(('mapList.getRounds',)).thenReturn([0, 1])
        self.console.write.expect(('mapList.getMapIndices',)).thenReturn([0, 1])

        self.console.write.expect(('mapList.setNextMapIndex', 2))

        self.superadmin.connects('superadmin')
        self.superadmin.message_history = []
        self.superadmin.says('!snmap map1')
        self.console.getMapsSoundingLike.verify_expected_calls()
        self.console.write.verify_expected_calls()
        self.assertEqual(['next map set to MAP_001'], self.superadmin.message_history)


    def test_wanted_map_is_in_the_list_multiple_times_2(self):
        self.console.getMapsSoundingLike = Mockito(wraps=self.console.getMapsSoundingLike)
        self.console.getMapsSoundingLike.expect('map1').thenReturn('MAP_001')

        self.console.write.expect(('mapList.list',)).thenReturn([10, 3,
                                                                 'MAP_A', 'gamemode', '1',
                                                                 'MAP_B', 'gamemode', '1',
                                                                 'MAP_001', 'gamemode', '1', #2
                                                                 'MAP_C', 'gamemode', '1',
                                                                 'MAP_D', 'gamemode', '1',
                                                                 'MAP_E', 'gamemode', '1',
                                                                 'MAP_001', 'gamemode', '1', #6
                                                                 'MAP_F', 'gamemode', '1',
                                                                 'MAP_G', 'gamemode', '1',
                                                                 'MAP_H', 'gamemode', '1',
                                                                 ])
        self.console.write.expect(('mapList.getRounds',)).thenReturn([0, 1])
        self.console.write.expect(('mapList.getMapIndices',)).thenReturn([2, 3])

        self.console.write.expect(('mapList.setNextMapIndex', 6))

        self.superadmin.connects('superadmin')
        self.superadmin.message_history = []
        self.superadmin.says('!snmap map1')
        self.console.getMapsSoundingLike.verify_expected_calls()
        self.console.write.verify_expected_calls()
        self.assertEqual(['next map set to MAP_001'], self.superadmin.message_history)


    def test_wanted_map_is_in_the_list_multiple_times_3(self):
        self.console.getMapsSoundingLike = Mockito(wraps=self.console.getMapsSoundingLike)
        self.console.getMapsSoundingLike.expect('map1').thenReturn('MAP_001')

        self.console.write.expect(('mapList.list',)).thenReturn([10, 3,
                                                                 'MAP_A', 'gamemode', '1',
                                                                 'MAP_B', 'gamemode', '1',
                                                                 'MAP_001', 'gamemode', '1', #2
                                                                 'MAP_C', 'gamemode', '1',
                                                                 'MAP_D', 'gamemode', '1',
                                                                 'MAP_E', 'gamemode', '1',
                                                                 'MAP_001', 'gamemode', '1', #6
                                                                 'MAP_F', 'gamemode', '1',
                                                                 'MAP_G', 'gamemode', '1',
                                                                 'MAP_H', 'gamemode', '1',
                                                                 ])
        self.console.write.expect(('mapList.getRounds',)).thenReturn([0, 1])
        self.console.write.expect(('mapList.getMapIndices',)).thenReturn([6, 7])

        self.console.write.expect(('mapList.setNextMapIndex', 2))

        self.superadmin.connects('superadmin')
        self.superadmin.message_history = []
        self.superadmin.says('!snmap map1')
        self.console.getMapsSoundingLike.verify_expected_calls()
        self.console.write.verify_expected_calls()
        self.assertEqual(['next map set to MAP_001'], self.superadmin.message_history)

