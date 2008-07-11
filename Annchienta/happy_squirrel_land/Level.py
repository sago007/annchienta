import annchienta

def treeUpperY():
    videoManager = annchienta.getVideoManager()
    return videoManager.getScreenHeight()-100
    
def treeLowerY():
    videoManager = annchienta.getVideoManager()
    return videoManager.getScreenHeight()-56

def yAboveTree( y ):
    return y<treeUpperY()

def yInTree( y ):
    return y>=treeUpperY() and y<=treeLowerY()
    
def yBelowTree( y ):
    return y>treeLowerY()

