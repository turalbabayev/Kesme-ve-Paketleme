import matplotlib.pyplot as plt

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = -1
        self.y = -1  # Sığmayan dikdörtgenlerin koordinatları (-1, -1)

class Bin:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rectangles = []

    def add_rectangle(self, rectangle):
        self.rectangles.append(rectangle)

def is_valid_location(bin, rect, x, y):
    if x + rect.width > bin.width or y + rect.height > bin.height:
        return False
    for r in bin.rectangles:
        if (x < r.x + r.width and x + rect.width > r.x and
            y < r.y + r.height and y + rect.height > r.y):
            return False
    return True

def pack_rectangles(rectangles, bin_width, bin_height):
    bins = [Bin(bin_width, bin_height)]

    plt.figure()
    plt.title('Kesme ve Paketleme Problem Çözümü')

    for i, rect in enumerate(rectangles):
        fitted = False
        for bin in bins:
            for y in range(bin.height):
                for x in range(bin.width):
                    if is_valid_location(bin, rect, x, y):
                        rect.x = x
                        rect.y = y
                        bin.add_rectangle(rect)
                        fitted = True
                        visualize_packing(bins, i)  # Her adımda görselleştir
                        break
                if fitted:
                    break
            if fitted:
                break

    return bins

def visualize_packing(bins, step):
    colors = ['#FF5733', '#33FF57', '#5733FF', '#FF57D5', '#33A6FF', "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FFA500", "#FFC0CB", "#800080", "#40E0D0", "#808080", "#A52A2A", "#FFD700", "#E6E6FA"]

    for j, bin in enumerate(bins):
        plt.subplot(1, len(bins), j + 1)
        plt.title(f'Bin {j + 1}')
        for i, rect in enumerate(bin.rectangles):
            color = colors[i % len(colors)]
            plt.gca().add_patch(plt.Rectangle((rect.x, rect.y), rect.width, rect.height, fill=True, color=color))
            plt.text(rect.x + rect.width / 2, rect.y + rect.height / 2, f'W:{rect.width}\nH:{rect.height}', ha='center', va='center', color='white')

        for x in range(bin.width):
            for y in range(bin.height):
                is_empty = True
                for rect in bin.rectangles:
                    if x >= rect.x and x < rect.x + rect.width and y >= rect.y and y < rect.y + rect.height:
                        is_empty = False
                        break
                if is_empty:
                    plt.gca().add_patch(plt.Rectangle((x, y), 1, 1, fill=True, color='black'))

        plt.xlim(0, bin.width)
        plt.ylim(0, bin.height)

    plt.pause(0.5)  # Her adım arasında bekleme süresi (saniye)
    if step < len(bins) - 1:
        plt.clf()  # Sonraki adıma geçmeden önce mevcut adımı temizle

if __name__ == "__main__":
    rectangles = []
    with open("C3_1.txt", "r") as file:
        num_rectangles = int(file.readline().strip())
        bin_width, bin_height = map(int, file.readline().strip().split())

        for _ in range(num_rectangles):
            width, height = map(int, file.readline().strip().split())
            rectangles.append(Rectangle(width, height))
            
    bins = pack_rectangles(rectangles, bin_width, bin_height)

    total_rectangles_area = sum(rect.width * rect.height for rect in rectangles)
    total_packing_area = bin_width * bin_height
    total_fitted_area = sum(rect.width * rect.height for bin in bins for rect in bin.rectangles)
    success_rate = (total_fitted_area / total_rectangles_area) * 100
    plt.suptitle(f'Kesme ve Paketleme Problem Çözümü\nBaşarı Oranı: {success_rate}%', fontsize=14)
    visualize_packing(bins, len(bins) - 1)  # Son adımı göster
    plt.show()  # Sonuçları görüntüle
