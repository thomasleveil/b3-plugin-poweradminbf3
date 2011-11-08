# -*- encoding: utf-8 -*-
from test import prepare_fakeparser_for_tests
import time
import b3
from b3.parsers.frostbite2.util import PlayerInfoBlock

prepare_fakeparser_for_tests()

from b3.fake import fakeConsole, joe, simon, superadmin, FakeClient
from poweradminbf3 import Poweradminbf3Plugin
from b3.config import XmlConfigParser


conf = XmlConfigParser()
conf.loadFromString("""
    <configuration plugin="poweradminbf3">

      <settings name="commands">
        <set name="scramble">20</set>
        <set name="scramblemode">20</set>
        <set name="autoscramble">20</set>
      </settings>

      <settings name="scrambler">
        <set name="mode">off</set>
        <set name="strategy">random</set>
      </settings>

    </configuration>
""")

p = Poweradminbf3Plugin(fakeConsole, conf)
p.onLoadConfig()
p.onStartup()

def generate_scores():
    scores = fakeConsole.getPlayerScores()
    score_list = ['2','name','score', len(scores)]
    for k, v in scores.items():
        score_list.append(k)
        score_list.append(v)
        client = fakeConsole.getClient(k)
        if client:
            client.score = v
    p._scrambler._last_round_scores = PlayerInfoBlock(score_list)

def printTeams():
    team1players = []
    team2players = []
    for client in fakeConsole.clients.getList():
        if str(client.teamId) == '1':
            team1players.append(client)
        elif str(client.teamId) == '2':
            team2players.append(client)
    print("+" + ("-"*22) + "+" + ("-"*22) + "+")
    while len(team1players) + len(team2players) > 0:
        try:
            p1 = team1players.pop()
            p1name = p1.name
            p1score = getattr(p1, 'score', 0)
        except IndexError:
            p1name = ''
            p1score = ''
        try:
            p2 = team2players.pop()
            p2name = p2.name
            p2score = getattr(p2, 'score', 0)
        except IndexError:
            p2name = ''
            p2score = ''
        print("| {: >4} {:>15} | {:<15} {: >4} |".format(p1score, p1name, p2name, p2score))
    print("+" + ("-"*22) + "+" + ("-"*22) + "+")


superadmin.connects('superadmin')
superadmin.teamId = 2


print "\n\n####################################### test !scramble"
superadmin.says('!scramble')
assert p._scrambling_planned is True
superadmin.says('!scramble')
assert p._scrambling_planned is False
superadmin.says('!scramble')
assert p._scrambling_planned is True


print "\n\n####################################### test scrambleTeams()"
for i in range(12):
    fakeConsole.clients.newClient(cid='p%s'%i, guid='p%s'%i, name="Player %s"%i, teamId=1)
printTeams()
p._scrambler.scrambleTeams()
printTeams()
p._scrambler.scrambleTeams()
printTeams()


print "\n\n####################################### test !scramblemode"
superadmin.says('!scramblemode')
superadmin.says('!scramblemode random')
superadmin.says('!scramblemode score')

print "\n\n####################################### test scrambling by score"
generate_scores()
superadmin.says('!scramblemode score')
printTeams()
p._scrambler.scrambleTeams()
printTeams()

print "\n\n####################################### test scrambling at next round change"
print "\n\t------------ Should scramble after second event ---------------"
generate_scores()
fakeConsole.queueEvent(b3.events.Event(b3.events.EVT_GAME_ROUND_START, 2, None))
printTeams()
print "\n\t------------ Should not scramble after second event ---------------"
fakeConsole.queueEvent(b3.events.Event(b3.events.EVT_GAME_ROUND_START, 2, None))
