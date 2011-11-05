# -*- encoding: utf-8 -*-

from b3.fake import fakeConsole, FakeConsole
from b3.fake import FakeClient, joe, simon, moderator, superadmin


def frostbitewrite(msg, maxRetries=1, needConfirmation=False):
    """send text to the console"""
    if type(msg) == str:
        # console abuse to broadcast text
        self.say(msg)
    elif type(msg) == tuple:
        print "   >>> %s" % repr(msg)


def authorizeClients():
    pass


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


def getPlayerScores(self=None, maxRetries=0):
    scores = {}
    for c in fakeConsole.clients.getList():
        scores[c.cid] = random.randint(-20, 200)
    print "getPlayerScores : %s" % repr(scores)
    return scores


def getClient(self, cid, _guid=None):
    return fakeConsole.clients.getByCID(cid)


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


def prepare_fakeparser_for_tests():
    fakeConsole.gameName = 'bf3'
    fakeConsole.write = frostbitewrite
    fakeConsole.authorizeClients = authorizeClients
    FakeConsole.getPlayerList = getPlayerList
    FakeConsole.getPlayerScores = getPlayerScores
    FakeConsole.getClient = getClient
    FakeClient.joinsTeam = joinsTeam