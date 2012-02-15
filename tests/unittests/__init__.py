import logging
import unittest
# http://www.voidspace.org.uk/python/mock/mock.html
from mock import Mock, callargs, DEFAULT as mock_DEFAULT, class_types
from b3 import TEAM_UNKNOWN
from b3.config import XmlConfigParser
from b3.fake import FakeClient
from b3.parsers.bf3 import Bf3Parser
from b3.plugins.admin import AdminPlugin



def extends_mock():
    # extend the Mock class
    def assert_was_called_with(self, *args, **kwargs):
        """
        assert that the mock was called with the specified arguments at least once.

        Raises an AssertionError if the args and keyword args passed in are
        different from all calls to the mock.
        """
        if self.call_args is None:
            raise AssertionError('Expected: %s\nNot called' % ((args, kwargs),))
        found = False
        for call_args in self.call_args_list:
            if call_args == (args, kwargs):
                found = True
                break
        if not found:
            raise AssertionError(
                'Expected: %s\nCalled at least once with: %s' % ((args, kwargs), self.call_args_list)
            )
    Mock.assert_was_called_with = assert_was_called_with


class Expector(object):
    def __init__(self):
        self._return_value = Mock()
        self._return_exception = None

    def thenReturn(self, obj):
        self._return_value = obj

    def thenRaise(self, exception):
        self._return_exception = exception


class Mockito(Mock):

    def __init__(self, *args, **kwargs):
        super(Mockito, self).__init__(*args, **kwargs)
        self._expected_calls = dict()


    def expect(self, *args, **kwargs):
        expector = Expector()
        self._expected_calls[repr((args, kwargs))] = (expector, callargs((args, kwargs)))
        return expector

    def verify_expected_calls(self):
        failures = []
        for expected_calls, call_args in self._expected_calls.values():
            if call_args not in self.call_args_list:
                failures.append(call_args)
        if len(failures):
            raise AssertionError("missing expected calls : %s. Got %s" % (failures, self.call_args_list))

    def reset_mock(self):
        self._expected_calls = dict()
        super(Mockito, self).reset_mock()

    def __call__(self, *args, **kwargs):
        self.called = True
        self.call_count += 1
        self.call_args = callargs((args, kwargs))
        self.call_args_list.append(callargs((args, kwargs)))

        parent = self._parent
        name = self._name
        while parent is not None:
            parent.method_calls.append(callargs((name, args, kwargs)))
            if parent._parent is None:
                break
            name = parent._name + '.' + name
            parent = parent._parent

        if repr((args, kwargs)) in self._expected_calls:
            expector, call_args = self._expected_calls[repr((args, kwargs))]
            if expector._return_exception:
                raise expector._return_exception
            else:
                return expector._return_value

        ret_val = mock_DEFAULT
        if self.side_effect is not None:
            if (isinstance(self.side_effect, BaseException) or
                isinstance(self.side_effect, class_types) and
                issubclass(self.side_effect, BaseException)):
                raise self.side_effect

            ret_val = self.side_effect(*args, **kwargs)
            if ret_val is mock_DEFAULT:
                ret_val = self.return_value

        if self._wraps is not None and self._return_value is mock_DEFAULT:
            return self._wraps(*args, **kwargs)
        if ret_val is mock_DEFAULT:
            ret_val = self.return_value
        return ret_val


class Bf3TestCase(unittest.TestCase):
    """
    Test case that is suitable for testing BF3 parser specific features
    """

    @classmethod
    def setUpClass(cls):
        # less logging
        logging.getLogger('output').setLevel(logging.CRITICAL)

        from b3.parsers.frostbite2.abstractParser import AbstractParser
        from b3.fake import FakeConsole
        AbstractParser.__bases__ = (FakeConsole,)
        # Now parser inheritance hierarchy is :
        # Bf3Parser -> AbstractParser -> FakeConsole -> Parser

        # add method changes_team(newTeam, newSquad=None) to FakeClient
        def changes_team(self, newTeam, newSquad=None):
            self.console.OnPlayerTeamchange(data=[self.cid, newTeam, newSquad if newSquad else self.squad], action=None)
        FakeClient.changes_team = changes_team

    def setUp(self):
        # create a BF3 parser
        self.parser_conf = XmlConfigParser()
        self.parser_conf.loadFromString("""
                    <configuration>
                    </configuration>
                """)
        self.console = Bf3Parser(self.parser_conf)
        self.console.startup()


        # simulate game server actions
        def frostbitewrite(msg, maxRetries=1, needConfirmation=False):
            print "   >>> %s" % repr(msg)
            if msg[0] == 'admin.movePlayer':
                self.console.routeFrostbitePacket(['player.onTeamChange'] + list(msg[1:]))
            else:
                return mock_DEFAULT # will make Mockito fall back on return_value and wrapped function
        self.console.write = Mockito(wraps=self.console.write, side_effect=frostbitewrite)


        # load the admin plugin
        self.adminPlugin = AdminPlugin(self.console, '@b3/conf/plugin_admin.xml')
        self.adminPlugin.onStartup()

        # make sure the admin plugin obtained by other plugins is our admin plugin
        def getPlugin(name):
            if name == 'admin':
                return self.adminPlugin
            else:
                return self.console.getPlugin(name)
        self.console.getPlugin = getPlugin

        # prepare a few players
        self.joe = FakeClient(self.console, name="Joe", exactName="Joe", guid="zaerezarezar", groupBits=1, team=TEAM_UNKNOWN, teamId=0, squad=0)
        self.simon = FakeClient(self.console, name="Simon", exactName="Simon", guid="qsdfdsqfdsqf", groupBits=0, team=TEAM_UNKNOWN, teamId=0, squad=0)
        self.reg = FakeClient(self.console, name="Reg", exactName="Reg", guid="qsdfdsqfdsqf33", groupBits=4, team=TEAM_UNKNOWN, teamId=0, squad=0)
        self.moderator = FakeClient(self.console, name="Moderator", exactName="Moderator", guid="sdf455ezr", groupBits=8, team=TEAM_UNKNOWN, teamId=0, squad=0)
        self.admin = FakeClient(self.console, name="Level-40-Admin", exactName="Level-40-Admin", guid="875sasda", groupBits=16, team=TEAM_UNKNOWN, teamId=0, squad=0)
        self.superadmin = FakeClient(self.console, name="God", exactName="God", guid="f4qfer654r", groupBits=128, team=TEAM_UNKNOWN, teamId=0, squad=0)