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
        
    ## Starts and runs the battle.
    #
    def run( self ):
    
        # Reset combatants
        for c in self.combatants:
            c.reset()
    
        # Update the lists
        self.updateCombatantLists()
        self.positionCombatants()
    
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
            for a in self.allies:
                a.timer = 100.0
            self.lines += ["Preemptive strike!"]
        elif self.mathManager.randFloat() <= 0.1:
            for a in self.allies:
                a.timer = 0.0
            self.lines += ["Ambushed!"]
            

        while self.running:
        
            self.update()
            
            self.videoManager.begin()
            self.draw()
            self.videoManager.end()
    
        self.mapManager.resync()

    ## Cleans up the battle by removing dead
    #  combatants. This also calculates the experience
    #  and such when someone dies.
    def removeDeadCombatants( self ):

        for combatant in self.combatants:

            # Check if the target died
            if combatant.healthStats["hp"] <= 0 and not self.actionInProgress:

                # Add experience if we killed an enemy
                if not combatant.ally:
                    self.xp += combatant.dropXp
                    if combatant.dropItem:
                        if self.mathManager.randFloat() < combatant.dropRate:
                            self.lines += [ combatant.name.capitalize()+" drops "+combatant.dropItem+"!" ]
                            self.partyManager.inventory.addItem( combatant.dropItem )

                            # Rebuild menus
                            for a in self.allies:
                                a.buildMenu()

                # Die die die!!!!11!!!!1
                self.actionInProgress = True
                self.playDieAnimation( combatant )

                self.combatants.remove( combatant )

                self.actionInProgress = False

    ## Calculate the combatants who are ready
    #
    def updateCombatantLists( self ):
    
        # Sort combatant based on y (virtual z)
        self.combatants.sort( lambda c1, c2: int(c1.position.y - c2.position.y) )

        self.allies = filter( lambda q: q.ally, self.combatants )
        self.enemies = filter( lambda q: not q.ally, self.combatants )
        self.readyEnemies = filter( lambda q: q.timer >= 100.0, self.enemies )
        self.readyAllies = filter( lambda q: q.timer >= 100.0, self.allies )
    
    ## Set all combatants to a good position
    #  on the screen.
    def positionCombatants( self ):
    
        # Align them and stuff
        for i in range(len(self.allies)):
            self.allies[i].position = annchienta.Vector( 100, 50+(i+1)*35 )
            
        for i in range(len(self.enemies)):
            self.enemies[i].position = annchienta.Vector( self.videoManager.getScreenWidth()-100, 50+(i+1)*35 )
    
    ## We have to be very careful in this function because it
    #  might very well recurse. That's why we need booleans to
    #  ensure some things are not executed in the same time,
    #  for example two animations or two open menu's.
    def update( self, updateInputManagerToo=True ):
    
        if updateInputManagerToo:
            self.inputManager.update()
        
        if not self.inputManager.running():
            self.running = False
            return
        
        # Remove unnecessary lines
        while len(self.lines)>2:
            self.lines.pop(0)
        
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
                    if ally.healthStats["hp"] <= 1:
                        ally.addHp( ally.healthStats["mhp"]/7 )
            else:
                self.won = False
                self.sceneManager.gameOver()
                self.mapManager.stop()
            self.running = False
            return

        # Let allies take actions
        if (not self.menuOpen) and len(self.readyAllies) and not self.actionInProgress:
            self.menuOpen = True
            actor = self.readyAllies.pop(0)
            action, target = actor.selectAction( self )
            if action is None:
                # Put this ready ally in the back
                self.readyAllies += [actor]
            else:
                self.actionQueue += [ (action, actor, target) ]
                # Make sure to reset time
                actor.timer = 0.0
            self.menuOpen = False
        
        # Let enemies take actions
        if len(self.readyEnemies):
            actor = self.readyEnemies.pop(0)
            action, target = actor.selectAction( self )
            # An enemy can't queue twice, so check if the enemy isn't there already.
            if not len( filter( lambda a: a[1]==actor, self.actionQueue ) ):
                self.actionQueue += [ (action, actor, target) ]
                # Make sure to reset timer
                actor.timer = 0.0

        # Update actionqueue
        if len(self.actionQueue) and not self.actionInProgress and not self.menuOpen:
            self.actionInProgress = True
            action, actor, target = self.actionQueue.pop()
            # Check if the target and actor still exist
            if actor in self.combatants:
                # If this attack doesn't need a target or the target is alive.
                if not target or target in self.combatants:
                    self.takeAction( action, actor, target )
            self.actionInProgress = False

    ## Draws the battle to the screen.
    #
    def draw( self ):

        # Start with background
        self.videoManager.drawSurface( self.background, 0, 0 )

        # Draw the console and lines
        self.videoManager.setColor( 0, 0, 0, 100 )
        self.videoManager.drawRectangle( 0, 0, self.videoManager.getScreenWidth(), self.sceneManager.margin*2+self.sceneManager.defaultFont.getLineHeight()*2 )
        self.sceneManager.inactiveColor()
        for i in range(len(self.lines))[:2]:
            self.videoManager.drawString( self.sceneManager.defaultFont, self.lines[i], self.sceneManager.margin, self.sceneManager.margin+self.sceneManager.defaultFont.getLineHeight()*i )
        self.videoManager.setColor()
        
        # Draw the combatants
        for c in self.combatants:
            c.draw()
            
        # Draw the allies info
        self.videoManager.pushMatrix()
        self.videoManager.translate( 0, self.videoManager.getScreenHeight()-20*len(self.allies) )
        for a in self.allies:
            a.drawInfo()
            self.videoManager.translate( 0, 20 )
        self.videoManager.popMatrix()

    # Takes any action, might call to takeXAction
    def takeAction( self, action, combatant, target ):

        # If the action is a string...
        if type(action) == type("string"):
            # And is an item...
            if self.partyManager.inventory.hasItem( action ):
                self.takeItemAction( action, combatant, target )
                return

        # First check for special actions
        if action.name == "steal":
            self.takeStealAction( combatant, target )
            return
        if action.name == "row":
            self.takeRowAction( combatant )
            return
        if action.name == "flee":
            self.takeFleeAction( combatant )
            return
        if action.name == "esuna":
            self.takeEsunaAction( combatant, target )
            return

        # If we reach this point, we're dealing with a generic action.
        self.takeGenericAction( action, combatant, target )



    ## Make an combatant do an action
    #
    def takeGenericAction( self, action, combatant, target ):
            
        # Info
        self.lines += [combatant.name.capitalize()+" uses "+action.name+" on "+target.name.capitalize()+"!"]
        
        # Let's assume we are dealing with a regular action for now
        baseDamage = 0.0
        if action.type == "physical":
            baseDamage = combatant.physicalBaseDamage()
        else:
            baseDamage = combatant.magicalBaseDamage()
            
        # Invert damage if we are dealing with restorative magic
        if action.elemental["restorative"]:
            baseDamage = -float(baseDamage)
            
        # Take the power of the attack into account
        baseDamage *= action.factor
        
        # Take the target's defense into account
        defense = target.derivedStats[ "def" if action.type == "physical" else "mdf" ]
        baseDamage *= ( (512.0 - target.derivedStats["def"])/512.0 )
    
        # Elemental properties now
        for element in action.elemental:
            if element != "restorative":
                # For example, if the action has "ice":1
                if action.elemental[element]:
                    # Multiply damage by the factor the
                    # target has set for it
                    baseDamage *= target.derivedElemental[element]
    
        # Round it
        baseDamage = int(baseDamage)

        # Rows only matter when it's physical damage
        if action.type == "physical":
            # If attacker is in back row, half damage...
            if combatant.row == "back":
                baseDamage /= 2
            # If target is in back row, half damage...
            if target.row == "back":
                baseDamage /= 2

        # Our hit rate
        rate = action.hit
        # ... is influenced by blindness (but only on physical attacks)
        if action.type == "physical":
            if "blinded" in combatant.statusEffects:
                rate /= 2.0

            # We also have double damage on injured units.
            if "injured" in combatant.statusEffects:
                baseDamage *= 2

        hit = self.mathManager.randFloat() <= rate

        # Play animation
        self.playAnimation( action, combatant, target )

        if hit:
            # Check for status effects
            if action.statusEffect!="none" and action.statusEffect not in target.statusEffects:
                if self.mathManager.randFloat() <= action.statusHit:
                    target.statusEffects += [action.statusEffect]
                    self.lines += [ target.name.capitalize()+" is now "+action.statusEffect+"!" ]

            # Finally, do damage to damaged ones
            target.addHp( -baseDamage )

        else:
            self.lines += [ combatant.name.capitalize()+" misses!" ]

        # That took some effort, rest and get mp
        combatant.healthStats["mp"] -= action.cost

        # Damage animation only if hit
        if hit:
            target.damage = baseDamage
            target.damageTimer = 0.0

    # Might steal an item
    def takeStealAction( self, combatant, target ):

        # Play a quick animation
        self.playAttackAnimation( combatant, target )

        # Allies have no item to be stolen
        if not target.ally:

            # Only if enemy is carrying an item
            if target.steal:
                if self.mathManager.randFloat()<=0.7:
                    self.lines += [ combatant.name.capitalize()+" stole "+target.steal+" from "+target.name.capitalize()+"!" ]
                    self.partyManager.inventory.addItem( target.steal )
                    # Remove item from target when stolen
                    target.steal = None

                    # Rebuild item menus
                    for ally in self.allies:
                        ally.buildItemMenu()

                else:
                    self.lines += [ combatant.name.capitalize()+" could not steal from "+target.name.capitalize()+"!" ]
            else:
                self.lines += [ target.name.capitalize()+" has nothing to steal!" ]

    # Uses an item
    def takeItemAction( self, item, combatant, target ):
        
        self.lines += [ combatant.name.capitalize()+" uses "+item+" on "+target.name.capitalize()+"!" ]
        self.partyManager.inventory.useItemOn( item, target )

        # Rebuild item menus
        for ally in self.allies:
            ally.buildItemMenu()

    # Switches back/front row with small animation
    def takeRowAction( self, combatant ):

        rowDeltaX = 30
        position = annchienta.Vector( combatant.position )
        if combatant.row == "front":
            combatant.row = "back"
            position.x += -rowDeltaX if combatant.ally else rowDeltaX
        else:
            combatant.row = "front"
            position.x += rowDeltaX if combatant.ally else -rowDeltaX
        self.lines += [combatant.name.capitalize()+" moves to the "+combatant.row+" row!"]
        self.playMoveAnimation( combatant, position )

    # Tries to flee from battle
    def takeFleeAction( self, combatant ):

        if not self.canFlee:
            self.lines += ["You cannot flee from this battle!"]
            return

        # 0.6% chance to run away
        if self.mathManager.randFloat() < 0.6:
            self.running = False

        else:
            self.lines += ["Couldn't run away!"]

    # Removes a status effect from a target.
    def takeEsunaAction( self, combatant, target ):
        
        if not len(target.statusEffects):
            self.lines += [target.name.capitalize()+" is not suffering from status effects!"]
            return

        effect = target.statusEffects[ self.mathManager.randInt( 0, len(target.statusEffects) ) ]
        self.lines += [combatant.name.capitalize()+" cures "+target.name.capitalize()+" from "+effect+"!"]
        target.statusEffects.remove( effect )

    # Plays the animation for the given parameters
    # This calls to playXAnimation, where X depends on the action
    def playAnimation( self, action, combatant, target ):

        if action.animation == "attack":
            self.playAttackAnimation( combatant, target, action.animationData, action.animationSound )
        elif action.animation == "sprite":
            self.playSpriteAnimation( target, action.animationData, action.animationSound )

    # Animation that moves the given combatant to
    # the given position
    def playMoveAnimation( self, combatant, position, duration=400.0 ):

        start = self.engine.getTicks()
        origPosition = annchienta.Vector(combatant.position)
        while self.inputManager.running() and self.engine.getTicks()<start+duration:
            
            self.update()

            factor = float(self.engine.getTicks()-start)/duration
            combatant.position = origPosition*(1.0-factor) + position*factor

            self.videoManager.begin()
            self.draw()
            self.videoManager.end()

        # Make sure we're in the right position in the end.
        combatant.position = annchienta.Vector( position )

    # Moves the combatant to the target and back again
    def playAttackAnimation( self, combatant, target, optionalSprite=None, animationSound=None ):

        origPosition = annchienta.Vector( combatant.position )
        position = annchienta.Vector( target.position )
        dx = ( target.width/2 + combatant.width/2 )
        dx = dx if target.ally else -dx
        position.x += dx
        self.playMoveAnimation( combatant, position )

        if animationSound:
            sound = self.cacheManager.getSound( animationSound )
            self.audioManager.playSound( sound )

        if optionalSprite:
            self.playSpriteAnimation( target, optionalSprite )

        self.playMoveAnimation( combatant, origPosition )

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

            self.videoManager.begin()
            self.draw()
            self.videoManager.drawSurface( surf, int(position.x)-surf.getWidth()/2, int(position.y)-surf.getHeight()/2 )
            self.videoManager.end()

    # Make combatant move away from battle centre
    def playDieAnimation( self, combatant ):

        position = annchienta.Vector( combatant.position )
        position.x -= 30 if combatant.ally else -30
        self.playMoveAnimation( combatant, position )

