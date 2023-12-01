import os
import sys
from platform import system
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QStyleFactory, QDesktopWidget
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

# Application root location ↓
if system() == "Windows":
    appFolder = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\"
elif system() == "Linux":
    appFolder = os.path.dirname(os.path.realpath(sys.argv[0])) + "//"

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, main_window=None, width=30, height=29, dpi=120):
        self.main_window = main_window
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        self.fig.set_facecolor(main_window.palette().color(QPalette.Window).getRgbF())
        self.fig.set_size_inches(main_window.width() / dpi, main_window.height() / dpi)
        super(MyMplCanvas, self).__init__(self.fig)
        self.setParent(parent)

        self.ax.set_facecolor(main_window.palette().color(QPalette.Window).getRgbF())
        # Diğer grafik öğelerini de güncelleyin
        #self.ax.plot([0, 1, 2, 1, 0], color='blue')  # Örnek çizgi
    

class App(QMainWindow):
    def __init__(self):
        """Constructor."""
        super(App, self).__init__()
        uic.loadUi(appFolder + "cut.ui", self)  # Load the UI(User Interface) file.
        self.makeWindowCenter()
        #self.run_system()  # main operating function of this GUI FIle
        # Status Bar Message
        self.statusBar().showMessage("Developed By Sammöst")
        self.setWindowTitle("Kesme ve Paketleme Problemi Arayüzü")
        self.canvas = MyMplCanvas(self, main_window=self, width=30, height=29, dpi=100)
        self.verticalLayout.addWidget(self.canvas)

    def makeWindowCenter(self):
        """For launching windows in center."""
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyle(QStyleFactory.create("Fusion"))

    darkPalette = QtGui.QPalette()
    darkColor = QColor(45, 45, 45)
    disabledColor = QColor(127, 127, 127)
    darkPalette.setColor(QPalette.Window, darkColor)
    darkPalette.setColor(QPalette.WindowText, Qt.white)
    darkPalette.setColor(QPalette.Base, QColor(40, 40, 40))
    darkPalette.setColor(QPalette.AlternateBase, darkColor)
    darkPalette.setColor(QPalette.ToolTipBase, Qt.white)
    darkPalette.setColor(QPalette.ToolTipText, Qt.white)
    darkPalette.setColor(QPalette.Text, Qt.white)
    darkPalette.setColor(QPalette.Disabled, QPalette.Text, disabledColor)
    darkPalette.setColor(QPalette.Button, darkColor)
    darkPalette.setColor(QPalette.ButtonText, Qt.white)
    darkPalette.setColor(QPalette.Disabled, QPalette.ButtonText, disabledColor)
    darkPalette.setColor(QPalette.BrightText, Qt.red)
    darkPalette.setColor(QPalette.Link, QColor(42, 130, 218))
    darkPalette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    darkPalette.setColor(QPalette.HighlightedText, Qt.black)
    darkPalette.setColor(QPalette.Disabled, QPalette.HighlightedText, disabledColor)

    app.setPalette(darkPalette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

    run_main = App()  # Instantiate The App() class
    run_main.show()
    sys.exit(app.exec_())