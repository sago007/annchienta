import annchienta
import PartyManager, SceneManager, BattleManager

mapManager = annchienta.getMapManager()
videoManager = annchienta.getVideoManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

currentMap = partyManager.getCurrentMap()

august = partyManager.getPlayer()

# Addobject and stuff...
march = annchienta.Person( "march", "locations/common/march.xml" )
avril = annchienta.Person( "avril", "locations/common/avril.xml" )

position = august.getPosition().to( annchienta.TilePoint )
currentMap.addObject( march, annchienta.Point( annchienta.TilePoint, position.x+1, position.y-1) )
currentMap.addObject( avril, annchienta.Point( annchienta.TilePoint, position.x+1, position.y+1) )
sceneManager.initDialog( [august, march, avril] )

sceneManager.speak( august, "It wasn't long before we reached the end of the mountains, like Kyzano had told us. But when we arrived...", True )

position.x -= 5

sceneManager.move( [august, march, avril], [ annchienta.Point( annchienta.TilePoint, position.x, position.y  ),
                                             annchienta.Point( annchienta.TilePoint, position.x+1, position.y-1 ), 
                                             annchienta.Point( annchienta.TilePoint, position.x+1, position.y+1 ) ] )

sceneManager.speak( avril, "What the fuck?!" )
sceneManager.speak( march, "Avril, language. August, I guess this is what your brother meant by... something unusual." )
sceneManager.speak( august, "I'll open the letter, then..." )

sceneManager.speak( august, "Dear brother. I'm writing this letter as you are sitting by a campfire. I can see you, but it would be useless to approach you now.", True )
sceneManager.speak( august, "You might remember that I fought Enthavos. They told us, members of the Fifth Guard, he had become mad.", True )
sceneManager.speak( august, "We found him attacking the empire... but now I know that he was not mad.", True )
sceneManager.speak( august, "He had discovered a the most terrible secret.", True )
sceneManager.speak( august, "We managed to defeat him, but... I was seriously injured.", True )
sceneManager.speak( august, "I was taken away by other soldiers, and reported death.", True )
sceneManager.speak( august, "After my 'death', I was taken to the Nupol continent.", True )
sceneManager.speak( august, "I awoke in the facilties you are probably looking at right now. In there, they were able to save my life using advanced technologies.", True )
sceneManager.speak( august, "But that all had a price. I was forced to guard their facilties, so nobody could get near.", True )
sceneManager.speak( august, "I was told that when I didn't obey, my brother would become victim of a mysterious murder.", True )
sceneManager.speak( august, "It is, however, of vital importance that these facilities are stopped.", True )
sceneManager.speak( august, "In this letter you will find an access card as well. You can use it to enter these facilities.", True )
sceneManager.speak( august, "You MUST check in before wednesday. If I don't check in every five days... They'll kill me.", True )
sceneManager.speak( august, "What day are we?" )
sceneManager.speak( march, "Absolutely no idea. Continue." )
sceneManager.speak( august, "Something very... evil is going on in those facilities. You need to bring an end to it.", True )
sceneManager.speak( august, "Use everything you can to stop it. Don't be afraid to kill their guards if you have to...", True )
sceneManager.speak( august, "After all, they were threatening to kill you, too...", True )
sceneManager.speak( august, "I will help you, so you will not be alone.", True )
sceneManager.speak( august, "See you soon, brother. I will be watching you.", True )
sceneManager.speak( august, "That's it..." )
sceneManager.speak( march, "Let's go, then." )

sceneManager.fade()

partyManager.addRecord("mountains_read_letter")

# Continue to facilities.
partyManager.changeMap("locations/facilities/entrance.xml", annchienta.Point( annchienta.TilePoint, 17, 28 ) )

sceneManager.quitDialog()
currentMap.removeObject( march )
currentMap.removeObject( avril )

partyManager.refreshMap()

