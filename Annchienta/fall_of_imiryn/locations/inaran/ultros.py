import annchienta
import PartyManager, SceneManager, BattleManager

mapManager = annchienta.getMapManager()
engine = annchienta.getEngine()
videoManager = annchienta.getVideoManager()
audioManager = annchienta.getAudioManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()
battleManager = BattleManager.getBattleManager()

currentMap = partyManager.getCurrentMap()

august = partyManager.getPlayer()

sceneManager.initDialog( [august] )

sceneManager.text("March:\nLook out!")
sceneManager.text("Ultros:\nYaaaouch! Seafood soup!")
won = battleManager.runBattle( ["ultros"], annchienta.Surface("images/backgrounds/cave.png"), False )
#won = True

if won:
    sound = annchienta.Sound( "sounds/collapse.ogg" )
    audioManager.playSound( sound )

    sceneManager.speak( august, "The cave is collapsing!" )
    sceneManager.text( "March:\nGet on this raft. Now." )
    sceneManager.text( "Use the mouse cursor to steer the raft. You will reach the cave exit in approximately one minute." )
    execfile("locations/inaran/raft.py")
    if mapManager.isRunning():

        # Make everything black
        sceneManager.fade()
        sceneManager.text("August:\nBy the time we regained some control over the raft, it had long left the cave.", None, True )
        videoManager.clear()
        surface = annchienta.Surface("images/storyline/sea_at_night.png")
        videoManager.drawSurface( surface, 0, 0 )
        videoManager.flip()
        videoManager.flip()
        sceneManager.text("August:\nThe current had taken us away from our beloved homeland.", None, True )
        sceneManager.text("August:\nThe moments where we could still see our Jemor continent in the distance... were gone.", None, True )
        sceneManager.text("August:\nThere was nothing but sea.", None, True )
        sceneManager.text("August:\nI have no idea how long we had been drifting. It felt like days. Perhaps it even were days.", None, True )  
        sceneManager.text("August:\nWe all thought about a lot of things. We thought we were going to die.", None, True )
        sceneManager.text("August:\nMy brother had been killed by Enthavos in the Fifth Guard, and my mother had recently passed away. And my father... I had never known him.", None, True )
        sceneManager.text("August:\nI don't think I was really afraid of dying. Avril started talking about her sister.", None, True )
        sceneManager.text("August:\nHow she missed her... How cruel it is she hadn't been able to say goodbye.", None, True )
        sceneManager.text("August:\nAt some point Avril said being in the Fifth Guard had really lost his meaning somehow.", None, True )
        sceneManager.text("August:\nWe were all getting very pessimistic.", None, True )
        sceneManager.text("August:\nThat must've been the point when we hit land.", None, True )
        sceneManager.text("August:\nWhere were we?", None, True )

        partyManager.changeMap( "locations/unknown/beach_start.xml", annchienta.Point( annchienta.TilePoint, 15, 15 ), 0, False )
        battleManager.delayNextBattle()

mapManager.resync()

sceneManager.quitDialog()

