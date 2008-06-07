import annchienta, scene, party

partyManager = party.getPartyManager()
sceneManager = scene.getSceneManager()

krelshar = annchienta.StaticObject( "krelshar", "locations/tasumian/krelshar.xml" )
player = partyManager.player

point = player.getPosition().to( annchienta.IsometricPoint )
point.x -= 30
krelshar.setPosition( point )

partyManager.currentMap.addObject( krelshar )

changeMap = False

def fight_krelshar():

    sceneManager.speak( krelshar, "You stubborn fools! Feel my wrath!" )
    audioManager.playMusic( "music/battle_1.ogg" )

    # Create some enemies
    enemies = map( lambda a:battle.getBattleManager().createEnemy(a), ["ghost", "krelshar", "ghost"] )

    # Start a battle.
    b = battle.Battle( partyManager.team + enemies )
    b.background = annchienta.Surface("images/backgrounds/woods.png")
    b.run()

    if b.won:
        partyManager.addRecord( "tasumian_passed_krelshar" )

if not partyManager.hasRecord( "tasumian_met_krelshar" ):

    partyManager.addRecord( "tasumian_met_krelshar" )
    sceneManager.speak( krelshar, "Where do you think you are headed? These woods belong to me!" )
    a = sceneManager.chat( krelshar, "Speak up, you dirty rats!", ["I'm sorry, we didn't know that...", "I go where I want!"] )

    if a==1:
        fight_krelshar()
    else:
        sceneManager.speak( krelshar, "You better show some respect if you want to pass this forest alive." )
        sceneManager.speak( krelshar, "All I want from you is a tiny little favor. When I was still alive, I was a famous trapper." )
        sceneManager.speak( krelshar, "Until one day, I was ambushed by wolves..." )
        sceneManager.speak( krelshar, "I want you to go back into the woods and kill some wolves. Four should be enough." )
        a = sceneManager.chat( krelshar, "How about that, you filthy worms?", ["We'll go and hunt wolves down.", "Hunt your wolves yourself, you demon!"] )
        if a==1:
            fight_krelshar()
        else:
            player.setPosition( annchienta.Point( annchienta.TilePoint, 8, 13 ) )

elif not partyManager.hasRecord( "tasumian_passed_krelshar" ):

    needed = 4-sum( map( lambda i: partyManager.hasRecord("tasumian_killed_wolf"+str(i)), range(1,5) ) )

    if needed==0:
        sceneManager.speak( krelshar, "Good... that will teach them... you can pass now." )
        partyManager.addRecord( "tasumian_passed_krelshar" )
        player.setPosition( annchienta.Point( annchienta.TilePoint, 8, 13 ) )
    else:
        a = sceneManager.chat( krelshar, "You need to kill "+str(needed)+" more wolves...", ["Allright...", "No way!"] )
        if a==1:
            fight_krelshar()
        else:
            player.setPosition( annchienta.Point( annchienta.TilePoint, 8, 13 ) )

else:
    changeMap = True
    partyManager.currentMap.removeObject( krelshar )
    partyManager.changeMap( "locations/world/world.xml", annchienta.Point( annchienta.TilePoint, 7, 13 ) )

if not changeMap:
    partyManager.currentMap.removeObject( krelshar )
    partyManager.refreshMap()
