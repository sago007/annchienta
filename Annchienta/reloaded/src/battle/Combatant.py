import annchienta
import xml.dom.minidom
import Weapon

## Defines a combatant who takes part in a battle. BaseCombatant only
#  describes the mechanics part, Combatant also handles the drawing etc.
#
class BaseCombatant:

    # Where we should get the weapons from
    weaponsLocation = "weapons.xml"
    weaponsXmlFile = xml.dom.minidom.parse( weaponsLocation )

    def __init__( self, xmlElement ):
    
        # We need to log stuff
        self.logManager = annchienta.getLogManager()
    
        # Set our name
        self.name = xmlElement.getAttribute("name")
    
        # Create a dictionary describing the primary stats
        self.primaryStats = {}
        primaryStatsElement = xmlElement.getElementsByTagName("primarystats")[0]
        for k in primaryStatsElement.attributes.keys():
            self.primaryStats[k] = int(primaryStatsElement.attributes[k].value)
    
        # Get our weapon (if there is one! enemies usually have no weapons)
        weaponElements = xmlElement.getElementsByTagName("weapon")
        if len(weaponElements):
            # Get the weapon name and search for the corresponding element
            weaponName = weaponElements[0].getAttribute("name")
            weaponElements = self.weaponsXmlFile.getElementsByTagName("weapon")
            found = filter( lambda w: w.getAttribute("name")==weaponName, weaponElements )
            if len(found):
                # Construct a weapon
                self.weapon = Weapon.Weapon( found[0] )
            else:
                self.logManager.error("No weapon called "+weaponName+" was found for "+self.name+".")
        else:
            self.weapon = 0
    
        # Generate derived stats
        self.generateDerivedStats()
    
    # Will generate derived stats based on equipped weapon.
    def generateDerivedStats( self ):
        
        # Base them on the primaries
        self.derivedStats = self.primaryStats
        
        # Then add weapon stats
        if self.weapon:
            for key in self.primaryStats:
                self.primaryStats[key] += self.weapon.stats[key]
        
