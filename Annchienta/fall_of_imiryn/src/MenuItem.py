
class MenuItem(object):

    # Constructs and sets stuff like name and tooltip
    def __init__( self, name, toolTip=None ):
    
        self.name = name
        self.toolTip = toolTip
        self.enabled = True
        
    # It's not a menu, it's purely a menu item
    def isMenu( self ):
        return False

    def getName( self ):
        return self.name

    def getToolTip( self ):
        return self.toolTip

    def setEnabled( self, enabled ):
        self.enabled = enabled

    def isEnabled( self ):
        return self.enabled
