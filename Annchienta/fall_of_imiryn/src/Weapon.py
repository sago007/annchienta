import annchienta
from BattleEntity import BattleEntity

## A class to describe weapons
#
class Weapon( BattleEntity ):

    def __init__( self, xmlElement ):

        # Call super constructor.
        BattleEntity.__init__( self, xmlElement )
    
        # Set our name
        self.description = str(xmlElement.getAttribute("description"))

        # Get our sprite
        spriteElements = xmlElement.getElementsByTagName("sprite")
        if len(spriteElements):
            cacheManager = annchienta.getCacheManager()
            self.sprite = cacheManager.getSurface( str(spriteElements[0].getAttribute("filename") ) )
            self.grip = annchienta.Vector( float(spriteElements[0].getAttribute("gripx")), float(spriteElements[0].getAttribute("gripy")) )
        else:
            self.sprite = None
            self.grip = None
    
    def getDescription( self ):
        return self.description

    def getSprite( self ):
        return self.sprite

    def getGrip( self ):
        return self.grip
