import annchienta
import xml.dom.minidom
import Weapon, Action

## Defines a combatant who takes part in a battle. BaseCombatant only
#  describes the mechanics part, Combatant also handles the drawing etc.
#
class BaseCombatant:

    # Where we should get the weapons from
    weaponsLocation = "data/battle/weapons.xml"
    weaponsXmlFile = xml.dom.minidom.parse( weaponsLocation )
    # Where we should get the actions from
    actionsLocation = "data/battle/actions.xml"
    actionsXmlFile = xml.dom.minidom.parse( actionsLocation )

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
    
        # Create a dictionary describing the level stuff
        self.level = {}
        levelElement = xmlElement.getElementsByTagName("level")[0]
        for k in levelElement.attributes.keys():
            self.level[k] = int(levelElement.attributes[k].value)
    
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
                self.logManager.error("No weapon called "+weaponName+" was found for "+self.name+" in "+self.weaponsLocation+".")
        else:
            self.weapon = 0
    
        # Get all possible actions. The actual actions are in the first child
        # of the element, hence the code. <actions> action1 action2 </actions>
        actionsElement = xmlElement.getElementsByTagName("actions")[0]
        actionNames = actionsElement.firstChild.data.split()
        # Prepare to get the from the xml data
        self.actions = []
        actionElements = self.actionsXmlFile.getElementsByTagName("action")
        # Get them
        for a in actionNames:
            # Convert '_' to ' '
            a = a.replace( '_', ' ' )
            found = filter( lambda w: w.getAttribute("name")==a, actionElements )
            if len(found):
                self.actions += [ Action.Action( found[0] ) ]
            else:
                self.logManager.error("No action called "+a+" was found for "+self.name+" in "+self.actionsLocation+".")
        print map( lambda a: a.name, self.actions )
            
        # Create a dictionary describing the elemental properties
        # Only enemies have them, usually
        self.primaryElemental = {}
        elementalElements = xmlElement.getElementsByTagName("elemental")
        if len(elementalElements):
            for k in elementalElement.attributes.keys():
                self.primaryElemental[k] = int(elementalElements[0].attributes[k].value)
    
        # Generate derived stats
        self.generateDerivedStats()
    
        # Reset status effects
        self.statusEffects = []
    
    # Will generate derived stats based on equipped weapon.
    def generateDerivedStats( self ):
        
        # Base them on the primaries
        self.derivedStats = self.primaryStats
        
        # Then add weapon stats
        if self.weapon:
            for key in self.primaryStats:
                self.derivedStats[key] += self.weapon.stats[key]
    
        # Cap everything at 255
        for key in self.derivedStats:
            self.derivedStats[key] = self.derivedStats[key] if self.derivedStats[key]<255 else 255
    
        # Base elemental properties on weapon
        if self.weapon:
            self.derivedElemental = self.weapon.elemental
        else:
            self.derivedElemental = self.primaryElemental
    
    # base damage for physical attacks
    def physicalBaseDamage( self ):
        att = self.derivedStats["att"]
        lvl = self.level["lvl"]
        return att + int( float(att + lvl) / 32.0 ) * int( float(att * lvl) / 32.0 )
        
    # base damage for magical attacks
    def magicalBaseDamage( self ):
        mat = self.derivedStats["mat"]
        lvl = self.level["lvl"]
        return 6 * (mat + lvl)

    # prototype, not correct
    def selectAction( self ):
        return self.actions[ annchienta.randInt( 0, len(self.actions)-1 ) ]

## Now the graphical interface
#
class Combatant(BaseCombatant):

    def __init__( self, xmlElement ):
    
        # Call superclass constructor
        BaseCombatant.__init__( self, xmlElement )
        
        
