import matplotlib.pyplot as plt
import random
import math

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = -1
        self.y = -1  # Sığmayan dikdörtgenlerin koordinatları (-1, -1)
        self.rotated = False # Dikdörtgenin döndürülüp döndürülmediğini belirtir

class Bin:
    def __init__(self, width, height):
        self.width = width #Yerleştirilecek alanın genişliği
        self.height = height #Yerleştirilecek alanın uzunluğu
        self.rectangles = [] #Yerleştirilecek alandaki dikdörtgenlerin tutulduğu liste
        self.fitness = 0 #Yerleştirilen dikdörtgenlerin alanının toplamı

    def add_rectangle(self, rectangle): #Dikdörtgen Ekleme Fonksiyonu
        self.rectangles.append(rectangle) #Dikdörtgenlerin tutulduğu listeye gelen uygun dikdörtgeni ekleme işlemi
        self.fitness += rectangle.width * rectangle.height #Yerleştirilen dikdörtgenin alanını fitness değerine ekleme işlemi

def is_valid_location(bin, rect, x, y): #Uygun Yer Bulma Fonksiyonu
    if x + rect.width > bin.width or y + rect.height > bin.height: 
        return False
    for r in bin.rectangles:
        if (x < r.x + r.width and x + rect.width > r.x and
            y < r.y + r.height and y + rect.height > r.y):
            return False
    return True

def pack_rectangles(rectangles, bin_width, bin_height):
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

def visualize_packing(bins):
    plt.figure()
    colors = ['#FF5733', '#33FF57', '#5733FF', '#FF57D5', '#33A6FF', "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FFA500", "#FFC0CB", "#800080", "#40E0D0", "#808080", "#A52A2A", "#FFD700", "#E6E6FA"]

    for i, bin in enumerate(bins):
        plt.subplot(1, len(bins), i + 1)
        plt.title(f'Bin {i + 1}')
        for j, rect in enumerate(bin.rectangles):
            color = colors[j % len(colors)]
            plt.gca().add_patch(plt.Rectangle((rect.x, rect.y), rect.width, rect.height, fill=True, color=color))

        for x in range(bin.width):
            for y in range(bin.height):
                is_empty = True
                for rect in bin.rectangles:
                    if x >= rect.x and x < rect.x + rect.width and y >= rect.y and y < rect.y + rect.height:
                        is_empty = False
                        break
                if is_empty:
                    plt.gca().add_patch(plt.Rectangle((x, y), 1, 1, fill=True, color='black'))  # Boş alanları siyahla boyar

        plt.xlim(0, bin.width)
        plt.ylim(0, bin.height)

    plt.show()



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
        bins = pack_rectangles(decoded_rectangles, bin_width, bin_height) #Dikdörtgenleri yerleştirme işlemi
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

def genetic_algorithm(rectangles, bin_width, bin_height, population_size, iteration, crossover_rate, mutation_rate): #Genetik Algoritma Fonksiyonu
    population = create_population(rectangles, population_size) #Rastgele bir popülasyon oluşturma işlemi
    best_chromosome = None #En iyi kromozomu tutan değişken
    best_fitness = 0 #En iyi fitness değerini tutan değişken
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

        print(f"Iterasyon {i + 1} - En iyi fitness: {best_fitness}")
    print("En iyi kromozom:", best_chromosome)
    print("En iyi fitness değeri:", best_fitness)
    return best_chromosome, best_fitness #En iyi kromozomu ve fitness değerini döndürme işlemi
    
if __name__ == "__main__":
    rectangles = []
    with open("Data/C2_1.txt", "r") as file:
        num_rectangles = int(file.readline().strip())
        bin_width, bin_height = map(int, file.readline().strip().split())

        for _ in range(num_rectangles):
            width, height = map(int, file.readline().strip().split())
            rectangles.append(Rectangle(width, height))
            
    #GA parametreleri
    population_size = 2 #Popülasyon boyutu
    iteration = 1 #Iterasyon sayısı
    crossover_rate = 0.8 #Çaprazlama oranı
    mutation_rate = 0.1 #Mutasyon oranı

    best_chromosome, best_fitness = genetic_algorithm(rectangles, bin_width, bin_height, population_size, iteration, crossover_rate, mutation_rate) #Genetik algoritmayı çalıştırma işlemi
    best_rectangles = decode_chromosome(best_chromosome, rectangles) #En iyi kromozomu dikdörtgenlere dönüştürme işlemi
    best_bins = pack_rectangles(best_rectangles, bin_width, bin_height) #En iyi dikdörtgenleri yerleştirme işlemi
    
    total_rectangles_area = sum(rect.width * rect.height for rect in rectangles)
    print(total_rectangles_area)
    total_packing_area = bin_width * bin_height
    print(total_packing_area)
    total_fitted_area = sum(rect.width * rect.height for bin in best_bins for rect in bin.rectangles)
    success_rate = (total_fitted_area / total_rectangles_area) * 100
    plt.suptitle(f'C2_1 Datası \nBaşarı Oranı: {success_rate}%', fontsize=14)
    visualize_packing(best_bins) #Yerleştirme sonucunu görselleştirme işlemi
