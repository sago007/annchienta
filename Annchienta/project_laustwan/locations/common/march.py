import annchienta
import PartyManager, SceneManager

mapManager = annchienta.getMapManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

march = annchienta.getPassiveObject()
august = annchienta.getActiveObject()

sceneManager.initDialog( [march, august] )

if not partyManager.hasRecord("inaran_intro_march"):

    avril = partyManager.currentMap.getObject( "avril" )
    laustwan = partyManager.currentMap.getObject( "laustwan" )

    sceneManager.speak( march, "Can you see that cave over there? That must be it." )

    sceneManager.speak( august, "I guess... finally..." )

    sceneManager.speak( august, "We had been searching these Inaran areas for a week.", True )
    sceneManager.speak( august, "It was supposed to be our last test before we could join the Fifth Guard.", True )

    lp = laustwan.getPosition().to( annchienta.IsometricPoint )
    lp.x += 60
    sceneManager.move( laustwan, lp )
    sceneManager.speak( laustwan, "Puko!" )

    sceneManager.speak( august, "Can we leave the laustwan here?" )
    sceneManager.speak( march, "Sure. He will find it's way to another master, they always do." )
    sceneManager.speak( laustwan, "Gri-huk." )

    sceneManager.speak( avril, "Well, you've been really helpful... I'm glad we had you with us. You are free now." )
    sceneManager.speak( august, "Why doesn't it run off? You released it, right?" )

    sceneManager.speak( laustwan, "Hog-hu." )

    sceneManager.speak( avril, "Maybe he doesn't realize it yet. Or he thinks I'll take him back. Anyway, we're not here to talk about laustwan." )
    sceneManager.speak( august, "I never really understood these helpful human-like creatures.", True )
    sceneManager.speak( august, "Still, I was grateful to them that they were there, always helping humans out.", True )
    sceneManager.speak( march, "One final test. Let's go." )

    partyManager.addRecord("inaran_intro_march")

sceneManager.quitDialog()

