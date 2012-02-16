Power Admin Battlefield 3 for Big Brother Bot (www.bigbrotherbot.net)
=====================================================================


Description
-----------

This plugin brings Battlefield 3 specific features to Bigbrotherbot.



Installation
------------

 * copy poweradminbf3.py into b3/extplugins
 * add to the plugins section of your main b3 config file :
      <plugin name="poweradminbf3" config="@b3/extplugins/conf/plugin_poweradminbf3.xml" />


Commands
--------

!roundnext - Switch to next round, without ending current
!roundrestart - Restart current round
!kill <player> [reason] - Kill a player without scoring effects
!changeteam <player> - move <player> to the other team
!swap <player A> [<player B>] - swap player A's team/squad with player B's team/squad
!setnextmap <map partial name> - select the next map to load after current round
!punkbuster <punkbuster command> - run a punkbuster command
!loadconfig <config file> - load a config file to change server vars, map list, game modes
!listconfig - list available config files
!scramble - (un)request scrambler to scramble teams at next round
!scramblemode <random/score> - set the scrambling strategy
!autoscramble <off/round/map> - set the auto-scrambling mode
!unlockmode <all|common|stats|none> - set the weapons unlocks
!vehicles <on|off> - (en|dis)able vehicles spawn
!autobalance <off|on> - (de)activate the autobalancer
!autoassign <off|on> - (de)activate the autoassigner which puts connecting player into the right team
!endround <winning team id> - end current round and set winning team
!idle <off|on|min> - set the idle kicker off/on or to the number of minute you wish
!serverreboot - restart the BF3 gameserver

Other features
--------------

 ## CONFIG MANAGER ##
    Configmanager can automatically load server config scripts at each map change based on current 
    gamemode and/or map. It will first look if a b3_<gametype>_<mapname>.cfg exists 
    (example: b3_teamdeathmatch0_mp001.cfg) and execute it. If it doesn't exist, it checks for 
    b3_<gametype>.cfg (example: b3_rushlarge0.cfg). 

    If none of them exist, it will look for b3_main.cfg. This file makes it possible to reset certain 
    vars, so always create a b3_main.cfg if you want to enable and use this feature.

    ** Example Scenario **
    You are running a server with mixed gametypes of Conquest and Rush and you want to play Rush maps
    without vehicles. What you need to do is to create a file called "b3_rushlarge0.cfg" inside your
    configmanager folder with required settings. "vars.vehicleSpawnAllowed false" in this case. Also
    make sure you add "vars.vehicleSpawnAllowed True" in your b3_main.cfg so that when a conquest map
    comes in rotation vehicles are enabled again.

    Please take note that config manager plugin supports only instantaneous server vars.


Support
-------

Support is only provided on www.bigbrotherbot.net forums on the following topic :
http://forum.bigbrotherbot.net/bf3b3-beta-board/poweradmin-bf3/
