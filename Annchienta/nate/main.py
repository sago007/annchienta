#!/usr/bin/python
import gtk
import MainWindow
import annchienta

# Our main function
if __name__ == "__main__":

    annchienta.init()
    mainWindow = MainWindow.MainWindow()
    gtk.main()
    mainWindow.free()
    annchienta.quit()
