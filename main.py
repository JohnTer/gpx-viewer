import sys
from PyQt5 import QtWidgets
from gpxviewer import Gpxviewer

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    viewer = Gpxviewer()
    viewer.show()
    sys.exit(app.exec_())
