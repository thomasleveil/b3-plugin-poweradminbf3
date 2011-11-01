# -*- encoding: utf-8 -*-

from b3.fake import fakeConsole, FakeConsole
from b3.fake import FakeClient, joe, simon, moderator, superadmin
fakeConsole.gameName = 'bf3'

def frostbitewrite(msg, maxRetries=1, needConfirmation=False):
    """send text to the console"""
    if type(msg) == str:
        # console abuse to broadcast text
        self.say(msg)
    elif type(msg) == tuple:
        print "   >>> %s" % repr(msg)
fakeConsole.write = frostbitewrite


def authorizeClients():
    pass
fakeConsole.authorizeClients = authorizeClients


def getPlayerList(self=None, maxRetries=0):
    players = {}
    for c in fakeConsole.clients.getList():
        players[c.cid] = {
            'cid' : c.cid,
            'name' : c.name,
            'teamId': c.teamId
            }
    #print "getPlayerList : %s" % repr(players)
    return players
FakeConsole.getPlayerList = getPlayerList


def getPlayerScores(self=None, maxRetries=0):
    scores = {}
    for c in fakeConsole.clients.getList():
        scores[c.cid] = random.randint(-20, 200)
    print "getPlayerScores : %s" % repr(scores)
    return scores
FakeConsole.getPlayerScores = getPlayerScores


def getClient(self, cid, _guid=None):
    return fakeConsole.clients.getByCID(cid)
FakeConsole.getClient = getClient


def getTeam(team):
    """convert BFBC2 team numbers to B3 team numbers"""
    team = int(team)
    if team == 1:
        return b3.TEAM_RED
    elif team == 2:
        return b3.TEAM_BLUE
    elif team == 3:
        return b3.TEAM_SPEC
    else:
        return b3.TEAM_UNKNOWN


def joinsTeam(self, teamId):
    print "\n%s goes to team %s" % (self.name, teamId)
    self.teamId = teamId
    self.team = getTeam(teamId) # .team setter will send team change event
    self.console.queueEvent(self.console.getEvent("EVT_CLIENT_TEAM_CHANGE", teamId, self))
FakeClient.joinsTeam = joinsTeam

def printTeams():
    team1players = []
    team2players = []
    for client in fakeConsole.clients.getList():
        if str(client.teamId) == '1':
            team1players.append(client)
        elif str(client.teamId) == '2':
            team2players.append(client)
    print("+" + ("-"*32) + "+" + ("-"*32) + "+")
    while len(team1players) + len(team2players) > 0:
        try:
            p1 = team1players.pop()
            p1name = p1.name
            c = p1.var(p, 'teamtime', fakeConsole.time())
            p1teamtime = "(%s)" % c.value
        except IndexError:
            p1name = ''
            p1teamtime = ''
        try:
            p2 = team2players.pop()
            p2name = p2.name
            c = p2.var(p, 'teamtime', fakeConsole.time())
            p2teamtime = "(%s)" % c.value
        except IndexError:
            p2name = ''
            p2teamtime = ''
        print("| {:>18}{:12} | {:>18}{:12} |".format(p1name, p1teamtime, p2name, p2teamtime))
    print("+" + ("-"*32) + "+" + ("-"*32) + "+")


############################################################################################

from poweradminbf3 import Poweradminbf3Plugin
from b3.config import XmlConfigParser

def test_1():
    conf = XmlConfigParser()
    conf.loadFromString("""
    <configuration plugin="poweradminbf3">
      <settings name="commands">
        <set name="punkbuster-pb">100</set>
        <set name="setmode-mode">60</set>

        <set name="roundnext-rnext">40</set>
        <set name="roundrestart-rrestart">40</set>
        <set name="kill">40</set>

        <set name="changeteam">20</set>
        <set name="swap">20</set>
        <set name="setnextmap-snmap">20</set>
      </settings>
    </configuration>
    """)

    p = Poweradminbf3Plugin(fakeConsole, conf)
    p.onLoadConfig()
    p.onStartup()

    simon.connects("simon")
    simon.teamId = 1
    simon.squad = 7
    joe.connects('Joe')
    joe.teamId = 1
    joe.squad = 7
    superadmin.connects('superadmin')
    superadmin.teamId = 2
    superadmin.squad = 6
    moderator.connects('moderator')
    moderator.teamId = 2
    moderator.squad = 5
    print "Joe's group is " +  joe.maxGroup.name
    print "Simon's group is " + simon.maxGroup.name
    print "Moderator's group is " + moderator.maxGroup.name
    print "superadmin's group is " +  superadmin.maxGroup.name

    print "#"*80 ###################################### test basic commands
    superadmin.says("!roundnext")
    superadmin.says("!roundrestart")
    superadmin.says("!punkbuster")
    superadmin.says("!punkbuster some command")


    print "#"*80 ###################################### test !kill
    superadmin.says("!changeteam joe")
    p._adminPlugin._commands["changeteam"].level = 0,100
    joe.says("!changeteam god")
    joe.says("!changeteam simon")

    print "#"*80 ###################################### test !kill
    superadmin.says("!kill joe")
    p._adminPlugin._commands["kill"].level = 0,100
    joe.says("!kill god")
    joe.says("!kill simon")


    print "#"*80 ###################################### test !swap
    superadmin.teamId = 2
    superadmin.squad = 6
    print "superadmin.teamId: %s, squad: %s" % (superadmin.teamId, superadmin.squad)
    joe.teamId = 1
    joe.squad = 7
    print "joe.teamId: %s, squad: %s" % (joe.teamId, joe.squad)
    superadmin.says('!swap joe')

    simon.teamId = 1
    simon.squad = 6
    joe.teamId = 1
    joe.squad = 6
    superadmin.says("!swap joe simon")

    joe.squad = 2
    superadmin.says("!swap joe simon")

    # test groups
    p._adminPlugin._commands["swap"].level = 0,100
    simon.says("!swap moderator")
    moderator.says("!swap simon god")


    print "#"*80 ###################################### test !setnextmap
    superadmin.says('!snmap')
    import mock

def test_bug_getmessage():
    conf = XmlConfigParser()
    conf.loadFromString("""
<configuration plugin="poweradminbf3">
  <settings name="commands">
    <set name="setmode-mode">60</set>

    <set name="roundnext-rnext">40</set>
    <set name="roundrestart-rrestart">40</set>
    <set name="kill">40</set>

    <set name="changeteam">20</set>
    <set name="swap">20</set>
    <set name="setnextmap-snmap">20</set>
  </settings>
  <settings name="messages">
    <set name="operation_denied">Operation denied</set>
    <set name="operation_denied_level">Operation denied because %(name)s is in the %(group)s group</set>
  </settings>
</configuration>
    """)

    p = Poweradminbf3Plugin(fakeConsole, conf)
    p.onLoadConfig()
    p.onStartup()

test_bug_getmessage()