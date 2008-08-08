import annchienta
import xml.dom.minidom
import Weapon, Action
import SceneManager, PartyManager

## Defines a combatant who takes part in a battle. BaseCombatant only
#  describes the mechanics part, Combatant also handles the drawing etc.
#
class BaseCombatant:

    # Where we should get the weapons from
    # weaponsLocation = "battle/weapons.xml"
    # weaponsXmlFile = xml.dom.minidom.parse( weaponsLocation )
    # Deprecated - we get weapons from the inventory now.

    # Where we should get the actions from
    actionsLocation = "battle/actions.xml"
    actionsXmlFile = xml.dom.minidom.parse( actionsLocation )

    def __init__( self, xmlElement ):
    
        # We need to log stuff
        self.logManager = annchienta.getLogManager()
    
        # Set our name
        self.name = str(xmlElement.getAttribute("name"))
    
        # Create a dictionary describing the level stuff
        self.level = {}
        levelElement = xmlElement.getElementsByTagName("level")[0]
        for k in levelElement.attributes.keys():
            self.level[k] = int(levelElement.attributes[k].value)

        # Create a dictionary describing the primary stats
        self.primaryStats = {}
        primaryStatsElement = xmlElement.getElementsByTagName("primarystats")[0]
        for k in primaryStatsElement.attributes.keys():
            self.primaryStats[k] = int(primaryStatsElement.attributes[k].value)
    
        # Create a dictionary describing the health stats
        self.healthStats = {}
        healthStatsElement = xmlElement.getElementsByTagName("healthstats")[0]
        for k in healthStatsElement.attributes.keys():
            self.healthStats[k] = int(healthStatsElement.attributes[k].value)
    
        # Get our weapon (if there is one! enemies usually have no weapons)
        weaponElements = xmlElement.getElementsByTagName("weapon")
        if len(weaponElements):
            # Get the weapon name and search for the corresponding element
            weaponName = str(weaponElements[0].getAttribute("name"))
            self.setWeapon( weaponName )
        else:
            self.weapon = 0
    
        # Get all possible actions. The actual actions are in the first child
        # of the element, hence the code. <actions> action1 action2 </actions>
        actionsElement = xmlElement.getElementsByTagName("actions")[0]
        actionNames = str(actionsElement.firstChild.data).split()
        # Prepare to get the from the xml data
        self.actions = []
        # Get them
        for a in actionNames:
            self.addAction( a )
            
        # Create a dictionary describing the elemental properties
        # Only enemies have them, usually
        self.primaryElemental = {}
        elementalElements = xmlElement.getElementsByTagName("elemental")
        if len(elementalElements):
            for k in elementalElements[0].attributes.keys():
                self.primaryElemental[k] = int(elementalElements[0].attributes[k].value)
    
        # Generate derived stats
        self.generateDerivedStats()
    
        self.reset()
    
    # Must be called before every battle
    def reset( self ):
    
        # Reset status effects
        self.statusEffects = []
        
        # Reset time bar
        self.timer = 100.0 * annchienta.randFloat()
    
        # Start in the front row
        self.row = "front"

    # Will generate derived stats based on equipped weapon.
    def generateDerivedStats( self ):
        
        # Base them on the primaries
        self.derivedStats = dict(self.primaryStats)
        
        # Then add weapon stats
        if self.weapon:
            for key in self.primaryStats:
                self.derivedStats[key] += self.weapon.stats[key]
    
        # Cap everything at 255
        for key in self.derivedStats:
            self.derivedStats[key] = self.derivedStats[key] if self.derivedStats[key]<255 else 255
    
        # Base elemental properties on weapon
        if self.weapon:
            self.derivedElemental = dict(self.weapon.elemental)
        else:
            self.derivedElemental = dict(self.primaryElemental)
    
    def setWeapon( self, weaponName ):

        partyManager = PartyManager.getPartyManager()
        inventory = partyManager.inventory

        element = inventory.getElement( weaponName )
        
        self.weapon = Weapon.Weapon( element )
        self.generateDerivedStats()

    def addAction( self, actionName ):

        actionElements = self.actionsXmlFile.getElementsByTagName("action")
        # Get them
        actionName = actionName.replace( '_', ' ' )
        found = filter( lambda w: w.getAttribute("name")==actionName, actionElements )
        if len(found):
            self.actions += [ Action.Action( found[0] ) ]
        else:
            self.logManager.error("No action called "+actionName+" was found for "+self.name+" in "+self.actionsLocation+".")

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

    def addHealth( self, health ):
        self.healthStats["hp"] += health
        if self.healthStats["hp"]<0:
            self.healthStats["hp"] = 0
        if self.healthStats["hp"]>self.healthStats["mhp"]:
            self.healthStats["hp"] = self.healthStats["mhp"]

    def update( self, ms ):
        
        self.timer += 0.015*ms* float(255+self.derivedStats["spd"])/512.0
        if self.timer >= 100.0:
            self.timer = 100.0

    # prototype, not correct
    def selectAction( self, battle ):
        return self.actions[ annchienta.randInt( 0, len(self.actions)-1 ) ]

