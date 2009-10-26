import annchienta
import Combatant, MenuItem, Menu, Action
import PartyManager

class Ally( Combatant.Combatant ):

    def __init__( self, xmlElement ):

        # Stuff for sounds
        self.cacheManager = annchienta.getCacheManager()
        self.audioManager = annchienta.getAudioManager()
        self.soundLevelup = self.cacheManager.getSound('sounds/levelup.ogg')
        self.soundClickNeu = self.cacheManager.getSound('sounds/click-neutral.ogg')

        # Base constructor
        Combatant.Combatant.__init__( self, xmlElement )
        
        # References
        self.partyManager = PartyManager.getPartyManager()
        self.logManager   = annchienta.getLogManager()
        self.inputManager = annchienta.getInputManager()
        self.videoManager = annchienta.getVideoManager()
    
        # Get our weapon
        weaponElements = xmlElement.getElementsByTagName("weapon")
        if len(weaponElements):
            # Get the weapon name and search for the corresponding element
            weaponName = str(weaponElements[0].getAttribute("name"))
            self.setWeapon( weaponName )
        else:
            self.logManager.warning( "No Weapon defined for Ally!" )

        # Get the position of our hand
        handElements = xmlElement.getElementsByTagName("hand")
        if len(handElements):
            self.hand = annchienta.Vector( float(handElements[0].getAttribute("x")), float(handElements[0].getAttribute("y")) )
        else:
            self.hand = None
    
        # Create a dictionary describing the level grades
        self.grades = {}
        gradesElement = xmlElement.getElementsByTagName("grades")[0]
        for k in gradesElement.attributes.keys():
            self.grades[k] = int(gradesElement.attributes[k].value)

        # Create dictionary describing the level learns
        self.learn = {}
        learnElement = xmlElement.getElementsByTagName("learn")[0]
        text = str(learnElement.firstChild.data)
        words = text.split()
        for i in range( int(len(words)/2) ):
            self.learn[ int( words[i*2] ) ] = words[i*2+1]

        # Build the menu.
        self.buildMenu()

    def isAlly( self ):
        return True
    
    def getAttack( self ):
        return Combatant.Combatant.getAttack(self) + self.weapon.getAttack()

    def getDefense( self ):
        return Combatant.Combatant.getDefense(self) + self.weapon.getDefense()

    def getMagicAttack( self ):
        return Combatant.Combatant.getMagicAttack(self) + self.weapon.getMagicAttack()

    def getMagicDefense( self ):
        return Combatant.Combatant.getMagicDefense(self) + self.weapon.getMagicDefense()

    def getSpeed( self ):
        return Combatant.Combatant.getSpeed(self) + self.weapon.getSpeed()

    def getElementalFactor( self, element ):
        return self.weapon.getElementalFactor( element )

    def setWeapon( self, weaponName ):

        partyManager = PartyManager.getPartyManager()
        inventory = partyManager.getInventory()
        self.weapon = inventory.getWeapon( weaponName )

    def getWeapon( self ):
        return self.weapon

    ## Stores all information about this ally in the given
    #  xml element, so it can be loaded again later.
    def writeToXML( self, xmlElement, document ):

        # Call superclass first
        Combatant.Combatant.writeToXML( self, xmlElement, document )

        # Set grades info
        gradesElement = document.createElement("grades")
        for key in self.grades:
            gradesElement.setAttribute( str(key), str(self.grades[key]) )
        xmlElement.appendChild( gradesElement )

        # Set weapon name
        weaponElement = document.createElement("weapon")
        weaponElement.setAttribute("name", str( self.weapon.getName() ) )
        xmlElement.appendChild( weaponElement )

        # Set our hand
        if self.hand:
            handElement = document.createElement("hand")
            handElement.setAttribute("x", str(int(self.hand.x)))
            handElement.setAttribute("y", str(int(self.hand.y)))
            xmlElement.appendChild( handElement )

        # Set learn info
        learnElement = document.createElement("learn")

        # Create a text with the actions
        text = ' '
        if len( self.learn ):
            for key in self.learn:
                text += str(key) + " " + str(self.learn[key]) + " "

        textNode = document.createTextNode( text )
        learnElement.appendChild( textNode )
        xmlElement.appendChild( learnElement )

    ## Create a menu with all options this Ally
    #  can use in battle.
    def buildMenu( self ):
    
        self.menu = Menu.Menu( self.name, "Select an action." )
        subs = []
        for action in self.actions:

            # Create a decription first
            description = action.getDescription()
            if action.getCost()>0:
                description += " ("+str(action.getCost())+"MP)"

            menuItem = MenuItem.MenuItem( action.getName(), description )
            if action.getCost() > self.getMp():
                menuItem.setEnabled( False )
            added = False

            for sub in subs:
                if sub.name == action.getCategory():
                    sub.options += [menuItem]
                    added = True

            if not added:
                if action.category=="top":
                    subs += [menuItem]
                else:
                    newsub = Menu.Menu( action.getCategory() )
                    newsub.options += [menuItem]
                    subs += [newsub]
                
        self.itemMenu = Menu.Menu( "item", "Use items." )
        subs += [ self.itemMenu ]
        self.buildItemMenu()

        # set options and align
        self.menu.setOptions( subs )
        self.menu.leftBottom()

    # create the item menu
    def buildItemMenu( self ):
        
        inv = self.partyManager.getInventory()
        loot = inv.getAvailableLoot()
        items = []
        for lootItem in loot:
            items += [ MenuItem.MenuItem( lootItem, inv.getItemDescription(lootItem)+" ("+str(inv.getItemCount(lootItem))+" left)" ) ]
        self.itemMenu.setOptions( items )
        self.itemMenu.leftBottom()

    ## Allies select an action from the menu. returns (action, target)
    def selectAction( self, battle ):

        # Build a menu first
        self.buildMenu()

        menuItem = self.menu.pop( battle )
        if menuItem is None:
            return None, None

        found = filter( lambda action: action.getName() == menuItem.getName(), self.actions )

        needsTarget = True
        action = None

        # We found an action
        if len(found):

            action = found[0]

            # Check if there is enough mp
            if self.getMp() < action.getCost():
                battle.addLine( self.getName().capitalize()+" doesn't have enough MP!" )
                return None, None
        
            if not action.hasTarget():
                needsTarget = False

        # No real action, check if it's an item
        # ... create an action on the fly
        elif self.partyManager.getInventory().hasItem( menuItem.name ):

            action = Action.Action()
            action.name = menuItem.name
            action.category = "item"
            action.target = 1

        # Select a target when needed
        target = None
        if needsTarget:
            # Start with allies when it's restorative magic.
            target = self.selectTarget( battle, not action.hasElement("restorative") )
            if target is None:
                return None, None

        return action, target

    def draw( self ):

        # Draw ourself
        Combatant.Combatant.draw( self )

        # draw the weapon
        if self.hand and self.getWeapon().getSprite():
            self.videoManager.push()

            weaponPosition = self.getPosition() - annchienta.Vector( self.getWidth()/2, self.getHeight()/2 ) + self.hand - self.getWeapon().getGrip()
            self.videoManager.translate( weaponPosition.x, weaponPosition.y )
            self.videoManager.drawSurface( self.weapon.getSprite(), 0, 0 )

            self.videoManager.pop()
        
    def drawInfo( self, boxWidth, boxHeight ):

        self.videoManager.push()

        # Draw a hp bar
        self.videoManager.setColor( 0, 160, 0, 150 )
        width = int(boxWidth/2*float(self.getHp())/self.getMaxHp())
        self.videoManager.drawRectangle( 0, 2, width, boxHeight-2 )

        if self.isCritical():
            self.videoManager.setColor( 255, 0, 0 )
        else:
            self.videoManager.setColor()

        # Draw the combanant's name
        self.videoManager.drawString( self.sceneManager.getDefaultFont(), self.name.capitalize(), 0, 0 )

        self.videoManager.translate( int(boxWidth/4), 0 )

        self.videoManager.drawString( self.sceneManager.getDefaultFont(), str(self.getHp()) + "/" + str(self.getMaxHp()) + "HP", 0, 0 )

        self.videoManager.translate( int(boxWidth/2), 0 )

        self.videoManager.drawStringRight( self.sceneManager.getDefaultFont(), str(self.getMp()) + "MP ", 0, 0 )
        
        # Draw the timer
        if self.timer>=100.0:
            self.videoManager.setColor( 161, 48, 0, 150 )
        else:
            self.videoManager.setColor( 161, 120, 0, 150 )

        width = int( 0.01 * self.timer * (boxWidth/4.0) )
        self.videoManager.drawRectangle( 0, 2, width, boxHeight-2 )
        
        self.videoManager.setColor()
        self.videoManager.pop()

    def selectTarget( self, battle, selectEnemies = True ):

        done = False

        mouseSelected = False

        # select a first enemy (there should always be one,
        # because it's not victory or game over)
        targetIndex = 0
        if selectEnemies:
            target = battle.enemies[0]
        else:
            target = battle.allies[0]

        while not done:
            
            # Update
            battle.update( False )
            
            # Update input
            self.inputManager.update()
            
            # Keyboard actions
            if self.inputManager.keyTicked( annchienta.SDLK_DOWN ):
                self.audioManager.playSound( self.soundClickNeu )
                targetIndex += 1
                mouseSelected = False
            elif self.inputManager.keyTicked( annchienta.SDLK_UP ):
                self.audioManager.playSound( self.soundClickNeu )
                targetIndex -= 1
                mouseSelected = False
            elif self.inputManager.keyTicked( annchienta.SDLK_LEFT ) or self.inputManager.keyTicked( annchienta.SDLK_RIGHT ):
                self.audioManager.playSound( self.soundClickNeu )
                selectEnemies = not selectEnemies
                mouseSelected = False
            elif self.inputManager.isMouseMoved():
                # Find out hover target
                # Just have it point to the closest combatant.
                distance = 0
                oldTarget = target
                target = None
                for i in range(len(battle.combatants)):
                    
                    combatant = battle.combatants[i]

                    # Use Vectors to calculate distance between mouse and combatant c.
                    mouse = annchienta.Vector( self.inputManager.getMouseX(), self.inputManager.getMouseY() )
                    pos = annchienta.Vector( combatant.getPosition().x, combatant.getPosition().y )
                    d = mouse.distance( pos )

                    if d<distance or target is None:
                        target = combatant
                        targetIndex = i
                        distance = d
                if target != oldTarget:
                    self.audioManager.playSound( self.soundClickNeu )
                mouseSelected = True

            if not mouseSelected:
                if selectEnemies:
                    targetIndex = targetIndex % len(battle.enemies)
                    target = battle.enemies[targetIndex]
                else:
                    targetIndex = targetIndex % len(battle.allies)
                    target = battle.allies[targetIndex]

            # Set selected mark
            target.setSelected( True )
            
            # Check for input
            if not self.inputManager.isRunning() or self.inputManager.buttonTicked(1) or self.inputManager.cancelKeyTicked():
                target = None
                done = True
            if self.inputManager.buttonTicked(0) or self.inputManager.interactKeyTicked():
                done = True
            
            # Draw
            battle.videoManager.clear()
            battle.draw()
            
            # Draw "select target"
            self.sceneManager.activeColor()
            self.videoManager.drawString( self.sceneManager.getLargeItalicsFont(), "Select Target", self.sceneManager.getMargin(), 40 )
            
            battle.videoManager.flip()

            # Reset selected mark
            for c in battle.combatants:
                c.setSelected( False )

        return target

    def addXp( self, xp, showDialog=True ):

        # Start by adding the xp
        self.level["xp"] += xp

        # Function to determine next level xp
        xpNeeded = lambda lvl: int(lvl*75)

        # If the amount is reached... cap at 99
        while self.level["xp"] >= xpNeeded(self.level["lvl"]) and self.level["lvl"]<=99:
            
            # Use up xp to level
            self.level["xp"] -= xpNeeded(self.level["lvl"])
            # Increase level
            self.level["lvl"] += 1

            self.audioManager.playSound( self.soundLevelup )
            text = self.name.capitalize()+" gains a level!"

            for key in self.stats:

                grade = self.grades[key]

                # Determine baseline
                baseline = int( float(self.level["lvl"] * 2.5)/float(grade) )

                # Difference baseline - current value
                difference = baseline - self.stats[key]
                
                # Add a certain random factor
                gain = difference + self.mathManager.randInt(0,4)

                # Now gain
                self.stats[key] += gain

                # Cap at 100
                if self.stats[key] > 100:
                    self.stats[key] = 100

            # Seperate formulas for hp, mp
            for string in ["hp", "mp"]:
                mstring = "m"+string
                gain = int( float(self.grades[mstring]*self.mathManager.randFloat(0.9,1.1)) )
                self.healthStats[mstring] += gain
                self.healthStats[string] += gain

            # Check for new abilities
            if self.level["lvl"] in self.learn.keys():
                ability = self.learn[ self.level["lvl"] ]
                text += " Learned "+ability+"!"

                self.addAction( ability )

            if showDialog:
                self.sceneManager.text( text, None )

