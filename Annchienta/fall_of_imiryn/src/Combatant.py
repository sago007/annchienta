import annchienta
import xml.dom.minidom
import BattleEntity
import Weapon, Action
import SceneManager, PartyManager

## Defines a combatant who takes part in a battle. BaseCombatant only
#  describes the mechanics part, Combatant also handles the drawing etc.
#
class Combatant( BattleEntity.BattleEntity ):

    # Where we should get the weapons from
    # weaponsLocation = "battle/weapons.xml"
    # weaponsXmlFile = xml.dom.minidom.parse( weaponsLocation )
    # Deprecated - we get weapons from the inventory now.

    # Where we should get the actions from
    actionsLocation = "battle/actions.xml"
    actionsXmlFile = xml.dom.minidom.parse( actionsLocation )

    def __init__( self, xmlElement ):

        # Call super constructor
        BattleEntity.BattleEntity.__init__( self, xmlElement )
    
        # We need to log stuff
        self.logManager = annchienta.getLogManager()

        # Get references
        self.videoManager = annchienta.getVideoManager()
        self.cacheManager = annchienta.getCacheManager()
        self.mathManager  = annchienta.getMathManager()
        self.sceneManager = SceneManager.getSceneManager()

        # Create a dictionary describing the level stuff
        self.level = {}
        levelElement = xmlElement.getElementsByTagName("level")[0]
        for k in levelElement.attributes.keys():
            self.level[k] = int(levelElement.attributes[k].value)

        # Create a dictionary describing the health stats
        self.healthStats = {}
        healthStatsElement = xmlElement.getElementsByTagName("healthstats")[0]
        for k in healthStatsElement.attributes.keys():
            self.healthStats[k] = int(healthStatsElement.attributes[k].value)
    
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

        # Get width and height from those facts.
        self.width = self.sx2-self.sx1
        self.height = self.sy2-self.sy1

        self.position = annchienta.Vector( 0, 0 )
        
        # We will draw a mark upon ourselves sometimes
        self.active = False
        self.selected = False
        
        # Damage done by an attack
        self.damage = 0
        self.damageTimer = 0.0

        self.reset()

    # Prototype, must be overwritten
    def isAlly( self ):
        return True

    def getRow( self ):
        return self.row

    def changeRow( self ):
        rowDeltaX = 30
        if self.getRow() == "front":
            self.position.x += -rowDeltaX if self.isAlly() else rowDeltaX
        else:
            self.position.x += rowDeltaX if self.isAlly() else -rowDeltaX
        self.row = ( "front" if self.row=="back" else "back" )

    def setTimer( self, timer ):
        self.timer = timer

    def getTimer( self ):
        return self.timer

    def setPosition( self, position ):
        self.position = position

    def getPosition( self ):
        return self.position

    def getWidth( self ):
        return self.width

    def getHeight( self ):
        return self.height

    def setActive( self, active ):
        self.active = active

    def isActive( self ):
        return self.active

    def setSelected( self, selected ):
        self.selected = selected

    def isSelected( self ):
        return self.selected
    
    # Must be called before every battle
    def reset( self ):
    
        # Reset status effects
        self.statusEffects = []
        
        # Reset time bar
        self.timer = 100.0 * self.mathManager.randFloat()
    
        # Start in a random row, but usually it's the front.
        self.row = "front"
        if self.mathManager.randFloat() <= 0.3:
            self.changeRow()

        # Reset damage signs.
        self.damage = 0
        self.damageTimer = 0.0

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
            self.logManager.error("No action called "+actionName+" was found for "+self.getName()+" in "+self.actionsLocation+".")

    ## Calculates base damage for physical attacks
    #  \return Basedamage.
    def physicalBaseDamage( self ):
        att = self.getAttack()
        lvl = self.level["lvl"]
        return att + int( float(att + lvl) / 32.0 ) * int( float(att * lvl) / 24.0 )
        
    ## Calculates base damage for magical attacks
    #  \return Basedamage.
    def magicalBaseDamage( self ):
        mat = self.getMagicAttack()
        lvl = self.level["lvl"]
        return 4 * (mat + lvl)

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

    ## See if the player is wounded.
    #  \return If the player has critical health.
    def isCritical( self ):
        return self.getHp() < self.getMaxHp() * 0.15

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

        elif self.hasStatusEffect( statusEffect ):
            self.statusEffects.remove( statusEffect )
            return statusEffect

        return None

    ## See if this combatant has a certain status.
    #  \return If the combatant has this status.
    def hasStatusEffect( self, statusEffect ):
        return statusEffect in self.statusEffects

    ## Set a damage sign to be drawn
    #  \param damage Amount of damage
    def setDamage( self, damage ):
        self.damage = damage
        self.damageTimer = 0.0

    ## Stores all information about this combatant in the given
    #  xml element, so it can be loaded again later
    def writeToXML( self, xmlElement, document ):

        # Call superclass first
        BattleEntity.BattleEntity.writeToXML( self, xmlElement, document )

        # Set level info
        levelElement = document.createElement("level")
        for key in self.level:
            levelElement.setAttribute( str(key), str(self.level[key]) )
        xmlElement.appendChild( levelElement )

        # Set healthStats info
        healthStatsElement = document.createElement("healthstats")
        for key in self.healthStats:
            healthStatsElement.setAttribute( str(key), str(self.healthStats[key]) )
        xmlElement.appendChild( healthStatsElement )

        # Set possible actions      
        actionsElement = document.createElement("actions")
        # Create a text with the actions
        text = ""
        for action in self.actions:
            text += action.getName() + " "
        textNode = document.createTextNode( text )
        actionsElement.appendChild( textNode )
        xmlElement.appendChild( actionsElement )

        # Set sprite info
        spriteElement = document.createElement("sprite")
        spriteElement.setAttribute( "filename", self.spriteFilename )
        spriteElement.setAttribute( "x1", str(self.sx1) )
        spriteElement.setAttribute( "y1", str(self.sy1) )
        spriteElement.setAttribute( "x2", str(self.sx2) )
        spriteElement.setAttribute( "y2", str(self.sy2) )
        xmlElement.appendChild( spriteElement )

    ## Updates this combatant this includes updating his
    #  ATB gauge, his appearance...
    #  \param ms Milliseconds past since last update.
    def update( self, ms ):
        
        factor = 1.0
        # Slow/haste
        if self.hasStatusEffect( "slowed" ):
            factor = 0.5
        elif self.hasStatusEffect( "hasted" ):
            factor = 1.8
        elif self.hasStatusEffect( "paralysed" ):
            factor = 0.1

        self.timer += factor * 0.020 *ms* float(255+self.getSpeed())/512.0
        if self.timer >= 100.0:
            self.timer = 100.0

        # Update damage sign
        if self.damage != 0:
            self.damageTimer += 0.0005*ms
            if self.damageTimer >= 1.0:
                self.damage = 0
                self.damageTimer = 0.0

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
        if self.isSelected() or self.isActive():
            self.videoManager.push()

            self.videoManager.translate( 0, -self.height )

            # Select a different color when we're selected and marked.
            if self.isSelected() and self.isActive():
                self.videoManager.setColor( 255, 0, 0, 150 )
            else:
                self.videoManager.setColor( 255, 255, 0, 150 )

            self.videoManager.drawTriangle( int(-self.width/2), 0, 0, int(self.height/2), int(self.width/2), 0 )
            self.videoManager.setColor()

            self.videoManager.pop()

        # Status effects
        for i in range(len(self.statusEffects)):

            statusEffect = self.statusEffects[i]
            sprite = self.cacheManager.getSurface( "images/statuseffects/" + statusEffect + ".png" )

            x = 0
            if self.isAlly():
                x = int( -self.width/2 - int(1+i/2) * sprite.getWidth() )
            else:
                x = int( self.width/2 + int(i/2) * sprite.getWidth() )
            y = int( -self.height/2 + (i%2) * sprite.getWidth() )

            self.videoManager.drawSurface( sprite, x, y )
            
        # Actual sprite
        self.videoManager.drawSurface( self.sprite, int( -self.width/2 ), int( -self.height/2 ), self.sx1, self.sy1, self.sx2, self.sy2 )

        # Draw damage stuff
        if self.damage != 0:

            string = str(self.damage if self.damage>0 else -self.damage)
            dy = int(-40.0*self.damageTimer)
            self.videoManager.setColor( 0, 0, 0 )

            # Draw a black border first
            self.videoManager.drawStringCentered( self.sceneManager.getLargeDefaultFont(), string, -1, dy )
            self.videoManager.drawStringCentered( self.sceneManager.getLargeDefaultFont(), string, 1, dy )
            self.videoManager.drawStringCentered( self.sceneManager.getLargeDefaultFont(), string, 0, dy-1 )
            self.videoManager.drawStringCentered( self.sceneManager.getLargeDefaultFont(), string, 0, dy+1 )

            if self.damage > 0:
                self.videoManager.setColor( 255, 0, 0 )
            else:
                self.videoManager.setColor( 0, 255, 0 )
            
            # Now go for the real thing
            self.videoManager.drawStringCentered( self.sceneManager.getLargeDefaultFont(), string, 0, dy )

        self.videoManager.setColor()
        self.videoManager.pop()
