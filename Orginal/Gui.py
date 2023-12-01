import os
import sys
from platform import system
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtCore import Qt,QFileInfo
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QStyleFactory, QDesktopWidget,QListWidgetItem
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import main
from PyQt5.QtWidgets import QApplication, QMainWindow,QProgressBar, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLabel, QHBoxLayout, QSizePolicy, QFileDialog
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt,QSize
import random
import time


# Application root location ↓
if system() == "Windows":
    appFolder = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\"
elif system() == "Linux":
    appFolder = os.path.dirname(os.path.realpath(sys.argv[0])) + "//"

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
def is_valid_location(bin, rect, x, y):
    if x + rect.width > bin.width or y + rect.height > bin.height:
        return False
    for r in bin.rectangles:
        if (x < r.x + r.width and x + rect.width > r.x and
            y < r.y + r.height and y + rect.height > r.y):
            return False
    return True

#bin_width = 0
#bin_height = 0

def pack_rectangles(rectangles):
    bins = [Bin(bin_width, bin_height)]

    for rect in rectangles:
        fitted = False
        for bin in bins:
            for y in range(bin.height):
                for x in range(bin.width):
                    if is_valid_location(bin, rect, x, y):
                        rect.x = x
                        rect.y = y
                        bin.add_rectangle(rect)
                        fitted = True
                        break
                if fitted:
                    break
            if fitted:
                break

    return bins

def pack_rectangles_genetic(rectangles, bin_width, bin_height):
    bins = [Bin(bin_width, bin_height)]

    for rect in rectangles:
        fitted = False
        for bin in bins:
            for y in range(bin.height):
                for x in range(bin.width):
                    if is_valid_location(bin, rect, x, y):
                        rect.x = x
                        rect.y = y
                        bin.add_rectangle(rect)
                        fitted = True
                        break
                if fitted:
                    break
            if fitted:
                break

    return bins

def create_chromosome(rectangles): #Kromozom Oluşturma Fonksiyonu
        chromosome = []
        for i in range(len(rectangles)):
            chromosome.append(i) #Dikdörtgenlerin sıralamasını kromozoma ekleme işlemi
        random.shuffle(chromosome) #Dikdörtgenlerin sıralamasını rastgele karıştırma işlemi
        for i in range(len(rectangles)):
            chromosome.append(random.randint(0, 1)) #Dikdörtgenlerin döndürülmesini kromozoma ekleme işlemi
        return chromosome

def create_population(rectangles, population_size): #Popülasyon Oluşturma Fonksiyonu
    population = []
    for i in range(population_size):
        population.append(create_chromosome(rectangles)) #Rastgele kromozomlar oluşturarak popülasyona ekleme işlemi
    return population

def decode_chromosome(chromosome, rectangles): #Kromozomu Dikdörtgenlere Dönüştürme Fonksiyonu
    decoded_rectangles = []
    for i in range(len(rectangles)):
        index = chromosome[i] #Kromozomun ilk yarısında dikdörtgenlerin sıralaması vardır
        rotation = chromosome[i + len(rectangles)] #Kromozomun ikinci yarısında dikdörtgenlerin döndürülmesi vardır
        width = rectangles[index].width
        height = rectangles[index].height
        if rotation == 1: #Eğer dikdörtgen döndürülmüşse, genişlik ve yükseklik yer değiştirir
            width, height = height, width
        decoded_rectangles.append(Rectangle(width, height)) #Dönüştürülen dikdörtgenleri listeye ekleme işlemi
        decoded_rectangles[i].rotated = rotation #Dikdörtgenin döndürülüp döndürülmediğini kaydetme işlemi
    return decoded_rectangles

