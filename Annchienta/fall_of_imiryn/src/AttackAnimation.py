import annchienta
import Animation

class AttackAnimation( Animation.Animation ):

    def __init__( self, sprite, sound ):
        Animation.Animation.__init__( self, sprite, sound )
        self.audioManager = annchienta.getAudioManager()

    def play( self ):

        origPosition = annchienta.Vector( self.getCombatant().getPosition() )
        position = annchienta.Vector( self.getTarget().getPosition() )
        dx = int( self.target.getWidth()/2 + self.getCombatant().getWidth()/2 )
        dx = dx if self.target.isAlly() else -dx
        position.x += dx
        self.move( self.getCombatant(), position )

        if self.getSound():
            self.audioManager.playSound( self.getSound() )

        if self.getSprite():
            self.spriteOver( self.getTarget(), self.getSprite() )

        self.move( self.getCombatant(), origPosition )
