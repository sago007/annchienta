import annchienta
import Combatant, MenuItem, Menu, Action
import PartyManager

class Ally( Combatant.Combatant ):

    def __init__( self, xmlElement ):
        
        # Base constructor
        Combatant.Combatant.__init__( self, xmlElement )
        
        # References
        self.partyManager = PartyManager.getPartyManager()
        self.logManager   = annchienta.getLogManager()
    
        # Get our weapon
        weaponElements = xmlElement.getElementsByTagName("weapon")
        if len(weaponElements):
            # Get the weapon name and search for the corresponding element
            weaponName = str(weaponElements[0].getAttribute("name"))
            self.setWeapon( weaponName )
        else:
            self.logManager.warning( "No Weapon defined for Ally!" )
    
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
        for i in range( len(words)/2 ):
            self.learn[ int( words[i*2] ) ] = words[i*2+1]

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

        menuItem = self.menu.pop( battle )
        if menuItem is None:
            return None, None

        found = filter( lambda action: action.getName() == menuItem.getName(), self.actions )

        needsTarget = True

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
            target = self.selectTarget( battle )
            if target is None:
                return None, None

        return action, target
        
    def drawInfo( self, boxWidth, boxHeight ):

        self.videoManager.push()

        if self.getHp() > self.getMaxHp()*0.15:
            self.videoManager.setColor()
        else:
            self.videoManager.setColor( 255, 0, 0 )

        # Draw the combanant's name
        self.videoManager.drawString( self.sceneManager.getDefaultFont(), self.name.capitalize(), 0, 0 )

        self.videoManager.translate( boxWidth/4, 0 )

        # Draw the combatant's hp and mp
        self.videoManager.drawString( self.sceneManager.getDefaultFont(), str(self.getHp()) + "/" + str(self.getMaxHp()) + "HP", 0, 0 )

        self.videoManager.translate( boxWidth/2, 0 )

        self.videoManager.drawStringRight( self.sceneManager.getDefaultFont(), str(self.getMp()) + "MP ", 0, 0 )
        
        # Draw the timer
        if self.timer>=100.0:
            self.videoManager.setColor( 161, 48, 0 )
        else:
            self.videoManager.setColor( 161, 120, 0 )

        width = int( 0.01 * self.timer * (boxWidth/4.0) )
        self.videoManager.drawRectangle( 0, 2, width, boxHeight-2 )
        
        self.videoManager.setColor()
        self.videoManager.pop()

    def selectTarget( self, battle ):

        done = False
        target = None
        while not done:
            
            # Update
            battle.update( False )
            
            # Update input
            battle.inputManager.update()
            
            target = None
            
            # Find out hover target
            # Just have it point to the closest combatant.
            distance = 0
            for c in battle.combatants:
                
                # Use Vectors to calculate distance between mouse and combatant c.
                mouse = annchienta.Vector( battle.inputManager.getMouseX(), battle.inputManager.getMouseY() )
                pos = annchienta.Vector( c.getPosition().x, c.getPosition().y )

                d = mouse.distance( pos )

                if d<distance or target is None:
                    target = c
                    distance = d

            target.marked = True
            
            # Check for input
            if not battle.inputManager.running() or battle.inputManager.buttonTicked(1):
                target = None
                done = True
            if battle.inputManager.buttonTicked(0):
                done = True
            
            # Draw
            battle.videoManager.clear()
            battle.draw()
            
            # Draw "select target"
            self.sceneManager.activeColor()
            self.videoManager.drawString( self.sceneManager.largeItalicsFont, "Select Target", self.sceneManager.margin, 40 )
            
            battle.videoManager.flip()

            # Reset marked
            for c in battle.combatants:
                c.marked = False

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
                self.buildMenu()

            if showDialog:
                self.sceneManager.text( text, None )

