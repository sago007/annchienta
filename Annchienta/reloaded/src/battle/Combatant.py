import annchienta
import xml.dom.minidom
import Weapon, Action
import SceneManager

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
            
        # Create a dictionary describing the elemental properties
        # Only enemies have them, usually
        self.primaryElemental = {}
        elementalElements = xmlElement.getElementsByTagName("elemental")
        if len(elementalElements):
            for k in elementalElement.attributes.keys():
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
        weaponElements = self.weaponsXmlFile.getElementsByTagName("weapon")
        found = filter( lambda w: w.getAttribute("name")==weaponName, weaponElements )
        if len(found):
            # Construct a weapon
            self.weapon = Weapon.Weapon( found[0] )
        else:
            self.logManager.error("No weapon called "+weaponName+" was found for "+self.name+" in "+self.weaponsLocation+".")
        self.generateDerivedStats()

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
        
        # We will draw ourselves in another color if this is set to True
        self.hover = False
        
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

        if self.hover:
            self.videoManager.setColor( 0, 255, 0 )
        else:
            self.videoManager.setColor()
        
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

        self.videoManager.popMatrix()
        
