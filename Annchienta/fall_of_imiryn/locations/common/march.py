# This script is executd in the intro scene, when
# our party is outside of the cave.
import annchienta
import PartyManager, SceneManager

mapManager = annchienta.getMapManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

august = annchienta.getActiveObject()
march = partyManager.getCurrentMap().getPerson( "march" )
avril = partyManager.getCurrentMap().getPerson( "avril" )
laustwan = partyManager.getCurrentMap().getPerson( "laustwan" )
    
sceneManager.initDialog( [march, august, avril, laustwan] )

if not partyManager.hasRecord("inaran_talked_to_march"):

    august.lookAt( march )
    sceneManager.speak( march, "Can you see that cave over there? That must be it." )

    sceneManager.speak( august, "I guess... finally..." )

    sceneManager.speak( august, "We had been searching these Inaran areas for three weeks.", True )
    sceneManager.speak( august, "We were young and full of hope. We would join the Fifth Guard, the elite section of our army.", True )
    sceneManager.speak( august, "Being in that section had been my dream since my older brother died protecting it.", True )

    lp = laustwan.getPosition().to( annchienta.IsometricPoint )
    lp.x += 60
    sceneManager.move( laustwan, lp )
    sceneManager.speak( laustwan, "Puko!" )

    sceneManager.speak( august, "Can we leave the Laustwan here?" )
    sceneManager.speak( march, "Sure. He will find it's way to another master, they always do." )
    sceneManager.speak( laustwan, "Gri-huk." )

    sceneManager.speak( avril, "Well, you've been really helpful... I'm glad we had you with us. You are free now." )

    sceneManager.speak( laustwan, "Hog-hu." )

    lp.x = 0
    sceneManager.move( laustwan, lp )

    sceneManager.speak( august, "I never really understood these helpful human-like creatures.", True )
    sceneManager.speak( august, "Still, I was grateful to them that they were there, always helping humans out.", True )
    sceneManager.speak( august, "Getting here would have been a lot harder without him carrying most of our equipment.", True )
    sceneManager.speak( march, "One final test. The cave is here. Let's go." )

    avril.lookAt( august )
    sceneManager.speak( avril, "Wait, you know I prefer fighting from the back row, right? That way, I only receive half of the damage done." )
    march.lookAt( avril )
    sceneManager.speak( march, "Yeah, but you can only deal half damage, too!" )
    avril.lookAt( march )
    sceneManager.speak( avril, "Not if you use magic." )

    ap = august.getPosition()
    sceneManager.move( [avril, march], [ap,ap] )

    sceneManager.text( "Use the right mouse button to bring up the party menu. Use the left mouse button to navigate in any menu." )
    sceneManager.text( "When you are in a menu, you can also use the right mouse button to cancel the menu." )

    partyManager.addRecord("inaran_talked_to_march")
    partyManager.refreshMap()

sceneManager.quitDialog()

