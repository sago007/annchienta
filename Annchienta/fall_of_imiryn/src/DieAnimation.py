import annchienta
import Animation

class DieAnimation( Animation.Animation ):

    def __init__( self, sprite, sound ):
        Animation.Animation.__init__( self, sprite, sound )

    def play( self ):

        position = annchienta.Vector( self.getCombatant().getPosition() )
        position.x -= 30 if self.getCombatant().isAlly() else -30
        self.move( self.getCombatant(), position )
