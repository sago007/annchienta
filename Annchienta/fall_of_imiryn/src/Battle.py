import annchienta
import xml.dom.minidom
import SceneManager, PartyManager
import Enemy
import Animation
import DieAnimation
import AttackAnimation

## Holds a battle...
#
class Battle(object):

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
        self.actionLock = False
    
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
        if len(self.lines) >= 2:
            self.lines = [ self.lines[len(self.lines)-1] ]

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
        self.actionLock = False

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
            if combatant.getHp() <= 0 and not self.actionLock:

                # Add experience if we killed an enemy
                if not combatant.isAlly():
                    self.xp += combatant.getDropXp()
                    if combatant.dropItem:
                        if self.mathManager.randFloat() < combatant.getDropRate():
                            self.addLine( combatant.getName().capitalize()+" drops "+combatant.getDropItem()+"!" )
                            self.partyManager.getInventory().addItem( combatant.getDropItem() )

                            # Rebuild menus, because we might have gotten
                            # a new item we want to use.
                            for ally in self.allies:
                                ally.buildMenu()

                # Die die die!!!!11!!!!1
                self.actionLock = True

                animation = DieAnimation.DieAnimation( None, None )
                animation.setBattle( self )
                animation.setCombatant( combatant )
                animation.play()

                self.combatants.remove( combatant )

                self.actionLock = False

    ## Put the combatants in their appropriate list.
    #
    def updateCombatantLists( self ):
    
        # Sort combatant based on y (virtual z)
        self.combatants.sort( key = lambda combatant: combatant.getPosition().y )
        self.allies = filter( lambda q: q.isAlly(), self.combatants )
        self.enemies = filter( lambda q: not q.isAlly(), self.combatants )
    
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
                        ally.setHp( int(ally.getMaxHp()/7) )
            else:
                self.won = False
                self.sceneManager.gameOver()
                self.mapManager.stop()
            self.running = False
            return

    ## We have to be very careful in this function because it
    #  might very well recurse. That's why we need a lock to
    #  ensure some things are not executed in the same time,
    #  for example two animations or two open menu's.
    def update( self, updateInputManagerToo=True ):
    
        if updateInputManagerToo:
            self.inputManager.update()
        
        if not self.inputManager.isRunning() or not self.running:
            self.running = False
            return
        
        # Calculate number of ms passed
        ms = 0.0
        if self.lastUpdate is not None:
            ms = self.engine.getTicks() - self.lastUpdate
        
        self.lastUpdate = self.engine.getTicks()
        
        # Update combatants
        for combatant in self.combatants:
            combatant.update( ms )
            if combatant.getTimer() >= 100 and combatant not in self.actionQueue:
                self.actionQueue.append( combatant )
        
        # Check for dead combatants
        self.removeDeadCombatants()

        # Update lists
        self.updateCombatantLists()

        # Check if battle is finished
        self.checkBattleFinished()

        if self.running and len(self.actionQueue) and not self.actionLock:

            self.actionLock = True

            # Let combatant choose action and attack
            actor = self.actionQueue[ 0 ]

            if actor in self.combatants:

                # Note that we set him to 'selected', which will
                # cause it do draw an arrow above his head, so
                # the player can clearly see what's going on.
                if actor.isAlly():
                    actor.setActive(True)
                action, target = actor.selectAction( self )
                if actor.isAlly():
                    actor.setActive(False)

                # If the user cancelled, but the ally back of the queue
                if action is None:
                    self.actionQueue.append( actor )

                else:
                    # Validate a few things: actor should still be present, so does
                    # target.
                    # If this attack doesn't need a target or the target is alive.
                    if (not target or target in self.combatants) and (actor in self.combatants):
                        # Dependencies satisfied, take action
                        self.takeAction( action, actor, target )

            # Remove combatant from queue
            self.actionQueue.pop( 0 )

            self.actionLock = False
            
    ## Draws the battle to the screen.
    #
    def draw( self ):

        # Start with background
        self.videoManager.drawSurface( self.background, 0, 0 )

        # Draw the console and lines
        if len(self.lines):
            self.videoManager.setColor( 0, 0, 0, 100 )
            self.videoManager.drawRectangle( 0, 0, self.videoManager.getScreenWidth(), self.sceneManager.getMargin()*2+self.sceneManager.getDefaultFont().getLineHeight()*2 )
            self.sceneManager.inactiveColor()
            for i in range(len(self.lines))[:2]:
                self.videoManager.drawString( self.sceneManager.getDefaultFont(), self.lines[i], self.sceneManager.getMargin(), self.sceneManager.getMargin()+self.sceneManager.getDefaultFont().getLineHeight()*i )
            self.videoManager.setColor()
        
        # Draw the combatants
        for combatant in self.combatants:
            combatant.draw()
            
        # Draw the allies info
        self.videoManager.push()

        infoBoxWidth = 280
        infoBoxHeight = 20*len(self.allies)
        infoBoxX = self.videoManager.getScreenWidth() - infoBoxWidth - 3*self.sceneManager.getMargin()
        infoBoxY = self.videoManager.getScreenHeight() - infoBoxHeight - 3*self.sceneManager.getMargin()

        self.sceneManager.drawBox( infoBoxX, infoBoxY, infoBoxX + infoBoxWidth + 2*self.sceneManager.getMargin(), infoBoxY + infoBoxHeight + 2 * self.sceneManager.getMargin(), True )
        self.videoManager.translate( infoBoxX + self.sceneManager.getMargin(), infoBoxY + self.sceneManager.getMargin() )

        for ally in self.allies:
            ally.drawInfo( infoBoxWidth, 20 )
            self.videoManager.translate( 0, 20 )
        self.videoManager.pop()

    ## This function does nothing more than inspecting
    #  the action given, and then calling to the appropriate
    #  takeXAction function in this class.
    def takeAction( self, action, combatant, target ):

        combatant.setTimer( 0.0 )

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

        # When the attacker is critical, double damage
        if combatant.isCritical():
            damage *= 2
    
        if action.getType() == "physical":
            # If attacker is in back row, half damage...
            if combatant.getRow() == "back":
                damage /= 2
            # If target is in back row, half damage...
            if target.getRow() == "back":
                damage /= 2

            # We also have double damage on injured units,
            # and injured units do half damage
            if target.hasStatusEffect( "injured" ):
                damage *= 2
            if combatant.hasStatusEffect( "injured" ):
                damage /= 2

        # Our hit rate
        rate = action.getHit()
        # ... is influenced by blindness (but only on physical attacks)
        if action.getType() == "physical":
            if combatant.hasStatusEffect( "blinded" ):
                rate /= 2.0

        hit = ( self.mathManager.randFloat() <= rate )

        # Round the damage
        damage = int(damage)

        # Rows only matter when it's physical damage
        # Play animation
        animation = action.getAnimation()
        animation.setBattle( self )
        animation.setCombatant( combatant )
        animation.setTarget( target )
        animation.play()

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
        animation = AttackAnimation.AttackAnimation( None, None )
        animation.setBattle( self )
        animation.setCombatant( combatant )
        animation.setTarget( target )
        animation.play()

        # Allies have no item to be stolen
        if not target.isAlly():

            # Only if enemy is carrying an item
            if target.getStealableItem():
                if self.mathManager.randFloat()<=0.7:
                    self.addLine( combatant.getName().capitalize()+" stole "+target.getStealableItem()+" from "+target.getName().capitalize()+"!" )
                    self.partyManager.getInventory().addItem( target.getStealableItem() )
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
        self.partyManager.getInventory().useItemOn( item, target )

        # Rebuild item menus
        for ally in self.allies:
            ally.buildItemMenu()

    ## Switches back/front row with small animation
    #
    def takeRowAction( self, combatant ):

        oldPosition = annchienta.Vector( combatant.position )
        combatant.changeRow()
        newPosition = annchienta.Vector( combatant.position )

        # Rever and do a small animation
        combatant.setPosition( oldPosition )
        self.addLine( combatant.getName().capitalize()+" moves to the "+combatant.row+" row!" )

        animation = Animation.Animation( None, None )
        animation.setBattle( self )
        animation.setCombatant( combatant )
        animation.move( combatant, newPosition )

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
