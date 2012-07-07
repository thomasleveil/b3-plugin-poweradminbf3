# -*- encoding: utf-8 -*-
import os
from mock import Mock, patch # http://www.voidspace.org.uk/python/mock/

from poweradminbf3 import Poweradminbf3Plugin, __file__ as poweradminbf3_file
from b3.config import CfgConfigParser

from tests import Bf3TestCase

class Test_server_config_path(Bf3TestCase):
    existing_paths = []

    def setUp(self):
        Bf3TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.setExistingPaths([])

    def setExistingPaths(self, paths):
        """set the paths that os.path.isdir will consider to exist"""
        self.__class__.existing_paths = paths

    @staticmethod
    def isdir(path):
        path = os.path.normpath(path)
        for p in Test_server_config_path.existing_paths:
            if path == os.path.normpath(p):
                print "isdir(%s) ? True" % path
                return True
        print "isdir(%s) ? False" % path
        return False


    def test_1(self):
        """nothing in config, no plugin config file, no b3 config file"""
        self.conf.loadFromString("""
[preferences]

        """)
        # the plugin config does not exist on the filesystem
        p = Poweradminbf3Plugin(self.console, self.conf)
        p.onLoadConfig()
        self.assertIsNone(p._configPath)


    def test_2(self):
        """nothing in config, no plugin config file, b3 config file"""
        self.conf.loadFromString("""
[preferences]

        """)
        # the plugin config does not exist on the filesystem

        p = Poweradminbf3Plugin(self.console, self.conf)
        # make B3 think it has a config file on the filesystem
        p.console.config.fileName = "somewhere/on/the/filesystem/b3conf/b3.xml"

        self.setExistingPaths(["somewhere/on/the/filesystem/b3conf/serverconfigs"])
        with patch.object(os.path, 'isdir', Mock(side_effect=Test_server_config_path.isdir)):
            p.onLoadConfig()

        self.assertEqual(os.path.normpath("somewhere/on/the/filesystem/b3conf/serverconfigs"), p._configPath)


    def test_2bis(self):
        """nothing in config, plugin config file, no b3 config file"""
        self.conf.loadFromString("""
[preferences]

        """)
        self.conf.fileName = "somewhere/on/the/filesystem/plugin_poweradminbf3.ini"

        p = Poweradminbf3Plugin(self.console, self.conf)

        self.setExistingPaths(["somewhere/on/the/filesystem//serverconfigs"])
        with patch.object(os.path, 'isdir', Mock(side_effect=Test_server_config_path.isdir)):
            p.onLoadConfig()

        self.assertEqual(os.path.normpath("somewhere/on/the/filesystem//serverconfigs"), p._configPath)


    def test_3(self):
        """junk in config, no plugin config file, no b3 config file"""
        self.conf.loadFromString("""
[preferences]
config_path: I don't exists
        """)

        p = Poweradminbf3Plugin(self.console, self.conf)
        p.onLoadConfig()
        self.assertIsNone(p._configPath)


    def test_4(self):
        """absolute existing path in config file"""
        self.conf.loadFromString("""
[preferences]
config_path: /somewhere/on/the/filesystem/
        """)
        p = Poweradminbf3Plugin(self.console, self.conf)

        self.setExistingPaths(['/somewhere/on/the/filesystem/'])
        with patch.object(os.path, 'isdir', Mock(side_effect=Test_server_config_path.isdir)):
            p.onLoadConfig()

        self.assertEqual(os.path.normpath('/somewhere/on/the/filesystem/'), p._configPath)


    def test_5(self):
        """existing path in config file relative to b3 config directory"""
        self.conf.loadFromString("""
[preferences]
config_path: subdirectory
        """)
        p = Poweradminbf3Plugin(self.console, self.conf)
        # make B3 think it has a config file on the filesystem
        p.console.config.fileName = "somewhere/on/the/filesystem/b3conf/b3.xml"

        self.setExistingPaths(['somewhere/on/the/filesystem/b3conf/subdirectory'])
        with patch.object(os.path, 'isdir', Mock(side_effect=Test_server_config_path.isdir)):
            p.onLoadConfig()

        self.assertEqual(os.path.normpath('somewhere/on/the/filesystem/b3conf/subdirectory'), p._configPath)

    def test_6(self):
        """existing path in config file relative to plugin config directory"""
        self.conf.loadFromString("""
[preferences]
config_path: subdirectory
        """)
        self.conf.fileName = "somewhere/on/the/filesystem/plugin_poweradminbf3.ini"

        p = Poweradminbf3Plugin(self.console, self.conf)

        self.setExistingPaths(["somewhere/on/the/filesystem/subdirectory"])
        with patch.object(os.path, 'isdir', Mock(side_effect=Test_server_config_path.isdir)):
            p.onLoadConfig()

        self.assertEqual(os.path.normpath('somewhere/on/the/filesystem/subdirectory'), p._configPath)


