import annchienta
import PartyManager, SceneManager

mapManager = annchienta.getMapManager()
videoManager = annchienta.getVideoManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

currentMap = partyManager.currentMap

august = partyManager.player
march = currentMap.getPerson( "march" )
avril = currentMap.getPerson( "avril" )
laustwan = currentMap.getPerson( "laustwan" )

sceneManager.initDialog( [august, march, avril, laustwan] )

if not partyManager.hasRecord( "inaran_intro" ):

    imiryn = annchienta.Surface("images/storyline/imiryn.png")
    videoManager.clear()
    videoManager.drawSurface( imiryn, 0, 0 )
    videoManager.flip()
    videoManager.flip()

    sceneManager.text( "Our story unfolds in a place where magic was commonplace and airships plied the skies, crowding out the heavens... the Imiryn Empire.", None )
    sceneManager.text( "The Empire was built on technology and magic. Overly superior to the other civilizations, it quickly conquered the entire Jemor continent.", None )
    sceneManager.text( "But it didn't stop there. Expeditions were send to other islands.", None )
    sceneManager.text( "To the south of the Jemor continent, the Nupol continent was discovered.", None )
    
    continents = annchienta.Surface("images/storyline/continents.png")
    videoManager.clear()
    videoManager.drawSurface( continents, 0, 0 )
    videoManager.flip()
    videoManager.flip()

    sceneManager.waitForClick()

    sceneManager.text( "The Nupol continent was more dangerous then the Empire had expected. It took time before the first colonists settled on the northern side of it.", None )
    sceneManager.text( "At that time, the Laustwan were discovered in the Nupol continent.", None )
    sceneManager.text( "The Laustwan were a tribe of apparently human-like creatures, who offered their services to men.", None )
    sceneManager.text( "Communication with them turned out to be hard, as they were only capable of making strange cries, and they didn't seem to understand any language.", None )
    sceneManager.text( "But they were very helpful, always obeying mankind.", None )

    videoManager.clear()
    videoManager.drawSurface( imiryn, 0, 0 )
    videoManager.flip()
    videoManager.flip()

    sceneManager.text( "With their help, the Empire was able to expand their territories, and people and Laustwan were able to live very comfortable lives.", None )
    sceneManager.text( "But as they Empire grew more prosperous, pirate attacks became more and more frequent. To protect itself, the Empire created an army.", None )
    sceneManager.text( "The elite section of this army was called the Fifth Guard.", None )
    sceneManager.text( "Our story handles about three aspiring young warriors, hoping to join this Fifth Guard.", None )

    sceneManager.fade( 255, 255, 255 )
    sceneManager.speak( march, "It must be here." )

    march.setAnimation( "standwest" )

    sceneManager.speak( august, "March is a strange guy... wandering the world with only one arm. He doesn't want to tell us when he lost the other one.", True )
    sceneManager.speak( august, "In fact... he doesn't say a lot at all. But when he says something... it's usually correct.", True )
    sceneManager.speak( avril, "Are you sure?" )
    sceneManager.speak( march, "... Yes. Come over here, August." )
    sceneManager.text( "Hold down the left mouse button to move. Then click March when you are close enough." )
    sceneManager.text( "During the game, press the right mouse button to bring up the menu." )
    sceneManager.text( "In all menu's, use the left mouse button to click your choice. Click using the right mouse button to back to a higher-level menu." )
    partyManager.addRecord( "inaran_intro" )

sceneManager.quitDialog()

partyManager.refreshMap()

