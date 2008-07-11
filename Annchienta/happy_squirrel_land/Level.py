import annchienta

def treeUpperY():
    videoManager = annchienta.getVideoManager()
    return videoManager.getScreenHeight()-100

def yAboveTree( y ):
    return False

def yInTree( y ):
    return True
    
def yBelowTree( y ):
    return False

