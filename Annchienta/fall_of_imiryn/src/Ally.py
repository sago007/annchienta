import annchienta
import Combatant, Menu, Action
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
        return Combatant.Combatant.getAttack(self) + weapon.getAttack()

    def getDefense( self ):
        return Combatant.Combatant.getDefense(self) + weapon.getDefense()

    def getMagicAttack( self ):
        return Combatant.Combatant.getMagicAttack(self) + weapon.getMagicAttack()

    def getMagicDefense( self ):
        return Combatant.Combatant.getMagicDefense(self) + weapon.getMagicDefense()

    def getSpeed( self ):
        return Combatant.Combatant.getSpeed(self) + weapon.getSpeed()

    def getElementalFactor( self, element ):
        return weapon.getElementalFactor( element )

    def setWeapon( self, weaponName ):

        partyManager = PartyManager.getPartyManager()
        inventory = partyManager.inventory
        self.weapon = inventory.getWeapon( weaponName )

    ## Create a menu with all options this Ally
    #  can use in battle.
    def buildMenu( self ):
    
        self.menu = Menu.Menu( self.name, "Select an action." )
        subs = []
        for action in self.actions:

            # Create a decription first
            description = action.description
            if action.cost>0:
                description += " ("+str(action.cost)+"MP)"

            menuItem = Menu.MenuItem( action.name, description )
            added = False

            for sub in subs:
                if sub.name == action.category:
                    sub.options += [menuItem]
                    added = True
            if not added:
                if action.category=="top":
                    subs += [menuItem]
                else:
                    newsub = Menu.Menu( action.category )
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
        
        inv = self.partyManager.inventory
        loot = inv.getAvailableLoot()
        items = []
        for l in loot:
            items += [ Menu.MenuItem( l, inv.getItemDescription(l)+" ("+str(inv.getItemCount(l))+" left)" ) ]
        self.itemMenu.setOptions( items )
        self.itemMenu.leftBottom()

    ## Allies select an action from the menu. returns (action, target)
    def selectAction( self, battle ):

        menuItem = self.menu.pop( battle )
        if menuItem is None:
            return None, None

        found = filter( lambda a: a.name == menuItem.name, self.actions )

        needsTarget = True

        # We found an action
        if len(found):

            action = found[0]

            # Check if there is enough mp
            if self.getMp() < action.cost:
                battle.lines += [self.name.capitalize()+" doesn't have enough MP!"]
                return None, None
        
            if not action.target:
                needsTarget = False

        # No real action, check if it's an item
        elif self.partyManager.inventory.hasItem( menuItem.name ):

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
        
    def drawInfo( self ):
    
        self.videoManager.push()

        # Draw a quick black background
        self.videoManager.setColor( 0, 0, 0, 100 )
        self.videoManager.drawRectangle( 0, 0, self.videoManager.getScreenWidth(), 20 )        
        
        # Draw the timer
        self.videoManager.push()
        if self.timer>=100.0:
            self.videoManager.setColor( 161, 48, 0 )
        else:
            self.videoManager.setColor( 161, 120, 0 )
        self.videoManager.translate( self.videoManager.getScreenWidth()*0.4 + 3, 3 )
        width = int(0.01*self.timer*(self.videoManager.getScreenWidth()*0.6-6))
        self.videoManager.drawRectangle( 0, 0, width, 14 )
        self.videoManager.pop()
        
        # Draw the combatant's name
        self.videoManager.setColor()
        self.videoManager.drawString( self.sceneManager.largeItalicsFont, self.name.capitalize(), self.sceneManager.margin, -3 )
        
        # Draw the combatant's hp
        self.videoManager.drawString( self.sceneManager.largeItalicsFont, str(self.getHp())+"/"+str(self.getMaxHp())+"HP", int(self.videoManager.getScreenWidth()*0.4)+self.sceneManager.margin, -3 )
        
        # Draw the combatant's mp
        self.videoManager.drawStringRight( self.sceneManager.largeItalicsFont, str(self.getMp())+"MP", self.videoManager.getScreenWidth()-self.sceneManager.margin, -3 )
        
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
                pos = annchienta.Vector( c.position.x, c.position.y )

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
            self.videoManager.drawString( self.sceneManager.largeItalicsFont, "Select Target", self.sceneManager.margin, self.videoManager.getScreenHeight()-20*(len(battle.allies)+1) )
            
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

            for key in self.primaryStats:

                grade = self.grades[key]

                # Determine baseline
                baseline = int( float(self.level["lvl"] * 2.5)/float(grade) )

                # Difference baseline - current value
                difference = baseline - self.primaryStats[key]
                
                # Add a certain random factor
                gain = difference + self.mathManager.randInt(0,4)

                # Now gain
                self.primaryStats[key] += gain

                # Cap at 100
                if self.primaryStats[key] > 100:
                    self.primaryStats[key] = 100

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

