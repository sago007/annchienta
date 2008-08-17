import annchienta
import PartyManager, SceneManager, Battle

mapManager = annchienta.getMapManager()
engine = annchienta.getEngine()
videoManager = annchienta.getVideoManager()
audioManager = annchienta.getAudioManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

currentMap = partyManager.currentMap

august = partyManager.player

sceneManager.initDialog( [august] )

sceneManager.text("Ultros:\nYaaaouch! Seafood soup!")
#won = Battle.runBattle( ["ultros"], annchienta.Surface("images/backgrounds/cave.png"), False )
won = True

if won:
    sound = annchienta.Sound( "sounds/collapse.ogg" )
    audioManager.playSound( sound )

    sceneManager.speak( august, "The cave is collapsing!" )
    sceneManager.text( "March:\nGet on this raft. Now." )
    sceneManager.text( "Use the mouse cursor to steer the raft." )
    execfile("locations/inaran/raft.py")

mapManager.resync()

sceneManager.quitDialog()

partyManager.refreshMap()