## Now the graphical interface
#
class Combatant(BaseCombatant):

    def __init__( self, xmlElement ):
    
        # Call superclass constructor
        BaseCombatant.__init__( self, xmlElement )
        
        # Get references
        self.videoManager = annchienta.getVideoManager()
        self.sceneManager = SceneManager.getSceneManager()
        
        # Load sprite
        spriteElement = xmlElement.getElementsByTagName("sprite")[0]
        # Keep the filename so we can save it later on
        self.spriteFilename = str(spriteElement.getAttribute("filename"))
        self.sprite = annchienta.Surface( self.spriteFilename )
        if spriteElement.hasAttribute("x1"):
            self.sx1 = int(spriteElement.getAttribute("x1"))
            self.sy1 = int(spriteElement.getAttribute("y1"))
            self.sx2 = int(spriteElement.getAttribute("x2"))
            self.sy2 = int(spriteElement.getAttribute("y2"))
        else:
            self.sx1, self.sy1 = 0, 0
            self.sx2 = self.sprite.getWidth()
            self.sy2 = self.sprite.getHeight()

        self.width = self.sx2-self.sx1
        self.height = self.sy2-self.sy1

        self.position = annchienta.Vector( 0, 0 )
        
        # We will draw a mark upon ourselves sometimes
        self.marked = False
        
        # Damage done by an attack
        self.damage = 0
        self.damageTimer = 0.0

    def update( self, ms ):

        # Call base update
        BaseCombatant.update( self, ms )

        if self.damage != 0:
            self.damageTimer += 0.0005*ms
            if self.damageTimer >= 1.0:
                self.damage = 0
                self.damageTimer = 0.0

    def draw( self ):
    
        self.videoManager.pushMatrix()
        self.videoManager.translate( self.position.x, self.position.y )

        if self.marked:
            self.videoManager.pushMatrix()

            self.videoManager.translate( 0, -self.height )
            self.videoManager.setColor( 255, 255, 0 )
            self.videoManager.drawTriangle( -self.width/2, 0, 0, self.height/2, self.width/2, 0 )
            self.videoManager.setColor()

            self.videoManager.popMatrix()
        
        self.videoManager.drawSurface( self.sprite, -self.width/2, -self.height/2, self.sx1, self.sy1, self.sx2, self.sy2 )

        # Draw damage stuff
        if self.damage != 0:

            string = str(self.damage if self.damage>0 else -self.damage)
            dy = int(-40.0*self.damageTimer)
            self.videoManager.setColor( 0, 0, 0 )

            # Draw a black border first
            self.videoManager.drawStringCentered( self.sceneManager.largeRegularFont, string, -1, dy )
            self.videoManager.drawStringCentered( self.sceneManager.largeRegularFont, string, 1, dy )
            self.videoManager.drawStringCentered( self.sceneManager.largeRegularFont, string, 0, dy-1 )
            self.videoManager.drawStringCentered( self.sceneManager.largeRegularFont, string, 0, dy+1 )

            if self.damage > 0:
                self.videoManager.setColor( 255, 0, 0 )
            else:
                self.videoManager.setColor( 0, 255, 0 )
            
            # Now go for the real thing
            self.videoManager.drawStringCentered( self.sceneManager.largeRegularFont, string, 0, dy )

        self.videoManager.setColor()
        self.videoManager.popMatrix()
        
