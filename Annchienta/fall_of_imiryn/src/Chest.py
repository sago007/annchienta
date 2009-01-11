import annchienta
import SceneManager
import PartyManager

class Chest( annchienta.StaticObject ):

    chestConfigFile = "locations/common/chest.xml"

    def __init__( self, item, uniqueId ):

        annchienta.StaticObject.__init__( self, "chest", self.chestConfigFile )

        self.item = item
        self.uniqueId = uniqueId

        self.setOnInteractCode(
"""
audioManager = annchienta.getAudioManager()
cacheManager = annchienta.getCacheManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()
chest = annchienta.getPassiveObject()

if not partyManager.hasRecord( '""" + self.getUniqueId() + """' ):
    audioManager.playSound( cacheManager.getSound( "sounds/chest.ogg" ) )
    chest.setAnimation( "opened" )
    partyManager.getInventory().addItem( '""" + self.getItem() + """' )
    partyManager.addRecord( '""" + self.getUniqueId() + """' )
    sceneManager.text( "Found """ + self.getItem() + """!" )

else:
    sceneManager.text( "This chest is empty." )
"""
        )
    
    def getUniqueId( self ):
        return self.uniqueId

    def getItem( self ):
        return self.item
