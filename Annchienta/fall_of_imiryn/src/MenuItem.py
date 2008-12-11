
class MenuItem:

    # Constructs and sets stuff like name and tooltip
    def __init__( self, name, toolTip=None ):
    
        self.name = name
        self.toolTip = toolTip
        
    # It's not a menu, it's purely a menu item
    def isMenu( self ):
        return False

    def getName( self ):
        return self.name

    def getToolTip( self ):
        return self.toolTip
