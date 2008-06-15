import sys

sys.path.append(".")

from editor import *

app = QApplication( [] )
widget = Editor()
widget.show()
app.exec_()
