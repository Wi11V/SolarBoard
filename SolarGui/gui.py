import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel, QToolTip
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import pyqtgraph as pg

from comms import start_serial_thread, get_recent_data

def run_gui():
    app = QApplication(sys.argv)

    pg.setConfigOption('background', '#121212')
    pg.setConfigOption('foreground', '#E0E0E0')

    window = QWidget()
    window.setWindowTitle("Solar Module Data")
    window.resize(800, 800)
    window.setStyleSheet("background-color: #1E1E1E; color: #E0E0E0;")

    #app.setWindowIcon(QIcon("../icon.ico"))

    layout = QGridLayout()
    layout.setSpacing(20)
    layout.setContentsMargins(30, 30, 30, 30)

    #label = QLabel("Battery SOC: -- %")
    #label.setFont(QFont("Arial", 16))
    #label.setStyleSheet("color: #888;")

    #sub_label1 = QLabel("Solar Efficiency: -- %")
    #sub_label1.setFont(QFont("Arial", 16))
    #sub_label1.setStyleSheet("color: #888")

    #sub_label2 = QLabel("Temperature: --")
    #sub_label2.setFont(QFont("Arial", 16))
    #sub_label2.setStyleSheet("color: #888")

    x = [0, 10, 20, 30, 40, 50]
    y = [20, 35, 45, 60, 55, 70]

    # Custom ScatterPlotItem subclass to show tooltips
    class HoverScatter(pg.ScatterPlotItem):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.setAcceptHoverEvents(True)

        def hoverEvent(self, ev):
            if ev.isExit():
                QToolTip.hideText()
                return
            pts = self.pointsAt(ev.pos())
            if pts.size > 0:
                point = pts[0]
                data = point.pos()
                x_val = data.x()
                y_val = data.y()

                widget = self.parentItem()
                while widget and not isinstance(widget, QWidget):
                    widget = widget.parentItem()

                if widget is None: 
                    widget = None

                QToolTip.showText(ev.screenPos().toPoint(),
                                  f"Sample #: {x_val:.0f}\nValue: {y_val:.2f}",
                                  widget,
                                  )
            else:
                QToolTip.hideText()
            super().hoverEvent(ev)

    def create_plot(title, line_color, dot_color, ylabel, unitlabel):
        plot = pg.PlotWidget()
        plot.setTitle(title)
        plot.setLabel('left', ylabel, units= unitlabel)
        plot.setLabel('bottom', 'Sample Number')
        plot.setYRange(0, 100)
        plot.setXRange(0, 120)
        plot.enableAutoRange(x=False, y=False)

        # Line only
        plot.plot(x, y, pen=pg.mkPen(color=line_color, width=2))

        # Scatter points with hover effect and tooltip
        scatter = HoverScatter(
            x=x, y=y,
            symbol='o',
            size=4,
            brush=dot_color,
            pen='white',
            hoverable=True,
            hoverBrush='white',
            hoverSize=8
        )
        plot.addItem(scatter)
        return plot

    plot1 = create_plot("Solar Efficiency", 'b', 'b', 'Efficiency', '%')
    plot2 = create_plot("Battery SOC", 'g', 'g', 'SOC','%')
    plot3 = create_plot("MPPT Inst. Power", 'orange', 'orange', 'Power','mW')
    plot4 = create_plot("Raw ALS", 'y', 'y', 'Value','')

    button = QPushButton("Start Logging")
    button.setFont(QFont("Arial", 14))
    button.setStyleSheet("""
        QPushButton {
            background-color: #0077cc;
            color: white;
            padding: 10px;
            border-radius: 5px;
        }
    """)

    buttone = QPushButton("Export to Excel")
    buttone.setFont(QFont("Arial", 14))
    buttone.setStyleSheet("""
        QPushButton {
            background-color: #121212;
            color: white;
            padding: 10px;
            border-radius: 5px;
        }
        QPushButton:pressed {
            background-color: #666666;    
        }
    """)

    buttonu = QPushButton("Update Graphs")
    buttonu.setFont(QFont("Arial", 14))
    buttonu.setStyleSheet("""
        QPushButton {
            background-color: #121212;
            color: white;
            padding: 10px;
            border-radius: 5px;
        }
        QPushButton:pressed {
            background-color: #666666;    
        }
    """)
    


    is_logging = False
    def toggle_logging():
        nonlocal is_logging
        if not is_logging:
            button.setText("Stop Logging")
            button.setStyleSheet("""
                QPushButton {
                    background-color: #cc3333;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                }
            """)
            is_logging = True
        
            print("Logging started...")
        else:
            button.setText("Start Logging")
            button.setStyleSheet("""
                QPushButton {
                    background-color: #0077cc;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                }
            """)
            is_logging = False
            print("Logging stopped...")

    button.clicked.connect(toggle_logging)

    #layout.addWidget(label, 0, 0, 1, 2)
    #layout.addWidget(sub_label1, 1, 0, 1, 2)
    #layout.addWidget(sub_label2, 2, 0, 1, 2)
    layout.addWidget(plot1, 3, 0)
    layout.addWidget(plot2, 3, 1)
    layout.addWidget(plot3, 4, 0)
    layout.addWidget(plot4, 4, 1)
    layout.addWidget(buttonu,5,0)
    layout.addWidget(button, 6,0)
    layout.addWidget(buttone, 7,0)

    window.setLayout(layout)
    window.show()
    sys.exit(app.exec())


