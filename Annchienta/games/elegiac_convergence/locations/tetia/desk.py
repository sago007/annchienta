import annchienta, scene, party

partyManager = party.getPartyManager()
sceneManager = scene.getSceneManager()

def keepOnReading():

    a = sceneManager.chat( None, "Do you want to keep on reading?", ["Read some more.", "That'll be enough."] )
    return (a==0)

def read():
    sceneManager.text( "It is a book about the island Welsar." )
    sceneManager.text( "... Welsar is naturally divided into two. There is the northern part, where Tetia is situated. And there is the southern part, with Anpere." )
    sceneManager.text( "Most people live in the southern part, near Anpere. Anpere is the main city of Welsar, and the port..." )

    if not keepOnReading():
        return

    sceneManager.text( "... In the northern part is Tetia probably the only town worth mentioning. There is a prison complex as well." )
    sceneManager.text( "Most farmers live in the southern part, as there are still many wild beasts up to the north..." )

    if not keepOnReading():
        return

    sceneManager.text( "... The island is divided by two natural structures: the central mountains, and the Tasumian woods." )
    sceneManager.text( "Since most travellers would not be able to go through either of those, a road was built in between..." )

read()
