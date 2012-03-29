# -*- encoding: utf-8 -*-

def prepare_fakeparser_for_tests():
    import random
    from b3 import TEAM_BLUE, TEAM_RED, TEAM_SPEC, TEAM_UNKNOWN
    from b3.fake import fakeConsole, FakeConsole
    from b3.fake import FakeClient


    def frostbitewrite(self, msg, maxRetries=1, needConfirmation=False):
        """send text to the console"""
        if type(msg) == str:
            # console abuse to broadcast text
            self.say(msg)
        elif type(msg) == tuple:
            print "   >>> %s" % repr(msg)
            if len(msg) >= 4 and msg[0] == 'admin.movePlayer':
                client = getClient(self, msg[1])
                if client:
                    client.teamId = int(msg[2])
                    client.squad = int(msg[3])




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
        """convert Frostbite team numbers to B3 team numbers"""
        team = int(team)
        if team == 1:
            return TEAM_RED
        elif team == 2:
            return TEAM_BLUE
        elif team == 3:
            return TEAM_SPEC
        else:
            return TEAM_UNKNOWN


    def joinsTeam(self, teamId):
        print "\n%s goes to team %s" % (self.name, teamId)
        self.teamId = teamId
        self.team = getTeam(teamId) # .team setter will send team change event
        self.console.queueEvent(self.console.getEvent("EVT_CLIENT_TEAM_CHANGE", teamId, self))


    fakeConsole.gameName = 'bf3'
    fakeConsole.authorizeClients = authorizeClients
    FakeConsole.write = frostbitewrite
    FakeConsole.getPlayerList = getPlayerList
    FakeConsole.getPlayerScores = getPlayerScores
    FakeConsole.getClient = getClient
    FakeClient.joinsTeam = joinsTeam
    fakeConsole.Events.createEvent('EVT_GAME_ROUND_PLAYER_SCORES', 'round player scores')
    fakeConsole.Events.createEvent('EVT_GAME_ROUND_TEAM_SCORES', 'round team scores')

