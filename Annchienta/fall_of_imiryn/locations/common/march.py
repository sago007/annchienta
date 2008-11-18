# This script is executd in the intro scene, when
# our party is outside of the cave.
import annchienta
import PartyManager, SceneManager

mapManager = annchienta.getMapManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

march = annchienta.getPassiveObject()
august = annchienta.getActiveObject()
avril = partyManager.currentMap.getPerson( "avril" )
laustwan = partyManager.currentMap.getPerson( "laustwan" )
    
sceneManager.initDialog( [march, august, avril, laustwan] )

if not partyManager.hasRecord("inaran_intro_march"):

    sceneManager.speak( march, "Can you see that cave over there? That must be it." )

    sceneManager.speak( august, "I guess... finally..." )

    sceneManager.speak( august, "We had been searching these Inaran areas, the very south of the Jemor continent, for a week.", True )
    sceneManager.speak( august, "It was supposed to be our last test before we could join the Fifth Guard.", True )
    sceneManager.speak( august, "We were young and full of hope. We would join the Fifth Guard, the elite section of our army.", True )
    sceneManager.speak( august, "Being in that section had been my dream since my older brother died protecting it.", True )
    sceneManager.speak( august, "We could not know how this mission would change our lives... foregood.", True )
    sceneManager.speak( august, "March, Avril and me were the only candidates remaining.", True )
    sceneManager.speak( august, "The others had failed during their missions... or even died.", True )
    sceneManager.speak( august, "This were the Fifth Guard tests after all... not exactly a picknick.", True )
    sceneManager.speak( august, "Nearby fishermen had been attacked by some sea creature. Our job was to exterminate it.", True )
    sceneManager.speak( august, "We tracked it down to this beach quite easily.", True )

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
    sceneManager.speak( march, "One final test. The cave is here. Let's go." )

    ap = august.getPosition()
    sceneManager.move( [avril, march], [ap,ap] )

    partyManager.addRecord("inaran_intro_done")
    partyManager.refreshMap()

sceneManager.quitDialog()

