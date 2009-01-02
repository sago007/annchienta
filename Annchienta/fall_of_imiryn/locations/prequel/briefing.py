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
sceneManager.text( "After receiving their orders, they travelled to the Inaran regions, where their task was to be accomplished...", None )

sceneManager.fade( 255, 255, 255, 2000 )
videoManager.setColor( 0, 0, 0 )
videoManager.drawStringCentered( sceneManager.largeItalicsFont, "Fall of Imiryn", videoManager.getScreenWidth()/2, 100 )
videoManager.drawStringCentered( sceneManager.italicsFont, "The Downfall of an Empire", videoManager.getScreenWidth()/2, 150 )
videoManager.flip()
videoManager.flip()
sceneManager.waitForClick()

currentMap.removeObject( banver )
sceneManager.quitDialog()
partyManager.changeMap( "locations/inaran/beach.xml", annchienta.Point( annchienta.TilePoint, 9, 14 ) )

