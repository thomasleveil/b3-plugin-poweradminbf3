# -*- coding: utf-8 -*-
#
# PowerAdmin BF3 Plugin for BigBrotherBot(B3) (www.bigbrotherbot.net)
# Copyright (C) 2011 Thomas LÉVEIL (courgette@bigbrotherbot.net)
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# CHANGELOG
#
__version__ = '0.0'
__author__  = 'Courgette'

import b3
import b3.events
from b3.plugin import Plugin

class Poweradminbf3Plugin(Plugin):
    def __init__(self, console, config=None):
        Plugin.__init__(self. console. config)
        self._adminPlugin = None

    def _getCmd(self, cmd):
        cmd = 'cmd_%s' % cmd
        if hasattr(self, cmd):
            func = getattr(self, cmd)
            return func
        return None

    def _registerCommands(self):
        # register our commands
        if 'commands' in self.config.sections():
            for cmd in self.config.options('commands'):
                level = self.config.get('commands', cmd)
                sp = cmd.split('-')
                alias = None
                if len(sp) == 2:
                    cmd, alias = sp
                func = self._getCmd(cmd)
                if func:
                    self._adminPlugin.registerCommand(self, cmd, level, func, alias)

#
#    Parser interface implementation
#
    def onLoadConfig(self):
        """\
        This is called after loadConfig(). Any plugin private variables loaded
        from the config need to be reset here.
        """
        pass

    def startup(self):
        """\
        Initialize plugin settings
        """
        # get the admin plugin so we can register commands
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            # something is wrong, can't start without admin plugin
            self.error('Could not find admin plugin')
            return False
        self._registerCommands()

    def onEvent(self, event):
        """\
        Handle intercepted events
        """
        pass

#
#   Commands implementations
#

    def cmd_runnextround(self, data, client, cmd=None):
        """\
        Switch to next round, without ending current
        """
        raise NotImplementedError


    def cmd_restartround(self, data, client, cmd=None):
        """\
        Restart current round
        """
        raise NotImplementedError

    def cmd_kill(self, data, client, cmd=None):
        """\
        <player> Kill a player without scoring effects
        """
        raise NotImplementedError


    def cmd_changeteam(self, data, client, cmd=None):
        """\
        <name> - change a player to the other team
        """
        raise NotImplementedError


    def cmd_swap(self, data, client, cmd=None):
        """\
        <player A> [<player B>] - swap teams for player A and B if they are in different teams or squads
        """
        raise NotImplementedError


    def cmd_setnextmap(self, data, client=None, cmd=None):
        """\
        <mapname> - Set the nextmap (partial map name works)
        """
        raise NotImplementedError

    def cmd_setmode(self, data, client=None, cmd=None):
        """\
        <preset> - Change mode to given preset (normal, hardcore, infantry, ...)
        """
        raise NotImplementedError