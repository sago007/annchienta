import annchienta
import xml.dom.minidom
import SceneManager, PartyManager
import Enemy

## Holds a battle...
#
class Battle:

    ## Constructor for a battle class.
    #  \param combatants Combatants to participate in the battle.
    #  \param background A Surface to be used as background.
    #  \param canFlee If the party can escape this battle.
    def __init__( self, combatants, background, canFlee ):
    
        # Set variables
        self.combatants = combatants
        self.running = True
        self.background = background
        self.canFlee = canFlee
        self.won = False
    
        # Get references
        self.engine = annchienta.getEngine()
        self.videoManager = annchienta.getVideoManager()
        self.inputManager = annchienta.getInputManager()
        self.cacheManager = annchienta.getCacheManager()
        self.mathManager  = annchienta.getMathManager()
        self.mapManager   = annchienta.getMapManager()
        self.audioManager = annchienta.getAudioManager()
        self.sceneManager = SceneManager.getSceneManager()
        self.partyManager = PartyManager.getPartyManager()
        
        # Lines for the 'console' window
        self.lines = []
        
    def addLine( self, line ):

        # Remove previous line
        if len(self.lines) > 2:
            self.lines = self.lines[ len(self.lines)-2 : ]

        self.lines.append( line )
        
    ## Starts and runs the battle.
    #
    def run( self ):
    
        # Update the lists
        self.updateCombatantLists()
        self.positionCombatants()
    
        # Reset combatants
        for c in self.combatants:
            c.reset()
    
        self.lastUpdate = None
        
        # If there is currently a menu open
        self.menuOpen = False
    
        # Reset action que [ (action, combatant, target) ]
        self.actionQueue = []
        self.actionInProgress = False

        # Total experience earned in this battle
        self.xp = 0

        # Preemptive strike / ambush
        if self.mathManager.randFloat() <= 0.1:
            for ally in self.allies:
                ally.setTimer( 100.0 )
            self.addLine( "Preemptive strike!"  )
        elif self.mathManager.randFloat() <= 0.1:
            for ally in self.allies:
                ally.setTimer( 0.0 )
            self.addLine( "Ambushed!" )
            

        while self.running:
        
            self.update()
            
            self.videoManager.clear()
            self.draw()
            self.videoManager.flip()
    
        self.mapManager.resync()

    ## Cleans up the battle by removing dead
    #  combatants. This also calculates the experience
    #  and such when someone dies.
    #
    def removeDeadCombatants( self ):

        for combatant in self.combatants:

            # Check if the target died
            if combatant.getHp() <= 0 and not self.actionInProgress:

                # Add experience if we killed an enemy
                if not combatant.isAlly():
                    self.xp += combatant.getDropXp()
                    if combatant.dropItem:
                        if self.mathManager.randFloat() < combatant.getDropRate():
                            self.addLine( combatant.getName().capitalize()+" drops "+combatant.getDropItem()+"!" )
                            self.partyManager.inventory.addItem( combatant.getDromItem() )

                            # Rebuild menus, because we might have gotten
                            # a new item we want to use.
                            for ally in self.allies:
                                ally.buildMenu()

                # Die die die!!!!11!!!!1
                self.actionInProgress = True
                self.playDieAnimation( combatant )

                self.combatants.remove( combatant )

                self.actionInProgress = False

    ## Calculate the combatants who are ready
    #
    def updateCombatantLists( self ):
    
        # Sort combatant based on y (virtual z)
        self.combatants.sort( lambda c1, c2: int( c1.getPosition().y - c2.getPosition().y ) )

        self.allies = filter( lambda q: q.isAlly(), self.combatants )
        self.enemies = filter( lambda q: not q.isAlly(), self.combatants )
        self.readyEnemies = filter( lambda q: q.getTimer() >= 100.0, self.enemies )
        self.readyAllies = filter( lambda q: q.getTimer() >= 100.0, self.allies )
    
    ## Set all combatants to a good position
    #  on the screen.
    def positionCombatants( self ):
    
        # Align them and stuff
        for i in range(len(self.allies)):
            self.allies[i].setPosition( annchienta.Vector( 120-20*i, 75+(i+1)*30 ) )
            
        for i in range(len(self.enemies)):
            self.enemies[i].setPosition( annchienta.Vector( self.videoManager.getScreenWidth()-120+20*i, 75+(i+1)*30 ) )
    
    ## Check if we won or if the battle is over
    #
    def checkBattleFinished( self ):

        # Are all enemies dead? 'cause we win if they are
        # Then again, are we dead?
        if not len(self.enemies) or not len(self.allies):
            if len(self.allies):
                # We won!
                self.won = True
                self.sceneManager.text("Victorious! Gained "+str(self.xp)+" xp!", None)
                for ally in self.allies:
                    ally.addXp( self.xp )
                # Revive dead combatants
                for ally in self.partyManager.team:
                    if ally.getHp() <= 1:
                        ally.setHp( ally.getMaxHp()/7 )
            else:
                self.won = False
                self.sceneManager.gameOver()
                self.mapManager.stop()
            self.running = False
            return

    ## We have to be very careful in this function because it
    #  might very well recurse. That's why we need booleans to
    #  ensure some things are not executed in the same time,
    #  for example two animations or two open menu's.
    def update( self, updateInputManagerToo=True ):
    
        if updateInputManagerToo:
            self.inputManager.update()
        
        if not self.inputManager.running() or not self.running:
            self.running = False
            return
        
        # Calculate number of ms passed
        ms = 0.0
        if self.lastUpdate is not None:
            ms = self.engine.getTicks() - self.lastUpdate
        
        self.lastUpdate = self.engine.getTicks()
        
        # Update combatants
        for c in self.combatants:
            c.update( ms )
        
        # Check for dead combatants
        self.removeDeadCombatants()

        # Update lists
        self.updateCombatantLists()

        # Check if battle is finished
        self.checkBattleFinished()
        
        # Update actionqueue
        while self.running and len(self.actionQueue) and not self.actionInProgress and not self.menuOpen:

            self.actionInProgress = True
            action, actor, target = self.actionQueue.pop()
            # Check if the target and actor still exist
            if actor in self.combatants:
                # If this attack doesn't need a target or the target is alive.
                if (not target or target in self.combatants) and (actor in self.combatants):
                    self.takeAction( action, actor, target )
            self.actionInProgress = False

            self.removeDeadCombatants()
            self.updateCombatantLists()
            self.checkBattleFinished()

        # Let allies choose actions
        if self.running and (not self.menuOpen) and len(self.readyAllies) and not self.actionInProgress:
            self.menuOpen = True
            actor = self.readyAllies.pop(0)
            action, target = actor.selectAction( self )
            if action is None:
                # Put this ready ally in the back
                self.readyAllies += [actor]
            else:
                # First in first out
                self.actionQueue = self.actionQueue + [ (action, actor, target ) ]
                # Make sure to reset time
                actor.setTimer( 0.0 )
            self.menuOpen = False
        
        # Let enemies choose actions
        if self.running and len(self.readyEnemies) and not self.actionInProgress:
            actor = self.readyEnemies.pop(0)
            action, target = actor.selectAction( self )
            # An enemy can't queue twice, so check if the enemy isn't there already.
            if not len( filter( lambda a: a[1]==actor, self.actionQueue ) ):
                # First in first out
                self.actionQueue = [ (action, actor, target) ] + self.actionQueue
                # Make sure to reset timer
                actor.setTimer( 0.0 )

    ## Draws the battle to the screen.
    #
    def draw( self ):

        # Start with background
        self.videoManager.drawSurface( self.background, 0, 0 )

        # Draw the console and lines
        if len(self.lines):
            self.videoManager.setColor( 0, 0, 0, 100 )
            self.videoManager.drawRectangle( 0, 0, self.videoManager.getScreenWidth(), self.sceneManager.margin*2+self.sceneManager.defaultFont.getLineHeight()*2 )
            self.sceneManager.inactiveColor()
            for i in range(len(self.lines))[:2]:
                self.videoManager.drawString( self.sceneManager.defaultFont, self.lines[i], self.sceneManager.margin, self.sceneManager.margin+self.sceneManager.defaultFont.getLineHeight()*i )
            self.videoManager.setColor()
        
        # Draw the combatants
        for combatant in self.combatants:
            combatant.draw()
            
        # Draw the allies info
        self.videoManager.push()
        self.videoManager.translate( 0, self.videoManager.getScreenHeight()-20*len(self.allies) )
        for a in self.allies:
            a.drawInfo()
            self.videoManager.translate( 0, 20 )
        self.videoManager.pop()

    ## This function does nothing more than inspecting
    #  the action given, and then calling to the appropriate
    #  takeXAction function in this class.
    def takeAction( self, action, combatant, target ):

        if action.getCategory() == "item":
            self.takeItemAction( action.getName(), combatant, target )
        elif action.getName() == "steal":
            self.takeStealAction( combatant, target )
        elif action.getName() == "row":
            self.takeRowAction( combatant )
        elif action.getName() == "flee":
            self.takeFleeAction( combatant )
        elif action.getName() == "esuna":
            self.takeEsunaAction( combatant, target )
        elif action.getName() == "wait":
            self.takeWaitAction( combatant )
        else:
            # If we reach this point, we're dealing with a generic action.
            self.takeGenericAction( action, combatant, target )

    ## Make a combatant do a generic action
    #
    def takeGenericAction( self, action, combatant, target ):
            
        # Info
        self.addLine( combatant.getName().capitalize()+" uses "+action.getName()+" on "+target.getName().capitalize()+"!" )
        
        # Let's assume we are dealing with a regular action for now
        damage = 0.0
        if action.getType() == "physical":
            damage = combatant.physicalBaseDamage()
        else:
            damage = combatant.magicalBaseDamage()
            
        # Invert damage if we are dealing with restorative magic
        if action.hasElement("restorative"):
            damage = -float(damage)
            
        # Take the power of the attack into account
        damage *= action.getFactor()
        
        # Take the target's defense into account
        defense = target.getDefense() if action.getType() == "physical" else target.getMagicDefense()
        damage *= ( (512.0 - defense )/512.0 )
    
        # Elemental properties now
        for element in action.getElementList():
            if element != "restorative":
                # Multiply damage by the factor the
                # target has set for it
                damage *= target.getElementalFactor( element )
    
        # Round it
        damage = int(damage)

        # Rows only matter when it's physical damage
        if action.getType() == "physical":
            # If attacker is in back row, half damage...
            if combatant.getRow() == "back":
                damage /= 2
            # If target is in back row, half damage...
            if target.getRow() == "back":
                damage /= 2

        # Our hit rate
        rate = action.getHit()
        # ... is influenced by blindness (but only on physical attacks)
        if action.getType() == "physical":
            if combatant.hasStatusEffect( "blinded" ):
                rate /= 2.0

            # We also have double damage on injured units.
            if combatant.hasStatusEffect( "injured" ):
                damage *= 2

        hit = ( self.mathManager.randFloat() <= rate )

        # Play animation
        self.playAnimation( action, combatant, target )

        if hit:
            # Check for status effects
            if action.getStatusEffect()!="none" and not target.hasStatusEffect( action.getStatusEffect() ):
                if self.mathManager.randFloat() <= action.getStatusHit():
                    target.addStatusEffect( action.getStatusEffect() )
                    self.addLine( target.getName().capitalize()+" is now "+action.getStatusEffect()+"!" )

            # Finally, do damage to damaged ones
            target.setHp( target.getHp() - damage )

        else:
            self.addLine( combatant.getName().capitalize()+" misses!" )

        # That took some effort, rest and get mp
        combatant.setMp( combatant.getMp() - action.getCost() )

        # Damage animation only if hit
        if hit:
            target.setDamage( damage )

    ## Might steal an item
    #
    def takeStealAction( self, combatant, target ):

        # Play a quick animation
        self.playAttackAnimation( combatant, target )

        # Allies have no item to be stolen
        if not target.isAlly():

            # Only if enemy is carrying an item
            if target.getStealableItem():
                if self.mathManager.randFloat()<=0.7:
                    self.addLine( combatant.getName().capitalize()+" stole "+target.getStealableItem()+" from "+target.getName().capitalize()+"!" )
                    self.partyManager.inventory.addItem( target.getStealableItem() )
                    # Remove item from target when stolen
                    target.stealItem()

                    # Rebuild item menus
                    for ally in self.allies:
                        ally.buildItemMenu()

                else:
                    self.addLine( combatant.getName().capitalize()+" could not steal from "+target.getName().capitalize()+"!" )
            else:
                self.addLine( target.getName().capitalize()+" has nothing to steal!" )

    ## Uses an item
    #
    def takeItemAction( self, item, combatant, target ):
        
        self.addLine( combatant.getName().capitalize()+" uses "+item+" on "+target.getName().capitalize()+"!" )
        self.partyManager.inventory.useItemOn( item, target )

        # Rebuild item menus
        for ally in self.allies:
            ally.buildItemMenu()

    ## Switches back/front row with small animation
    #
    def takeRowAction( self, combatant ):

        oldPosition = annchienta.Vector( combatant.position )
        combatant.changeRow()
        newPosition = annchienta.Vector( combatant.position )

        combatant.position = oldPosition
        self.addLine( combatant.getName().capitalize()+" moves to the "+combatant.row+" row!" )
        self.playMoveAnimation( combatant, newPosition )

    ## Tries to flee from battle
    #
    def takeFleeAction( self, combatant ):

        if not self.canFlee:
            self.addLine( "You cannot flee from this battle!" )
            return

        # 75% chance to run away
        if self.mathManager.randFloat() < 0.75:
            self.running = False

        else:
            self.addLine( "Couldn't run away!" )

    ## Removes a status effect from a target.
    #
    def takeEsunaAction( self, combatant, target ):
        
        removedStatusEffect = target.removeStatusEffect()

        if not removedStatusEffect:
            self.addLine( target.getName().capitalize()+" is not suffering from status effects!" )

        else:
            self.addLine( combatant.getName().capitalize()+" cures "+target.getName().capitalize()+" from "+removedStatusEffect+"!" )

    ## Does nothing, really
    #
    def takeWaitAction( self, combatant ):

        # Speed up a little
        combatant.timer = 50.0

    ## Plays the animation for the given parameters
    #  This calls to playXAnimation, where X depends on the action
    def playAnimation( self, action, combatant, target ):

        if action.animation == "attack":
            self.playAttackAnimation( combatant, target, action.animationData, action.animationSound )
        elif action.animation == "sprite":
            self.playSpriteAnimation( target, action.animationData, action.animationSound )

    ## Animation that moves the given combatant to
    #  the given position
    def playMoveAnimation( self, combatant, position, duration=400.0 ):

        start = self.engine.getTicks()
        origPosition = annchienta.Vector(combatant.position)
        while self.inputManager.running() and self.engine.getTicks()<start+duration:
            
            self.update()

            factor = float(self.engine.getTicks()-start)/duration
            combatant.position = origPosition*(1.0-factor) + position*factor

            self.videoManager.clear()
            self.draw()
            self.videoManager.flip()

        # Make sure we're in the right position in the end.
        combatant.position = annchienta.Vector( position )

    ## Moves the combatant to the target and back again
    #
    def playAttackAnimation( self, combatant, target, optionalSprite=None, animationSound=None ):

        origPosition = annchienta.Vector( combatant.position )
        position = annchienta.Vector( target.position )
        dx = ( target.width/2 + combatant.width/2 )
        dx = dx if target.isAlly() else -dx
        position.x += dx
        self.playMoveAnimation( combatant, position )

        if animationSound:
            sound = self.cacheManager.getSound( animationSound )
            self.audioManager.playSound( sound )

        if optionalSprite:
            self.playSpriteAnimation( target, optionalSprite )

        self.playMoveAnimation( combatant, origPosition )

    ## Scrolls a sprite over the combatant. Very useful
    #  for magic-kinda attacks.
    def playSpriteAnimation( self, combatant, sprite, animationSound=None, duration=800.0 ):

        if animationSound:
            sound = self.cacheManager.getSound( animationSound )
            self.audioManager.playSound( sound )

        start = self.engine.getTicks()
        surf = self.cacheManager.getSurface( sprite )

        while self.inputManager.running() and self.engine.getTicks()<start+duration:
            
            self.update()

            factor = float(self.engine.getTicks()-start)/duration
            position = combatant.position + annchienta.Vector(0,-30)*factor

            self.videoManager.clear()
            self.draw()
            self.videoManager.drawSurface( surf, int(position.x)-surf.getWidth()/2, int(position.y)-surf.getHeight()/2 )
            self.videoManager.flip()

    ## Make combatant move away from battle centre
    #  and die.
    def playDieAnimation( self, combatant ):

        position = annchienta.Vector( combatant.position )
        position.x -= 30 if combatant.isAlly() else -30
        self.playMoveAnimation( combatant, position )

