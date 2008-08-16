import annchienta
import PartyManager, SceneManager

mapManager = annchienta.getMapManager()
videoManager = annchienta.getVideoManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

currentMap = partyManager.currentMap

august = partyManager.player
march = currentMap.getObject( "march" )
avril = currentMap.getObject( "avril" )

sceneManager.initDialog( [august, march, avril] )

if not partyManager.hasRecord( "inaran_intro" ):

    imiryn = annchienta.Surface("images/storyline/imiryn.png")
    videoManager.begin()
    videoManager.drawSurface( imiryn, 0, 0 )
    videoManager.end()

    sceneManager.text( "Our story unfolds in a place where magic was commonplace and airships plied the skies, crowding out the heavens... the Imiryn Empire.", None )
    sceneManager.text( "The Empire was built on technology and magic. Then, the Laustwan were discovered.", None )
    sceneManager.text( "The Laustwan were a tribe of apparently human-like creatures, who offered their services to men.", None )
    sceneManager.text( "With their help, the Empire was able to expand their territories, and people and Laustwan were able to live very comfortable lives.", None )
    sceneManager.text( "Now, the Empire of Imiryn was at the height of it's power. It controlled the entire Jemor continent, and had many colonies on the northern side of the Nupol continent.", None )
    sceneManager.text( "This Empire was protected by a very fine and well-trained army. The elite section of this army was called the Fifth Guard.", None )
    sceneManager.text( "Our story handles about three aspiring young warriors, hoping to join this Fifth Guard.", None )

    sceneManager.speak( march, "It must be here." )
    sceneManager.speak( avril, "Are you sure?" )
    sceneManager.speak( march, "... Yes. Come over here, August." )
    sceneManager.text( "Hold down the left mouse button to move. Then click March when you are close enough." )
    partyManager.addRecord( "inaran_intro" )



sceneManager.quitDialog()

partyManager.refreshMap()

