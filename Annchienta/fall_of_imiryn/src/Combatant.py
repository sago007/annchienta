import annchienta
import xml.dom.minidom
import Weapon, Action
import SceneManager, PartyManager

## Defines a combatant who takes part in a battle. BaseCombatant only
#  describes the mechanics part, Combatant also handles the drawing etc.
#
class Combatant:

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

        # Get references
        self.videoManager = annchienta.getVideoManager()
        self.cacheManager = annchienta.getCacheManager()
        self.mathManager  = annchienta.getMathManager()
        self.sceneManager = SceneManager.getSceneManager()

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
                self.primaryElemental[k] = float(elementalElements[0].attributes[k].value)
    
        # Generate derived stats
        self.generateDerivedStats()

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

        # Status effect currently displayed
        self.statusEffectTimer = 0.0

        self.reset()
    
    # Must be called before every battle
    def reset( self ):
    
        # Reset status effects
        self.statusEffects = []
        
        # Reset time bar
        self.timer = 100.0 * self.mathManager.randFloat()
    
        # Start in the front row
        self.row = "front"

        # Reset damage signs.
        self.damage = 0
        self.damageTimer = 0.0

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

        self.weapon = inventory.getWeapon( weaponName )
        self.generateDerivedStats()

    ## Adds an action to this combatant so he can
    #  use it in battle.
    #  \param actionName The name of the action to be added.
    def addAction( self, actionName ):

        actionElements = self.actionsXmlFile.getElementsByTagName("action")
        # Get them
        actionName = actionName.replace( '_', ' ' )
        found = filter( lambda w: w.getAttribute("name")==actionName, actionElements )
        if len(found):
            self.actions += [ Action.Action( found[0] ) ]
        else:
            self.logManager.error("No action called "+actionName+" was found for "+self.name+" in "+self.actionsLocation+".")

    ## Calculates base damage for physical attacks
    #  \return Basedamage.
    def physicalBaseDamage( self ):
        att = self.derivedStats["att"]
        lvl = self.level["lvl"]
        return att + int( float(att + lvl) / 32.0 ) * int( float(att * lvl) / 32.0 )
        
    ## Calculates base damage for magical attacks
    #  \return Basedamage.
    def magicalBaseDamage( self ):
        mat = self.derivedStats["mat"]
        lvl = self.level["lvl"]
        return 5 * (mat + lvl)

    ## Set health points for this combatant.
    #  \param health New health for this combatant.
    def setHp( self, hp ):
        self.healthStats["hp"] = hp
        # Cap the value
        if self.healthStats["hp"]<0:
            self.healthStats["hp"] = 0
        if self.healthStats["hp"]>self.healthStats["mhp"]:
            self.healthStats["hp"] = self.healthStats["mhp"]

    ## Get the hp for this combatant.
    #  \return This comabatant's hp.
    def getHp( self ):
        return self.healthStats["hp"]

    ## Get the amount of maximum hp.
    #  \return This combatant's max hp.
    def getMaxHp( self ):
        return self.healthStats["mhp"]

    ## Sets magic points for this combatant.
    #  \param mp New Magic points for this combatant
    def setMp( self, mp ):
        self.healthStats["mp"] = mp
        # Cap it.
        if self.healthStats["mp"]<0:
            self.healthStats["mp"] = 0
        if self.healthStats["mp"]>self.healthStats["mmp"]:
            self.healthStats["mp"] = self.healthStats["mmp"]

    ## Get the mp for this combatant
    #  \return This combatant's mp.
    def getMp( self ):
        return self.healthStats["mp"]

    ## Get the amount of maximum mp.
    #  \return This combatant's max mp.
    def getMaxMp( self ):
        return self.healthStats["mmp"]

    ## Add a certain status effect to this combatant.
    #  \param statusEffect Status effect to be added.
    def addStatusEffect( self, statusEffect ):
        if statusEffect not in self.statusEffects:
            self.statusEffects.append( statusEffect )

    ## Remove a certain status effect from this combatant.
    #  \param statusEffect Status effect to be removed. When not specified, the first status effect will be removed.
    #  \return The name of the removed status effect.
    def removeStatusEffect( self, statusEffect=None ):
        if statusEffect is None:
            if len(self.statusEffects)>0:
                toRemove = self.statusEffects[0]
                self.statusEffects.remove( toRemove )
                return toRemove

        elif hasStatusEffect( statusEffect ):
            self.statusEffects.remove( statusEffect )
            return statusEffect

        return None

    ## See if this combatant has a certain status.
    #  \return If the combatant has this status.
    def hasStatusEffect( self, statusEffect ):
        return statusEffect in self.statusEffects

    ## Updates this combatant this includes updating his
    #  ATB gauge, his appearance...
    #  \param ms Milliseconds past since last update.
    def update( self, ms ):
        
        factor = 1.0
        # Slow/haste
        if self.hasStatusEffect( "slowed" ):
            factor = 0.5
        elif self.hasStatusEffect( "hasted" ):
            factor = 1.7
        elif self.hasStatusEffect( "paralysed" ):
            factor = 0.1

        self.timer += factor * 0.020 *ms* float(255+self.derivedStats["spd"])/512.0
        if self.timer >= 100.0:
            self.timer = 100.0

        # Update damage sign
        if self.damage != 0:
            self.damageTimer += 0.0005*ms
            if self.damageTimer >= 1.0:
                self.damage = 0
                self.damageTimer = 0.0

        # Update status effect displayed.
        if len(self.statusEffects):
            self.statusEffectTimer += 0.001*ms
            while self.statusEffectTimer>=len(self.statusEffects):
                self.statusEffectTimer -= len( self.statusEffects )


    ## Function prototype, not correct, as
    #  derived classes should overwrite this.
    def selectAction( self, battle ):
        return self.actions[ self.mathManager.randInt( 0, len(self.actions) ) ]
 
    ## Draw combatant to the screen.
    #
    def draw( self ):
    
        self.videoManager.push()
        self.videoManager.translate( self.position.x, self.position.y )

        # Draw an arrow above our head when we're 'marked'.
        if self.marked:
            self.videoManager.push()

            self.videoManager.translate( 0, -self.height )
            self.videoManager.setColor( 255, 255, 0, 150 )
            self.videoManager.drawTriangle( -self.width/2, 0, 0, self.height/2, self.width/2, 0 )
            self.videoManager.setColor()

            self.videoManager.pop()

        # Status effects
        if len(self.statusEffects):    
            effect = self.statusEffects[ int(self.statusEffectTimer) % len(self.statusEffects) ]
            if self.ally:
                self.videoManager.drawStringRight( self.sceneManager.defaultFont, effect, -self.width/2, -self.height/2 )
            else:
                self.videoManager.drawString( self.sceneManager.defaultFont, effect, self.width/2, -self.height/2 )
        
        # Actual sprite
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
        self.videoManager.pop()
