import threading
import annchienta

## A threaded class that does nothing more
#  then ticking the MapControl.
#
class UpdateThread( threading.Thread ):

    ## Constructs the class
    #  \param mapControl The MapControl instance to tick
    #  \param sleepTime Ms to sleep before every next tick
    def __init__( self, mapControl, sleepTime=100 ):

        # Call superclass constructor
        threading.Thread.__init__( self )

        # Set parameters
        self.mapControl = mapControl 
        self.sleepTime = sleepTime

        # Not yet running
        self.running = False

        # Get a reference for hi-precision timing
        self.engine = annchienta.getEngine()
        self.inputManager = annchienta.getInputManager()

    def run( self ):

        self.running = True

        # For as long as the gtk_main is running
        while self.inputManager.running() and self.running:

            # Sleep and tick
            self.engine.delay( self.sleepTime ) 
            self.mapControl.tick()

    def stop( self ):

        self.running = False

    def isRunning( self ):

        return self.running

