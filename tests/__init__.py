import sys
import threading

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest
from mock import patch
import logging
logging.raiseExceptions = False  # get rid of 'No handlers could be found for logger output' message
from b3.update import B3version
from poweradminbf3 import MIN_BF3_PARSER_VERSION
from b3 import TEAM_UNKNOWN
from b3.config import XmlConfigParser
from b3.parsers.bf3 import Bf3Parser, __version__ as bf3_version
from b3.plugins.admin import AdminPlugin
from b3 import __version__ as b3_version
from b3.update import B3version


import b3.output # do not remove, needed because the module alters some defaults of the logging module
log = logging.getLogger('output')
log.setLevel(logging.WARNING)

class logging_disabled(object):
    """
    context manager that temporarily disable logging.

    USAGE:
        with logging_disabled():
            # do stuff
    """
    DISABLED = False

    def __init__(self):
        self.nested = logging_disabled.DISABLED

    def __enter__(self):
        if not self.nested:
            logging.getLogger('output').propagate = False
            logging_disabled.DISABLED = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.nested:
            logging.getLogger('output').propagate = True
            logging_disabled.DISABLED = False



@unittest.skipIf(B3version(bf3_version) < B3version(MIN_BF3_PARSER_VERSION),
                 "plugin requires B3 BF3 parser v%s or above (current is %s)" % (MIN_BF3_PARSER_VERSION, bf3_version))
class Bf3TestCase(unittest.TestCase):
    """
    Test case that is suitable for testing BF3 parser specific features
    """

    @classmethod
    def setUpClass(cls):
        # less logging
        logging.getLogger('output').setLevel(logging.ERROR)

        with logging_disabled():
            from b3.parsers.frostbite2.abstractParser import AbstractParser
            from b3.fake import FakeConsole
        AbstractParser.__bases__ = (FakeConsole,)
        # Now parser inheritance hierarchy is :
        # Bf3Parser -> AbstractParser -> FakeConsole -> Parser

        # add method changes_team(newTeam, newSquad=None) to FakeClient
        def changes_team(self, newTeam, newSquad=None):
            self.console.OnPlayerTeamchange(data=[self.cid, newTeam, newSquad if newSquad else self.squad], action=None)

        from b3.fake import FakeClient
        FakeClient.changes_team = changes_team

    def setUp(self):
        # create a BF3 parser
        self.parser_conf = XmlConfigParser()
        self.parser_conf.loadFromString("""<configuration />""")
        with logging_disabled():
            self.console = Bf3Parser(self.parser_conf)

        # alter a few settings to speed up the tests
        self.console.sayqueue_get_timeout = 0
        self.console._settings['message_delay'] = 0

        with logging_disabled():
            self.console.startup()

        # load the admin plugin
        if B3version(b3_version) >= B3version("1.10dev"):
            admin_plugin_conf_file = '@b3/conf/plugin_admin.ini'
        else:
            admin_plugin_conf_file = '@b3/conf/plugin_admin.xml'
        with logging_disabled():
            self.adminPlugin = AdminPlugin(self.console, admin_plugin_conf_file)
            self.adminPlugin.onStartup()

        # make sure the admin plugin obtained by other plugins is our admin plugin
        def getPlugin(name):
            if name == 'admin':
                return self.adminPlugin
            else:
                return self.console.getPlugin(name)
        self.console.getPlugin = getPlugin

        self.console.patch_b3_admin_plugin()

        # prepare a few players
        with logging_disabled():
            from b3.fake import FakeClient
            self.joe = FakeClient(self.console, name="Joe", exactName="Joe", guid="zaerezarezar", groupBits=1, team=TEAM_UNKNOWN, teamId=0, squad=0)
            self.simon = FakeClient(self.console, name="Simon", exactName="Simon", guid="qsdfdsqfdsqf", groupBits=0, team=TEAM_UNKNOWN, teamId=0, squad=0)
            self.reg = FakeClient(self.console, name="Reg", exactName="Reg", guid="qsdfdsqfdsqf33", groupBits=4, team=TEAM_UNKNOWN, teamId=0, squad=0)
            self.moderator = FakeClient(self.console, name="Moderator", exactName="Moderator", guid="sdf455ezr", groupBits=8, team=TEAM_UNKNOWN, teamId=0, squad=0)
            self.admin = FakeClient(self.console, name="Level-40-Admin", exactName="Level-40-Admin", guid="875sasda", groupBits=16, team=TEAM_UNKNOWN, teamId=0, squad=0)
            self.superadmin = FakeClient(self.console, name="God", exactName="God", guid="f4qfer654r", groupBits=128, team=TEAM_UNKNOWN, teamId=0, squad=0)


    def tearDown(self):
        self.console.working = False
        self.console.wait_for_threads()
        sys.stdout.write("\tactive threads count : %s " % threading.activeCount())
#        sys.stderr.write("%s\n" % threading.enumerate())
