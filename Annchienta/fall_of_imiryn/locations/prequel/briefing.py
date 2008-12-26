import annchienta
import PartyManager, SceneManager, BattleManager

mapManager = annchienta.getMapManager()
videoManager = annchienta.getVideoManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

currentMap = partyManager.currentMap

partyManager.addRecord("facilities_met_banver")

# Create a whole bunch of objects/persons and set them to
august = partyManager.player
march = currentMap.getPerson("march")
avril = currentMap.getPerson("avril")

banver = annchienta.Person( "banver", "locations/facilities/banver.xml" )
banver.setPosition( annchienta.Point( annchienta.TilePoint, 2, 5 ) )
currentMap.addObject( banver )

# Init our dialog.
sceneManager.initDialog( [august, march, avril, banver] )

# Set correct headings and animations.
august.lookAt( banver )
march.lookAt( banver )
avril.lookAt( banver )

sceneManager.speak( banver, "Greetings, recruits. It's good to see you back." )
sceneManager.speak( banver, "The Fifth Guard currently has sixteen members. Sixteen of the best warriors." )
sceneManager.speak( banver, "You three might be part of it soon. There only rests one task." )

sceneManager.speak( banver, "First, I want to congratulate you for finishing your personal task." )
sceneManager.speak( banver, "I especially want to congratulate March, who had asked to be given the hardest task." )
sceneManager.speak( banver, "But he brought it to a good end, and managed to kill a small dragon on his own." )
sceneManager.speak( banver, "He lost an arm in the fight. He has given us all an example of true courage." )

sceneManager.speak( banver, "Avril, August, you have done well, too." )
sceneManager.speak( banver, "Also, let us remember those who didn't make it. A minute of silence..." )

sceneManager.speak( avril, "What?! Are you saying all others died? Do you mean my sister..." )
sceneManager.speak( banver, "One of the qualities of a good warrior is to control herself, Avril. You shouldn't shout like that." )
sceneManager.speak( avril, "But I..." )
sceneManager.speak( banver, "There are those who succeed, and those who fail. There is nothing we can do about it." )

sceneManager.speak( banver, "Now, about your final task. I will be short." )
sceneManager.speak( banver, "Fishermen have recently been attacked by a terrible sea creature." )
sceneManager.speak( banver, "Most of the attacks happened around the Inaran region- in the very south of the Jemor continent." )
sceneManager.speak( banver, "Your task is to exterminate it. Finding out it's exact location and obtaining weapons is part of your task." )
sceneManager.speak( banver, "Good luck..." )

sceneManager.fade( 255, 255, 255, 2000 )
videoManager.setColor( 0, 0, 0 )
videoManager.drawStringCentered( sceneManager.largeItalicsFont, "One month later...", videoManager.getScreenWidth()/2, 100 )
videoManager.flip()
videoManager.flip()
sceneManager.waitForClick()

currentMap.removeObject( banver )
sceneManager.quitDialog()
partyManager.changeMap( "locations/inaran/beach.xml", annchienta.Point( annchienta.TilePoint, 9, 14 ) )
