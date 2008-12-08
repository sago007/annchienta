import annchienta
import xml.dom.minidom
import Weapon

## Holds all items
class Inventory:

    itemsLocation = "battle/items.xml"
    itemsFile = xml.dom.minidom.parse( itemsLocation )

    # Loads items from xml element
    def __init__( self, xmlElement ):

        # Get some references
        self.logManager = annchienta.getLogManager()

        text = str(xmlElement.firstChild.data)
        words = text.split()

        self.dictionary = {}

        # Get all the items
        for i in range( len(words)/2 ):

            self.dictionary[ words[ i*2 ] ] = int( words[ i*2+1 ] )

    def toXml( self ):

        return reduce( lambda a,b: a+' '+b, map( lambda key: key+' '+str(self.dictionary[key]), self.dictionary.keys() ) )

    # Returns the type of an item
    def getItemType( self, itemName ):
        element = self.getElement( itemName )
        return str(element.getAttribute("type"))

    def getItemCount( self, itemName ):
        return self.dictionary[itemName]

    # Returns the description of an item
    def getItemDescription( self, itemName ):
        element = self.getElement( itemName )
        return str(element.getAttribute("description"))

    # Searches for the given itemName in the xml file
    # and possibly returns the corresponding element.
    def getElement( self, itemName ):

        elements = self.itemsFile.getElementsByTagName("item")
        found = filter( lambda el: str(el.getAttribute("name"))==itemName, elements )
        if len(found):
            return found[0]
        else:
            self.logManager.error("No item "+itemName+" found in "+self.itemsLocation+"." )

    def getAvailableWeapons( self ):

        # Find all items of type weapon
        weapons = filter( lambda i: self.getItemType(i)=="weapon", self.dictionary.keys() )
        # Make sure we have one
        weapons = filter( lambda w: self.dictionary[w]>0, weapons )
        return weapons

    def getAvailableLoot( self ):

        # Find all items of type loot
        loot = filter( lambda i: self.getItemType(i)=="loot", self.dictionary.keys() )
        # Make sure we have one
        loot = filter( lambda l: self.dictionary[l]>0, loot )
        return loot

    # Finds, creates and returns a weapon
    def getWeapon( self, weaponName ):

        return Weapon.Weapon( self.getElement( weaponName ) )

    def hasItem( self, itemName ):

        return itemName in self.dictionary.keys()

    def addItem( self, itemName ):

        if itemName in self.dictionary.keys():
            self.dictionary[ itemName ] += 1
        else:
            self.dictionary[ itemName ] = 1
            
    def removeItem( self, itemName ):

        if not self.hasItem( itemName ):
            self.logManager.warning( "Inventory.removeItem called with item that is not inventory: %s", itemName )
        else:
            self.dictionary[ itemName ] -= 1
            if self.dictionary[ itemName ] <= 0:
                del self.dictionary[ itemName ]

    def useItemOn( self, itemName, target ):

        if itemName=="potion":
            target.setHp( target.getHp() + 100 )

        elif itemName=="eyedrops":
            if "blinded" in target.statusEffects:
                target.removeStatusEffect( "blinded" )

        elif itemName=="tincture":
            target.setMp( target.getMp() + 30 )

        elif itemName=="feather":
            if "slowed" in target.statusEffects:
                target.removeStatusEffect( "slowed" )
            if not "hasted" in target.statusEffects:
                target.addStatusEffect( "hasted" )

        elif itemName=="grenade":
            target.setHp( target.getHp() - 120 )
        
        elif itemName=="oil":
            if "paralysed" in target.statusEffects:
                target.removeStatusEffect( "paralysed" )

        elif itemName=="hi-potion":
            target.setHp( target.getHp() + 350 )

        self.removeItem( itemName )