def evaluate_population(population, rectangles, bin_width, bin_height): #Popülasyonu Değerlendirme Fonksiyonu
    evaluated_population = []
    for chromosome in population:
        decoded_rectangles = decode_chromosome(chromosome, rectangles) #Kromozomu dikdörtgenlere dönüştürme işlemi
        bins = pack_rectangles_genetic(decoded_rectangles, bin_width, bin_height) #Dikdörtgenleri yerleştirme işlemi
        fitness = bins[0].fitness #Yerleştirilen dikdörtgenlerin alanının toplamı
        evaluated_population.append((chromosome, fitness)) #Kromozom ve fitness değerini listeye ekleme işlemi
    return evaluated_population

def select_population(evaluated_population, population_size): #Popülasyondan Seçim Yapma Fonksiyonu
    selected_population = []
    total_fitness = sum(fitness for chromosome, fitness in evaluated_population) #Popülasyondaki tüm fitness değerlerinin toplamı
    probabilities = [fitness / total_fitness for chromosome, fitness in evaluated_population] #Popülasyondaki her kromozomun seçilme olasılığı
    for i in range(population_size):
        r = random.random() #Rastgele bir sayı üretme işlemi
        s = 0 #Kümülatif olasılık değeri
        for j in range(len(evaluated_population)):
            s += probabilities[j] #Kümülatif olasılığı artırma işlemi
            if r < s: #Eğer rastgele sayı kümülatif olasılıktan küçükse, o kromozomu seçme işlemi
                selected_population.append(evaluated_population[j][0]) #Seçilen kromozomu listeye ekleme işlemi
                break
    return selected_population

def crossover_population(population, crossover_rate): #Popülasyondaki Kromozomları Çaprazlama Fonksiyonu
    crossed_population = []
    for i in range(0, len(population), 2): #Popülasyondaki kromozomları ikişerli gruplara ayırma işlemi
        parent1 = population[i] #İlk ebeveyn kromozomu
        parent2 = population[i + 1] #İkinci ebeveyn kromozomu
        child1 = parent1.copy() #İlk çocuk kromozomu
        child2 = parent2.copy() #İkinci çocuk kromozomu
        r = random.random() #Rastgele bir sayı üretme işlemi
        if r < crossover_rate: #Eğer rastgele sayı çaprazlama oranından küçükse, çaprazlama yapma işlemi
            point = random.randint(1, len(parent1) - 1) #Çaprazlama noktasını rastgele belirleme işlemi
            child1[:point] = parent2[:point] #İlk çocuk kromozomunun ilk yarısını ikinci ebeveyn kromozomunun ilk yarısıyla değiştirme işlemi
            child2[:point] = parent1[:point] #İkinci çocuk kromozomunun ilk yarısını ilk ebeveyn kromozomunun ilk yarısıyla değiştirme işlemi
        crossed_population.append(child1) #İlk çocuk kromozomunu listeye ekleme işlemi
        crossed_population.append(child2) #İkinci çocuk kromozomunu listeye ekleme işlemi
    return crossed_population

