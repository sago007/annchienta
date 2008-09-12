import annchienta
import PartyManager, SceneManager, BattleManager

mapManager = annchienta.getMapManager()
videoManager = annchienta.getVideoManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()
battleManager = BattleManager.getBattleManager()

currentMap = partyManager.currentMap

august = partyManager.player

# Addobject and stuff...
march = annchienta.Person( "march", "locations/common/march.xml" )
avril = annchienta.Person( "avril", "locations/common/avril.xml" )
enthavos = annchienta.Person( "enthavos", "locations/unknown/enthavos.xml" )

position = annchienta.Point( annchienta.TilePoint, 17, 20 )
august.setPosition( position )
march.setPosition( annchienta.Point( annchienta.TilePoint, position.x+1, position.y ) )
avril.setPosition( annchienta.Point( annchienta.TilePoint, position.x+2, position.y ) )
enthavos.setPosition( annchienta.Point( annchienta.TilePoint, position.x+1, position.y-3 ) )
currentMap.addObject( march )
currentMap.addObject( avril )
currentMap.addObject( enthavos )
sceneManager.initDialog( [august, march, avril, enthavos] )

sceneManager.move( [august, march, avril, enthavos ], [ annchienta.Point( annchienta.TilePoint, 17, 6 ), 
                                                        annchienta.Point( annchienta.TilePoint, 17, 7 ), 
                                                        annchienta.Point( annchienta.TilePoint, 17, 8 ), 
                                                        annchienta.Point( annchienta.TilePoint, 19, 7 ) ] )

august.lookAt( enthavos )
march.lookAt( enthavos )
avril.lookAt( enthavos )
enthavos.lookAt( august )

sceneManager.speak( enthavos, "We are on the Nupol continent." )
sceneManager.speak( avril, "We figured that much! Are you Enthavos? What are you doing here? And what do you want from us?!" )
sceneManager.speak( enthavos, "Mostly, I want it all to go away..." )
sceneManager.speak( enthavos, "But now the time has come for a little test. Engage!" )

#won = battleManager.runBattle( ["enthavos"], annchienta.Surface("images/backgrounds/ice.png"), False )
won = True

if won:
    sceneManager.speak( enthavos, "Good... very good. This will be sufficient." )
    sceneManager.speak( march, "What the heck are you talking about?!" )
    sceneManager.speak( enthavos, "..." )
    enthavos.setAnimation( "reveal" )
    sceneManager.speak( august, "Brother?!" )
    sceneManager.speak( enthavos, "I'm sorry." )
    sceneManager.speak( enthavos, "I am indeed August's older brother, Kyzano." )
    enthavos.setName( "kyzano" )
    sceneManager.speak( avril, "What?!" )
    sceneManager.speak( march, "Weren't you... dead?" )
    sceneManager.speak( enthavos, "That's a long story..." )
    sceneManager.speak( august, "Well, I won't go before I know the truth." )
    sceneManager.speak( enthavos, "I know I owe you guys an explation." )
    sceneManager.speak( august, "We're waiting." )
    sceneManager.speak( enthavos, "As you might know... I fought the real Enthavos three years ago." )
    sceneManager.speak( enthavos, "I killed him, but was severly wounded." )
    sceneManager.speak( enthavos, "I don't remember that phase really well, but when I woke up, I was on the Nupol continent." )
    sceneManager.speak( enthavos, "Well... I wrote this letter for you guys, when I saw you on the beach." )
    sceneManager.speak( enthavos, "The time has come for me to go." )
    sceneManager.speak( enthavos, "You are almost out of the mountains. When you are, you will see something... unusual." )
    sceneManager.speak( enthavos, "Once there, read this letter. All will become clear." )
    sceneManager.speak( enthavos, "I'm sorry, but I can't help you any more. I am risking my life already." )
    sceneManager.speak( enthavos, "I wish you a safe journey, but I fear it will be more of the contrary. Goodbye... brother."  )
    sceneManager.speak( august, "Goodbye..." )

    partyManager.addRecord("mountains_second_enthavos_encounter")

sceneManager.quitDialog()
currentMap.removeObject( march )
currentMap.removeObject( avril )
currentMap.removeObject( enthavos )

partyManager.refreshMap()

