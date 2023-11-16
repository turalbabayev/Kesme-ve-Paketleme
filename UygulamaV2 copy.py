import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow,QProgressBar, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLabel, QHBoxLayout, QSizePolicy, QFileDialog
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt,QSize
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import random
import time
import time
from PyQt5.QtWidgets import QProgressBar, QProgressDialog


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

bin_width = 0
bin_height = 0

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

def genetic_algorithm(rectangles, bin_width, bin_height, population_size, iteration, crossover_rate, mutation_rate,progress_bar): #Genetik Algoritma Fonksiyonu
    population = create_population(rectangles, population_size) #Rastgele bir popülasyon oluşturma işlemi
    best_chromosome = None #En iyi kromozomu tutan değişken
    best_fitness = 0 #En iyi fitness değerini tutan değişken
    for i in range(iteration): #Belirli bir iterasyon sayısı kadar döngü yapma işlemi
        #start_time = time.time()
        evaluated_population = evaluate_population(population, rectangles, bin_width, bin_height) #Popülasyonu değerlendirme işlemi
        for chromosome, fitness in evaluated_population: #Popülasyondaki her kromozom ve fitness değeri için döngü yapma işlemi
            if fitness > best_fitness: #Eğer fitness değeri en iyi fitness değerinden büyükse, en iyi kromozomu ve fitness değerini güncelleme işlemi
                best_chromosome = chromosome
                best_fitness = fitness
        selected_population = select_population(evaluated_population, population_size) #Popülasyondan seçim yapma işlemi
        crossed_population = crossover_population(selected_population, crossover_rate) #Popülasyondaki kromozomları çaprazlama işlemi
        mutated_population = mutate_population(crossed_population, mutation_rate) #Popülasyondaki kromozomları mutasyona uğratma işlemi
        population = mutated_population #Popülasyonu güncelleme işlemi

        progress_bar.setValue(i+1)
        if QApplication.hasPendingEvents():
            QApplication.processEvents()
            if progress_bar.text() == "Canceled":
                break

        # Güncellenmiş ilerleme çubuğunu anlık olarak göstermek için
        QApplication.processEvents()
    #result_textbox.setPlainText("Genetik Algoritma Tamamlandı.")
    #self.progress_bar.setValue(iteration)  # İterasyon çubuğunu tam değere ayarla
    #self.progress_bar.setFormat("Genetik Algoritma Tamamlandı. Toplam Geçen Süre: {:.2f} saniye".format(time.time() - start_time))

        print(f"Iterasyon {i + 1} - En iyi fitness: {best_fitness}")
    print("En iyi kromozom:", best_chromosome)
    print("En iyi fitness değeri:", best_fitness)
    return best_chromosome, best_fitness #En iyi kromozomu ve fitness değerini döndürme işlemi

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super(MyMplCanvas, self).__init__(self.fig)
        self.setParent(parent)

    def sizeHint(self):
        w, h = self.get_width_height()
        return QSize(w, h)
class PackingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.rectangles = []
        self.bins = []
        self.progress_bar = None

        #Yeni
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet('font-size: 18px; color: white;')
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Kesme ve Paketleme Problem Uygulaması')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        

        # Üst bölüm (Başlık ve Arka Plan)
        top_layout = QVBoxLayout()
        top_layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel('Kesme ve Paketleme Problem Uygulaması')
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        top_layout.addWidget(title_label)

        """self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(self.iteration)  # İterasyon sayısı kadar maksimum değer
        layout.addWidget(self.progress_bar)"""

        # Butonlar
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)

        self.btn_select_data = QPushButton('Veri Seç', self)
        self.btn_select_data.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.btn_select_data.setStyleSheet('font-size: 16px; background-color: #3498db; color: white;')
        self.btn_select_data.clicked.connect(self.load_data)
        button_layout.addWidget(self.btn_select_data)

        self.btn_next_fit = QPushButton('Next-Fit Yöntemi', self)
        self.btn_next_fit.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.btn_next_fit.setStyleSheet('font-size: 16px; background-color: #27ae60; color: white;')
        self.btn_next_fit.clicked.connect(self.run_next_fit)
        button_layout.addWidget(self.btn_next_fit)

        self.btn_genetic_algorithm = QPushButton('Genetik Algoritma Yöntemi', self)
        self.btn_genetic_algorithm.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.btn_genetic_algorithm.setStyleSheet('font-size: 16px; background-color: #e67e22; color: white;')
        self.btn_genetic_algorithm.clicked.connect(self.run_genetic_algorithm)
        button_layout.addWidget(self.btn_genetic_algorithm)

        self.btn_save_svg = QPushButton('SVG Formatında Kaydet', self)
        self.btn_save_svg.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.btn_save_svg.setStyleSheet('font-size: 16px; background-color: #e74c3c; color: white;')
        self.btn_save_svg.clicked.connect(self.save_as_svg)
        button_layout.addWidget(self.btn_save_svg)

        # Mesajlar için Text Kutusu
        self.result_textbox = QTextEdit()
        self.result_textbox.setAlignment(Qt.AlignCenter)
        self.result_textbox.setStyleSheet('font-size: 18px; background-color: #333333; color: white;')
        self.progress_bar.setParent(self.result_textbox)
        self.progress_bar.setGeometry(10, 105, 820, 25)  # İstediğiniz konuma ve boyuta göre ayarlayabilirsiniz.
        layout.addLayout(top_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.result_textbox)

        # Matplotlib sonucu için alan
        self.canvas = MyMplCanvas(self, width=5, height=4, dpi=100)
        layout.addWidget(self.canvas)

        self.central_widget.setLayout(layout)

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

            self.result_textbox.setPlainText('Veri başarıyla seçildi.')

    def run_next_fit(self):
        if not self.rectangles:
            self.result_textbox.setPlainText('Önce veri seçmelisiniz.')
            return

        self.bins = pack_rectangles(self.rectangles)

        total_rectangles_area = sum(rect.width * rect.height for rect in self.rectangles)
        total_packing_area = bin_width * bin_height
        total_fitted_area = sum(rect.width * rect.height for bin in self.bins for rect in bin.rectangles)
        success_rate = (total_fitted_area / total_rectangles_area) * 100

        self.result_textbox.setPlainText(f'Kesme ve Paketleme Problem Çözümü\nBaşarı Oranı: {success_rate:.2f}%')
        self.visualize_packing()

    def run_genetic_algorithm(self):
        if not self.rectangles:
            self.result_textbox.setPlainText('Önce veri seçmelisiniz.')
            return

        # Genetik algoritma parametreleri
        population_size = 100
        iteration = 10
        crossover_rate = 0.8
        mutation_rate = 0.1

        self.progress_bar.setMaximum(iteration)
        self.progress_bar.setValue(0)


        start_time = time.time()
        best_chromosome, best_fitness = genetic_algorithm(self.rectangles, bin_width, bin_height, population_size, iteration, crossover_rate, mutation_rate,self.progress_bar)
        elapsed_time = time.time() - start_time

        self.progress_bar.setValue(iteration)

        best_rectangles = decode_chromosome(best_chromosome, self.rectangles)
        best_bins = pack_rectangles_genetic(best_rectangles, bin_width, bin_height)

        total_rectangles_area = sum(rect.width * rect.height for rect in self.rectangles)
        total_packing_area = bin_width * bin_height
        total_fitted_area = sum(rect.width * rect.height for bin in best_bins for rect in bin.rectangles)
        success_rate = (total_fitted_area / total_rectangles_area) * 100

        self.result_textbox.setPlainText(f'Genetik Algoritma Çözümü\nBaşarı Oranı: {success_rate:.2f}%')
        self.visualize_packing_genetic(best_bins)

    def visualize_packing(self):
        self.canvas.fig.clear()
        ax = self.canvas.fig.add_subplot(111)

        for i, bin in enumerate(self.bins):
            ax.set_title(f'Bin {i + 1}')
            for j, rect in enumerate(bin.rectangles):
                ax.add_patch(plt.Rectangle((rect.x, rect.y), rect.width, rect.height, fill=True, color='white'))
                ax.add_patch(plt.Circle((rect.x + rect.width / 2, rect.y + rect.height / 2), 0.1, color='black'))
                ax.plot([rect.x, rect.x + rect.width], [rect.y, rect.y], color='black')
                ax.plot([rect.x, rect.x], [rect.y, rect.y + rect.height], color='black')
                ax.plot([rect.x + rect.width, rect.x + rect.width], [rect.y, rect.y + rect.height], color='black')
                ax.plot([rect.x, rect.x + rect.width], [rect.y + rect.height, rect.y + rect.height], color='black')

            for x in range(bin_width):
                for y in range(bin_height):
                    is_empty = True
                    for rect in bin.rectangles:
                        if x >= rect.x and x < rect.x + rect.width and y >= rect.y and y < rect.y + rect.height:
                            is_empty = False
                            break
                    if is_empty:
                        ax.add_patch(plt.Rectangle((x, y), 1, 1, fill=True, color='black'))

        ax.set_xlim(0, bin_width)
        ax.set_ylim(0, bin_height)
        ax.figure.tight_layout()
        self.canvas.draw()

    def visualize_packing_genetic(self,bins):
        self.canvas.fig.clear()
        ax = self.canvas.fig.add_subplot(111)

        for i, bin in enumerate(bins):
            ax.set_title(f'Bin {i + 1}')
            for j, rect in enumerate(bin.rectangles):
                ax.add_patch(plt.Rectangle((rect.x, rect.y), rect.width, rect.height, fill=True, color='white'))
                ax.add_patch(plt.Circle((rect.x + rect.width / 2, rect.y + rect.height / 2), 0.1, color='black'))
                ax.plot([rect.x, rect.x + rect.width], [rect.y, rect.y], color='black')
                ax.plot([rect.x, rect.x], [rect.y, rect.y + rect.height], color='black')
                ax.plot([rect.x + rect.width, rect.x + rect.width], [rect.y, rect.y + rect.height], color='black')
                ax.plot([rect.x, rect.x + rect.width], [rect.y + rect.height, rect.y + rect.height], color='black')

            for x in range(bin_width):
                for y in range(bin_height):
                    is_empty = True
                    for rect in bin.rectangles:
                        if x >= rect.x and x < rect.x + rect.width and y >= rect.y and y < rect.y + rect.height:
                            is_empty = False
                            break
                    if is_empty:
                        ax.add_patch(plt.Rectangle((x, y), 1, 1, fill=True, color='black'))

        ax.set_xlim(0, bin_width)
        ax.set_ylim(0, bin_height)
        ax.figure.tight_layout()
        self.canvas.draw()

    def save_as_svg(self):
        if not self.bins:
            self.result_textbox.setPlainText('Önce veriyi çözmelisiniz.')
            return

        file_dialog = QFileDialog(self)
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_path, _ = file_dialog.getSaveFileName(self, 'SVG Olarak Kaydet', '', 'SVG Files (*.svg)', options=options)
        if file_path:
            self.visualize_packing()
            self.canvas.fig.savefig(file_path, format='svg', bbox_inches='tight')
            self.result_textbox.setPlainText(f'Görüntü başarıyla SVG olarak kaydedildi: {file_path}')

def main():

    app = QApplication(sys.argv)
    mainWin = PackingApp()
    mainWin.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
