import annchienta

videoMgr = annchienta.getVideoManager()
videoMgr.setVideoMode( 400, 300, "Annchienta", False )

inputMgr = annchienta.getInputManager()

surface = annchienta.Surface( "../testdata/img.png" )

videoMgr.drawSurface( surface, 0, 0 )

font = annchienta.Font( "../testdata/font.ttf", 50 )

mymap = annchienta.Map( "blabla" )

while inputMgr.running():
    
    inputMgr.update()
    
    videoMgr.setColor()
    
    videoMgr.drawSurface( surface, 0, 0 )
    
    #videoMgr.setColor( 255, 255, 0, 60 )
    
    videoMgr.drawString( font, "Hello World!", 200 - font.getStringWidth("Hello World!")/2, 10 )
    
    mymap.draw()
    
    videoMgr.flip()
    