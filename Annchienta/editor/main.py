import annchienta
import sys

sys.path.append(".")

from editor import *

# init annchienta
annchienta.init()

app = QApplication( [] )
widget = Editor()
widget.show()
app.exec_()

#annchienta.quit()

