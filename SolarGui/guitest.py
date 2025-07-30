
import sys
from PyQt5.QtWidgets import QApplication
import pyqtgraph as pg

app = QApplication(sys.argv)
win = pg.PlotWidget()
win.show()
win.plot([0], [0], symbol='o', symbolSize=30, symbolBrush='g')
sys.exit(app.exec())
