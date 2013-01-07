import sys
import threading

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest
import mock
import logging
from b3.update import B3version
from poweradminbf3 import MIN_BF3_PARSER_VERSION
from b3 import TEAM_UNKNOWN
from b3.config import XmlConfigParser
from b3.fake import FakeClient
from b3.parsers.bf3 import Bf3Parser, __version__ as bf3_version
from b3.plugins.admin import AdminPlugin


class Expector(object):
    def __init__(self):
        self._return_value = mock.Mock()
        self._return_exception = None

    def thenReturn(self, obj):
        self._return_value = obj

    def thenRaise(self, exception):
        self._return_exception = exception


class Mockito(mock.Mock):

    def __init__(self, *args, **kwargs):
        super(Mockito, self).__init__(*args, **kwargs)
        self._expected_calls = dict()


    def expect(self, *args, **kwargs):
        expector = Expector()
        self._expected_calls[repr(mock.call(args, kwargs))] = (expector, mock._Call((args, kwargs), two=True))
        return expector

    def verify_expected_calls(self):
        for expected_calls, call_args in self._expected_calls.values():
            if call_args not in self.call_args_list:
                raise AssertionError(
                    '%s call not found' % repr(call_args)
                )

    def reset_mock(self):
        self._expected_calls = dict()
        super(Mockito, self).reset_mock()

    def _mock_call(_mock_self, *args, **kwargs):
        self = _mock_self
        self.called = True
        self.call_count += 1
        self.call_args = mock._Call((args, kwargs), two=True)
        self.call_args_list.append(mock._Call((args, kwargs), two=True))

        _new_name = self._mock_new_name
        _new_parent = self._mock_new_parent
        self.mock_calls.append(mock._Call(('', args, kwargs)))

        seen = set()
        skip_next_dot = _new_name == '()'
        do_method_calls = self._mock_parent is not None
        name = self._mock_name
        while _new_parent is not None:
            this_mock_call = mock._Call((_new_name, args, kwargs))
            if _new_parent._mock_new_name:
                dot = '.'
                if skip_next_dot:
                    dot = ''

                skip_next_dot = False
                if _new_parent._mock_new_name == '()':
                    skip_next_dot = True

                _new_name = _new_parent._mock_new_name + dot + _new_name

            if do_method_calls:
                if _new_name == name:
                    this_method_call = this_mock_call
                else:
                    this_method_call = mock._Call(name, args, kwargs)
                _new_parent.method_calls.append(this_method_call)

                do_method_calls = _new_parent._mock_parent is not None
                if do_method_calls:
                    name = _new_parent._mock_name + '.' + name

            _new_parent.mock_calls.append(this_mock_call)
            _new_parent = _new_parent._mock_new_parent

            # use ids here so as not to call __hash__ on the mocks
            _new_parent_id = id(_new_parent)
            if _new_parent_id in seen:
                break
            seen.add(_new_parent_id)


        if repr(mock.call(args, kwargs)) in self._expected_calls:
            expector, call_args = self._expected_calls[repr(mock.call(args, kwargs))]
            if expector._return_exception:
                raise expector._return_exception
            else:
                return expector._return_value

        ret_val = mock.DEFAULT
        effect = self.side_effect
        if effect is not None:
            if mock._is_exception(effect):
                raise effect

            if not mock._callable(effect):
                return next(effect)

            ret_val = effect(*args, **kwargs)
            if ret_val is mock.DEFAULT:
                ret_val = self.return_value

        if (self._mock_wraps is not None and
            self._mock_return_value is mock.DEFAULT):
            return self._mock_wraps(*args, **kwargs)
        if ret_val is mock.DEFAULT:
            ret_val = self.return_value
        return ret_val


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
        self.parser_conf.loadFromString("""<configuration />""")
        self.console = Bf3Parser(self.parser_conf)

        # alter a few settings to speed up the tests
        self.console.sayqueue_get_timeout = 0
        self.console._settings['message_delay'] = 0

        self.console.startup()


        # simulate game server actions
        def frostbitewrite(msg, maxRetries=1, needConfirmation=False):
            print "   >>> %s" % repr(msg)
            if msg[0] == 'admin.movePlayer':
                self.console.routeFrostbitePacket(['player.onTeamChange'] + list(msg[1:]))
            else:
                return mock.DEFAULT # will make Mockito fall back on return_value and wrapped function
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

        self.console.patch_b3_admin_plugin()

        # prepare a few players
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
