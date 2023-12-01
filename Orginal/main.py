import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow,QProgressBar, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLabel, QHBoxLayout, QSizePolicy, QFileDialog
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt,QSize
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import random
import time
import Gui

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = -1
        self.y = -1

class Bin:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rectangles = [] #Yerleştirilecek alandaki dikdörtgenlerin tutulduğu liste
        self.fitness = 0 #Yerleştirilen dikdörtgenlerin alanının toplamı

    def add_rectangle(self, rectangle):
        self.rectangles.append(rectangle)
        self.fitness += rectangle.width * rectangle.height #Yerleştirilen dikdörtgenin alanını fitness değerine ekleme işlemi

def load_data(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, 'Veri Seç', '', 'Text Files (*.txt);;All Files (*)', options=options)
        if file_name:
            self.rectangles = []
            self.bins = []

            with open(file_name, 'r') as file:
                num_rectangles = int(file.readline().strip())
                global bin_width
                global bin_height
                bin_width, bin_height = map(int, file.readline().strip().split())

                for _ in range(num_rectangles):
                    width, height = map(int, file.readline().strip().split())
                    self.rectangles.append(Rectangle(width, height))

            Gui.App.textEditMesaj.setPlainText("Veri Başarıyla Eklendi!")