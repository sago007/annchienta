import annchienta, scene, party

partyManager = party.getPartyManager()
sceneManager = scene.getSceneManager()

def keepOnReading():

    a = sceneManager.chat( None, "Do you want to keep on reading?", ["Read some more.", "That'll be enough."] )
    return (a==0)

def read():
    sceneManager.text( "It is a book about the island Welsar. Welsar joined the Alliance seven years after the Creation of the Alliance." )
    sceneManager.text( "... Welsar is naturally divided into two. There is the northern part, where Tetia is situated. And there is the southern part, with Anpere." )
    sceneManager.text( "Most people live in the southern part, near Anpere. Anpere is the main city of Welsar, and the port..." )

    if not keepOnReading():
        return

    sceneManager.text( "... In the northern part is Tetia probably the only town worth mentioning. There is a large prison complex as well, built 84 years after the Creation of the Alliance." )
    sceneManager.text( "Most farmers live in the southern part, as there are still many wild beasts up to the north..." )

    if not keepOnReading():
        return

    sceneManager.text( "... The island is divided by two natural structures: the central mountains, and the Tasumian woods." )
    sceneManager.text( "Since most travellers were not be able to go through either of those, a road was built in between 56 years after the Creation of the Alliance..." )

    if not keepOnReading():
        return

    sceneManager.text( "... Since the colonisation of this island Welsar, contact with other islands was always maintained very well." )
    sceneManager.text( "This island, however, is situated rather far from most islands in the Alliance..." )

    if not keepOnReading():
        return

    sceneManager.text( "... That's why, until today, the island of Aldwar remains our most important trade contact." )
    sceneManager.text( "A ship for Aldwar parts every three days..." )

    if not partyManager.hasRecord("tetia_read_book"):

        if not keepOnReading():
            return

        # Should give something to readers here.
        sceneManager.text( "... For the attentive readers..." )
        sceneManager.text( "You received the Medic strategy!" )

        for c in partyManager.team:
            c.strategies += ["medic"]

        partyManager.addRecord("tetia_read_book")

read()