def mutate_population(population, mutation_rate): #Popülasyondaki Kromozomları Mutasyona Uğratma Fonksiyonu
    mutated_population = []
    for chromosome in population:
        mutated_chromosome = chromosome.copy() #Kromozomun bir kopyasını oluşturma işlemi
        r = random.random() #Rastgele bir sayı üretme işlemi
        if r < mutation_rate: #Eğer rastgele sayı mutasyon oranından küçükse, mutasyon yapma işlemi
            point = random.randint(0, len(chromosome) - 1) #Mutasyon noktasını rastgele belirleme işlemi
            if point < len(chromosome) // 2: #Eğer mutasyon noktası kromozomun ilk yarısındaysa, dikdörtgenlerin sıralamasını değiştirme işlemi
                swap = random.randint(0, len(chromosome) // 2 - 1) #Değiştirilecek diğer noktayı rastgele belirleme işlemi
                mutated_chromosome[point], mutated_chromosome[swap] = mutated_chromosome[swap], mutated_chromosome[point] #İki noktadaki değerleri değiştirme işlemi
            else: #Eğer mutasyon noktası kromozomun ikinci yarısındaysa, dikdörtgenlerin döndürülmesini değiştirme işlemi
                mutated_chromosome[point] = 1 - mutated_chromosome[point] #Döndürme değerini tersine çevirme işlemi
        mutated_population.append(mutated_chromosome) #Mutasyona uğramış kromozomu listeye ekleme işlemi
    return mutated_population

def genetic_algorithm(rectangles, bin_width, bin_height, population_size, iteration, crossover_rate, mutation_rate,progressBar,textBoxMessage): #Genetik Algoritma Fonksiyonu
    app = App()
    population = create_population(rectangles, population_size) #Rastgele bir popülasyon oluşturma işlemi
    best_chromosome = None #En iyi kromozomu tutan değişken
    best_fitness = 0 #En iyi fitness değerini tutan değişken
    total_iterations = iteration  # Toplam iterasyon sayısı
    start_time = time.time()
    
    for i in range(iteration): #Belirli bir iterasyon sayısı kadar döngü yapma işlemi
        
        evaluated_population = evaluate_population(population, rectangles, bin_width, bin_height) #Popülasyonu değerlendirme işlemi
        for chromosome, fitness in evaluated_population: #Popülasyondaki her kromozom ve fitness değeri için döngü yapma işlemi
            if fitness > best_fitness: #Eğer fitness değeri en iyi fitness değerinden büyükse, en iyi kromozomu ve fitness değerini güncelleme işlemi
                best_chromosome = chromosome
                best_fitness = fitness
        selected_population = select_population(evaluated_population, population_size) #Popülasyondan seçim yapma işlemi
        crossed_population = crossover_population(selected_population, crossover_rate) #Popülasyondaki kromozomları çaprazlama işlemi
        mutated_population = mutate_population(crossed_population, mutation_rate) #Popülasyondaki kromozomları mutasyona uğratma işlemi
        population = mutated_population #Popülasyonu güncelleme işlemi

        textBoxMessage.append(f"Iterasyon No: {i + 1} - En iyi fitness: {best_fitness:2f}")
        
        progress_percentage = (i + 1) / total_iterations * 100  # İterasyonun yüzde olarak oranını hesapla
        progressBar.setValue(int(progress_percentage))
        
    elapsed_time = time.time() - start_time  # Geçen süreyi hesapla
    progressBar.setValue(100)  # İterasyon çubuğunu tam değere ayarla
    textBoxMessage.append("Genetik Algoritma Tamamlandı. Toplam Geçen Süre: {:.2f} saniye".format(elapsed_time))
    #progressBar.setFormat("Genetik Algoritma Tamamlandı. Toplam Geçen Süre: {:.2f} saniye".format(elapsed_time))
    textBoxMessage.append(f"En iyi kromozom: {best_chromosome}")
    textBoxMessage.append(f"En iyi fitness değeri:, {best_fitness}")

        
    print("En iyi kromozom:", best_chromosome)
    print("En iyi fitness değeri:", best_fitness)
    return best_chromosome, best_fitness #En iyi kromozomu ve fitness değerini döndürme işlemi

#MatplotLib Sonuç Ekranı
class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, main_window=None, width=20, height=20, dpi=120):
        self.main_window = main_window
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        self.fig.set_facecolor(main_window.palette().color(QPalette.Window).getRgbF())
        self.fig.set_size_inches(main_window.width() / dpi, main_window.height() / dpi)
        
        super(MyMplCanvas, self).__init__(self.fig)
        self.setParent(parent)


        self.ax.set_facecolor(main_window.palette().color(QPalette.Window).getRgbF())
        self.ax.set_aspect('equal', adjustable='box')  # Ensure equal aspect ratio
        # Diğer grafik öğelerini de güncelleyin
        #self.ax.plot([0, 1, 2, 1, 0], color='blue')  # Örnek çizgi
