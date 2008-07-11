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

def insideScreen( x, y ):
    videoManager = annchienta.getVideoManager()
    return x>=0 and x<videoManager.getScreenWidth() and y>=0 and y<videoManager.getScreenHeight()

