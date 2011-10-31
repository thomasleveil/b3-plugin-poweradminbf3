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
# 0.1 - add command !kill
# 0.2 - add commands !roundrestart and !roundnext
import time
from b3.parsers.frostbite2.protocol import CommandFailedError

__version__ = '0.2'
__author__  = 'Courgette'

import b3
import b3.events
from b3.plugin import Plugin

class Poweradminbf3Plugin(Plugin):
    def __init__(self, console, config=None):
        Plugin.__init__(self, console, config)
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


################################################################################################################
#
#    Parser interface implementation
#
################################################################################################################

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

################################################################################################################
#
#   Commands implementations
#
################################################################################################################

    def cmd_roundnext(self, data, client, cmd=None):
        """\
        Switch to next round, without ending current
        """
        self.console.say('forcing next round')
        time.sleep(1)
        try:
            self.console.write(('mapList.runNextRound',))
        except CommandFailedError, err:
            client.message('Error: %s' % err.message)


    def cmd_roundrestart(self, data, client, cmd=None):
        """\
        Restart current round
        """
        self.console.say('Restart current round')
        time.sleep(1)
        try:
            self.console.write(('mapList.restartRound',))
        except CommandFailedError, err:
            client.message('Error: %s' % err.message)

    def cmd_kill(self, data, client, cmd=None):
        """\
        <player> [reason] - Kill a player without scoring effects
        """
        # this will split the player name and the message
        name, reason = self._adminPlugin.parseUserCmd(data)
        if name:
            sclient = self._adminPlugin.findClientPrompt(name, client)
            if not sclient:
                # a player matching the name was not found, a list of closest matches will be displayed
                # we can exit here and the user will retry with a more specific player
                return
            else:
                try:
                    self.console.write(('admin.killPlayer', sclient.cid))
                    if reason:
                        sclient.message("Kill reason: %s" % reason)
                    else:
                        sclient.message("Killed by admin")
                except CommandFailedError, err:
                    if err.message[0] == "SoldierNotAlive":
                        client.message("%s is already dead" % sclient.name)
                    else:
                        client.message('Error: %s' % err.message)

    def cmd_changeteam(self, data, client, cmd=None):
        """\
        <name> - change a player to the other team
        """
        name, reason = self._adminPlugin.parseUserCmd(data)
        if not name:
            client.message('Invalid data, try !help changeteam')
        else:
            sclient = self._adminPlugin.findClientPrompt(name, client)
            if sclient:
                newteam = '2' if sclient.teamId == 1 else '1'
                try:
                    self.console.write(('admin.movePlayer', sclient.cid, newteam, 0, 'true'))
                    cmd.sayLoudOrPM(client, '%s forced from team %s to team %s' % (sclient.cid, sclient.teamId, newteam))
                except CommandFailedError, err:
                    client.message('Error, server replied %s' % err)


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