class Action:
    def __init__(self, data_name,action_type, details):
        self.data_name = data_name
        self.action_type = action_type  # "LoadData", "RunNextFit", "RunGeneticAlgorithm", "RunEkYontem", "SaveAsSvg"
        self.details = details  # İlgili detaylar, örneğin, seçilen veri adı, kullanılan algoritma adı vb.

    def __str__(self):
        return f"DataName: {self.data_name}, Action Type: {self.action_type}, Details: {self.details}"

class Operation:
    def __init__(self, data_name, method_name, success_rate):
        self.data_name = data_name
        self.method_name = method_name
        self.success_rate = success_rate

class App(QMainWindow):
    def __init__(self):
        """Constructor."""
        super(App, self).__init__()
        uic.loadUi(appFolder + "cut.ui", self)  # Load the UI(User Interface) file.
        self.makeWindowCenter()
        self.run_system()  # main operating function of this GUI FIle
        # Status Bar Message
        self.statusBar().showMessage("Developed By Sammböst")
        self.setWindowTitle("Kesme ve Paketleme Problemi Arayüzü")
        self.canvas = MyMplCanvas(self, main_window=self, width=5, height=5, dpi=100) #Ana Sayfa Matplotlib Sonucu
        self.canvas_compare = MyMplCanvas(self, main_window=self, width=5, height=5, dpi=100) #Sonuç Sayfası Karşılaştırma MatplotLibi
        self.verticalLayout.addWidget(self.canvas)
        self.verticalLayout_5.addWidget(self.canvas_compare)
        self.textBoxMessage.setLineWrapMode(QTextEdit.WidgetWidth)
        # QListWidget'ın SelectionMode'ını ayarlamak
        self.listWidget.setSelectionMode(self.listWidget.MultiSelection)

        self.rectangles = []
        self.bins = []
        self.actions = []
        self.operations_list = []  # Yapılan işlemleri tutacak liste
        
    def update_actions(self,data_name,action_type, details):
        new_action = Action(data_name,action_type, details)
        self.actions.append(new_action)
        print(new_action)

    def gecis_yap(self):
        self.tabWidget.setCurrentIndex(1)
        self.show_operations_list()

    def makeWindowCenter(self):
        """For launching windows in center."""
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def run_system(self):
        """Main load function"""
        
        #self.pushButton.clicked.connect(self.add_folder_button_on_click)
        self.btnVeriSec.clicked.connect(self.load_data)
        self.btnNextFit.clicked.connect(self.run_next_fit)
        self.btnGenetic.clicked.connect(self.run_genetic_algorithm)
        self.btnEkYontem.clicked.connect(self.run_ek_yontem)
        self.btnSaveSVG.clicked.connect(self.save_as_svg)
        self.btnSonucGoruntule.clicked.connect(self.gecis_yap)
        self.showResult.clicked.connect(self.handle_process_button)
    
    def handle_process_button(self):
        selected_items = [item.text() for item in self.listWidget.selectedItems()]

        # Başarı oranları, yöntem isimleri ve veri isimlerini çıkarın
        data_names = []
        success_rates = {}
        methods = []

        for item in selected_items:
            parts = item.split(" - ")
            data_name = parts[0].split(":")[1].strip()  # Veri ismini ayıkla
            method = parts[1].split(":")[1].strip()     # Yöntemi ayıkla
            success_rate = float(parts[2].split(":")[1].replace('%', ''))  # Başarı oranını ayıkla ve yüzdelik işaretini kaldır
            #data_name, method, success_rate = parts[0], parts[1], parts[2]
            data_names.append(data_name)
            methods.append(method)
            success_rates[data_name + " - " + method] = success_rate

        
        # Matplotlib grafiklerini oluşturun
        self.plot_result_data(methods, success_rates, data_names)
        
    def load_data(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.file_name, _ = QFileDialog.getOpenFileName(self, 'Veri Seç', '', 'Text Files (*.txt);;All Files (*)', options=options)
        if self.file_name:
            self.rectangles = []
            self.bins = []

            self.file_info = QFileInfo(self.file_name)
            self.file_name_only = self.file_info.baseName()  # Dosyanın adını al
            

            with open(self.file_name, 'r') as file:
                num_rectangles = int(file.readline().strip())
                global bin_width
                global bin_height
                bin_width, bin_height = map(int, file.readline().strip().split())

                for _ in range(num_rectangles):
                    width, height = map(int, file.readline().strip().split())
                    self.rectangles.append(Rectangle(width, height))
            self.textBoxMessage.append(f"{self.file_name_only} başarıyla seçildi!") # Sadece dosya adını göster
            #self.update_text_box(f"{self.file_name_only} başarıyla seçildi!")  
            
    def run_next_fit(self,data_name):
        if not self.rectangles:
            #self.textBoxMessage.setPlainText('Önce veri seçmelisiniz.')
            self.textBoxMessage.append("Next-Fit Yöntemi İçin Önce Veri Seçmelisiniz")
            return

        self.bins = pack_rectangles(self.rectangles)

        total_rectangles_area = sum(rect.width * rect.height for rect in self.rectangles)
        total_packing_area = bin_width * bin_height
        total_fitted_area = sum(rect.width * rect.height for bin in self.bins for rect in bin.rectangles)
        success_rate = (total_fitted_area / total_rectangles_area) * 100

        self.textBoxMessage.append(f'Next-Fit Yöntemi Çözümü Tamamlandı.\nBaşarı Oranı: {success_rate:.2f}%')
        self.visualize_packing()
        self.update_actions(f"Veri İsmi: {self.file_name_only}","Yöntem: NextFit", f"Success Rate: {success_rate:.2f}%")  # Yeni işlemi kaydet
        self.operation = Operation(data_name=self.file_name_only, method_name="Next Fit", success_rate=success_rate)
        self.operations_list.append(self.operation)

    def run_genetic_algorithm(self,data_name):
        progressBar = self.progressBar
        textBoxMessage = self.textBoxMessage
        if not self.rectangles:
            self.textBoxMessage.append('Genetik Algoritma Yöntemi İçin Önce Veri Seçmelisiniz!')
            return

        self.bins = pack_rectangles_genetic(self.rectangles,bin_width,bin_height)
        # Genetik algoritma parametreleri
        population_size = 100
        iteration = 10
        crossover_rate = 0.8
        mutation_rate = 0.1

        best_chromosome, best_fitness = genetic_algorithm(self.rectangles, bin_width, bin_height, population_size, iteration, crossover_rate, mutation_rate,progressBar,textBoxMessage)
        print(best_chromosome,best_fitness)
        best_rectangles = decode_chromosome(best_chromosome, self.rectangles)
        self.best_bins = pack_rectangles_genetic(best_rectangles, bin_width, bin_height)

        total_rectangles_area = sum(rect.width * rect.height for rect in self.rectangles)
        total_packing_area = bin_width * bin_height
        total_fitted_area = sum(rect.width * rect.height for bin in self.best_bins for rect in bin.rectangles)
        success_rate = (total_fitted_area / total_rectangles_area) * 100

        self.textBoxMessage.append(f'Genetik Algoritma Çözümü Tamamlandı.\nBaşarı Oranı: {success_rate:.2f}%')
        self.visualize_packing_genetic(self.best_bins)
        self.update_actions(f"Veri İsmi: {self.file_name_only}","Genetic Algorithm", f"Success Rate: {success_rate:.2f}%")  # Yeni işlemi kaydet
        self.operation = Operation(data_name=self.file_name_only, method_name="Genetik Algoritma", success_rate=success_rate)
        self.operations_list.append(self.operation)

    def show_operations_list(self):
        # Yeni sekme açıldığında ListWidget içinde işlemleri gösterme
        self.listWidget.clear()
        for operation in self.operations_list:
            item_text = f"Veri İsmi: {operation.data_name} - Yöntem: {operation.method_name} - Başarı Oranı: {operation.success_rate}%"
            list_item = QListWidgetItem(item_text)
            print(item_text)
            self.listWidget.addItem(list_item)

    def run_ek_yontem(self):

        reply = QMessageBox.information(self, "Bilgilendirme", "Ek Yöntem Henüz Geliştirilmemiştir! "
                                                                      , QMessageBox.Ok)
    def plot_result_data(self, methods, success_rates, data_names):
        color = self.palette().color(QPalette.Window).getRgbF()
        self.canvas_compare.figure.clear()
        ax = self.canvas_compare.fig.add_subplot(111)
        #ax.set_aspect('equal')
        bar_width = 0.5


       #Bar grafik oluşturun
        #bars = ax.bar(range(len(data_names)), success_rates.values(),color=color)"""
        
        # Çizgi grafiği oluşturun
        ax.plot(range(len(data_names)), success_rates.values(), marker='o', linestyle='-', color=color)

        # Eksen etiketlerini ve başlık ekleyin
        ax.set_xlabel('Veri İsmi - Yöntem',color="white")
        ax.set_ylabel('Success Rate')
        ax.set_title('Success Rate Comparison')

        """# Barların üzerine etiketleri ekleyin
        for bar, label in zip(bars, success_rates.keys()):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), label,
                    ha='center', va='bottom', rotation=90)"""

        # Eğer gerekiyorsa x ekseni üzerindeki etiketleri ayarlayın
        ax.set_xticks(range(len(data_names)))
        ax.set_xticklabels(success_rates.keys(), rotation=0, ha='right')

        # Canvas'ı güncelleyin
        self.canvas_compare.draw()

    def visualize_packing(self):
        self.canvas.fig.clear()
        self.ax = self.canvas.fig.add_subplot(111)
        self.ax.set_aspect('equal')

        for i, bin in enumerate(self.bins):
            #ax.set_title(f'Bin {i + 1}')
            color = self.palette().color(QPalette.Window).getRgbF()
            for j, rect in enumerate(bin.rectangles):

                self.ax.add_patch(plt.Rectangle((rect.x, rect.y), rect.width, rect.height, fill=True, color=color))
                self.ax.add_patch(plt.Circle((rect.x + rect.width / 2, rect.y + rect.height / 2), 0.09, color='black'))
                self.ax.plot([rect.x, rect.x + rect.width], [rect.y, rect.y], color='white')
                self.ax.plot([rect.x, rect.x], [rect.y, rect.y + rect.height], color='white')
                self.ax.plot([rect.x + rect.width, rect.x + rect.width], [rect.y, rect.y + rect.height], color='white')
                self.ax.plot([rect.x, rect.x + rect.width], [rect.y + rect.height, rect.y + rect.height], color='white')


            #bin.height ve bin.width eskiden bin_height ve bin_width şeklindeydi
            for x in range(bin.width):
                for y in range(bin.height):
                    is_empty = True
                    for rect in bin.rectangles:
                        if x >= rect.x and x < rect.x + rect.width and y >= rect.y and y < rect.y + rect.height:
                            is_empty = False
                            break
                    if is_empty:
                        #self.ax.add_patch(plt.Rectangle((x, y), 1, 1, fill=True, color='red'))
                        rectangle = plt.Rectangle((x, y), 1, 1, fill=True, color='#8FACD0')
                        self.ax.add_patch(rectangle)
                        self.ax.plot([x, x + 1], [y, y + 1], color='black', linewidth=1)  
                        self.ax.plot([x + 1, x], [y, y + 1], color='black', linewidth=1) 

        self.ax.set_xlim(0, bin.width)
        self.ax.set_ylim(0, bin.height)
        self.ax.figure.tight_layout()
        self.canvas.draw()
        self.SaveValue = "NextFit"


    def visualize_saving_next_fit(self):
        #Next-Fit Kaydetmesi Yaparken Bu Fonksiyon Çalışarak Arka Plan Şeffaf Dikdörtgenler siyah olacaktır.
        self.canvas.fig.clear()
        self.ax = self.canvas.fig.add_subplot(111)
        self.ax.set_aspect('equal')

        for i, bin in enumerate(self.bins):
            #ax.set_title(f'Bin {i + 1}')
            color = self.palette().color(QPalette.Window).getRgbF()
            for j, rect in enumerate(bin.rectangles):

                self.ax.add_patch(plt.Rectangle((rect.x, rect.y), rect.width, rect.height, fill=True, color="white"))
                self.ax.add_patch(plt.Circle((rect.x + rect.width / 2, rect.y + rect.height / 2), 0.09, color='black'))
                self.ax.plot([rect.x, rect.x + rect.width], [rect.y, rect.y], color='black')
                self.ax.plot([rect.x, rect.x], [rect.y, rect.y + rect.height], color='black')
                self.ax.plot([rect.x + rect.width, rect.x + rect.width], [rect.y, rect.y + rect.height], color='black')
                self.ax.plot([rect.x, rect.x + rect.width], [rect.y + rect.height, rect.y + rect.height], color='black')


            #bin.height ve bin.width eskiden bin_height ve bin_width şeklindeydi
            for x in range(bin.width):
                for y in range(bin.height):
                    is_empty = True
                    for rect in bin.rectangles:
                        if x >= rect.x and x < rect.x + rect.width and y >= rect.y and y < rect.y + rect.height:
                            is_empty = False
                            break
                    if is_empty:
                        #self.ax.add_patch(plt.Rectangle((x, y), 1, 1, fill=True, color='red'))
                        rectangle = plt.Rectangle((x, y), 1, 1, fill=False, color='Black')
                        self.ax.add_patch(rectangle)
                        self.ax.plot([x, x + 1], [y, y + 1], color='black', linewidth=1)  
                        self.ax.plot([x + 1, x], [y, y + 1], color='black', linewidth=1) 

        self.ax.set_xlim(0, bin.width)
        self.ax.set_ylim(0, bin.height)
        self.ax.figure.tight_layout()
        #self.canvas.draw()

    def visualize_packing_genetic(self,bins):
        self.canvas.fig.clear()
        self.ax = self.canvas.fig.add_subplot(111)
        self.ax.set_aspect('equal')
        color = self.palette().color(QPalette.Window).getRgbF()

        for i, bin in enumerate(bins):
            #ax.set_title(f'Bin {i + 1}')
            for j, rect in enumerate(bin.rectangles):
                self.ax.add_patch(plt.Rectangle((rect.x, rect.y), rect.width, rect.height, fill=True, color=color))
                self.ax.add_patch(plt.Circle((rect.x + rect.width / 2, rect.y + rect.height / 2), 0.1, color='#263445'))
                self.ax.plot([rect.x, rect.x + rect.width], [rect.y, rect.y], color='#C5CBD2')
                self.ax.plot([rect.x, rect.x], [rect.y, rect.y + rect.height], color='#C5CBD2')
                self.ax.plot([rect.x + rect.width, rect.x + rect.width], [rect.y, rect.y + rect.height], color='#C5CBD2')
                self.ax.plot([rect.x, rect.x + rect.width], [rect.y + rect.height, rect.y + rect.height], color='#C5CBD2')

            for x in range(bin_width):
                for y in range(bin_height):
                    is_empty = True
                    for rect in bin.rectangles:
                        if x >= rect.x and x < rect.x + rect.width and y >= rect.y and y < rect.y + rect.height:
                            is_empty = False
                            break
                    if is_empty:
                        #self.ax.add_patch(plt.Rectangle((x, y), 1, 1, fill=True, color='#8FACD0'))
                        #self.ax.plot([x, x + 1], [y, y + 1], color='#8FACD0', linewidth=1)
                        rectangle = plt.Rectangle((x, y), 1, 1, fill=True, color='#8FACD0')
                        self.ax.add_patch(rectangle)
                        self.ax.plot([x, x + 1], [y, y + 1], color='black', linewidth=1)  
                        self.ax.plot([x + 1, x], [y, y + 1], color='black', linewidth=1)  

        self.ax.set_xlim(0, bin_width)
        self.ax.set_ylim(0, bin_height)
        self.ax.figure.tight_layout()
        self.canvas.draw()
        self.SaveValue = "Genetic"

    def visualize_packing_saving_genetic(self,bins):
        self.canvas.fig.clear()
        self.ax = self.canvas.fig.add_subplot(111)
        self.ax.set_aspect('equal')
        color = self.palette().color(QPalette.Window).getRgbF()

        for i, bin in enumerate(bins):
            #ax.set_title(f'Bin {i + 1}')
            for j, rect in enumerate(bin.rectangles):
                self.ax.add_patch(plt.Rectangle((rect.x, rect.y), rect.width, rect.height, fill=True, color="white"))
                self.ax.add_patch(plt.Circle((rect.x + rect.width / 2, rect.y + rect.height / 2), 0.1, color='black'))
                self.ax.plot([rect.x, rect.x + rect.width], [rect.y, rect.y], color='black')
                self.ax.plot([rect.x, rect.x], [rect.y, rect.y + rect.height], color='black')
                self.ax.plot([rect.x + rect.width, rect.x + rect.width], [rect.y, rect.y + rect.height], color='black')
                self.ax.plot([rect.x, rect.x + rect.width], [rect.y + rect.height, rect.y + rect.height], color='black')

            for x in range(bin_width):
                for y in range(bin_height):
                    is_empty = True
                    for rect in bin.rectangles:
                        if x >= rect.x and x < rect.x + rect.width and y >= rect.y and y < rect.y + rect.height:
                            is_empty = False
                            break
                    if is_empty:
                        #self.ax.add_patch(plt.Rectangle((x, y), 1, 1, fill=True, color='#8FACD0'))
                        rectangle = plt.Rectangle((x, y), 1, 1, fill=False, color='Black')
                        self.ax.add_patch(rectangle)
                        self.ax.plot([x, x + 1], [y, y + 1], color='black', linewidth=1)  
                        self.ax.plot([x + 1, x], [y, y + 1], color='black', linewidth=1)  
                        #self.ax.plot([x, x + 1], [y, y + 1], color='black', linewidth=1)

        self.ax.set_xlim(0, bin_width)
        self.ax.set_ylim(0, bin_height)
        self.ax.figure.tight_layout()
        #self.canvas.draw()

    def save_as_svg(self):
        if not self.bins:
            self.textBoxMessage.setPlainText('Önce veriyi çözmelisiniz.')
            return

        file_dialog = QFileDialog(self)
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_path, _ = file_dialog.getSaveFileName(self, 'SVG Olarak Kaydet', '', 'SVG Files (*.svg)', options=options)
        if file_path:
            if self.SaveValue == "NextFit":
                self.visualize_saving_next_fit()
                self.ax.axis('off')
                #fig = self.canvas.fig
                #fig.patch.set_alpha(0)
                self.canvas.fig.savefig(file_path, format='svg', bbox_inches='tight', pad_inches=0.2,transparent=True)
                self.textBoxMessage.setPlainText(f'Görüntü başarıyla SVG olarak kaydedildi: {file_path}')
            elif self.SaveValue == "Genetic":
                self.visualize_packing_saving_genetic(self.best_bins)
                self.ax.axis('off')
                self.canvas.fig.savefig(file_path, format='svg', bbox_inches='tight', pad_inches=0.2,transparent=True)
                self.textBoxMessage.setPlainText(f'Görüntü başarıyla SVG olarak kaydedildi: {file_path}')
    

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