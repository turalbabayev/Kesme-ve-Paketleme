class Bin:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rectangles = [] #Yerleştirilecek alandaki dikdörtgenlerin tutulduğu liste
        self.fitness = 0 #Yerleştirilen dikdörtgenlerin alanının toplamı

    def add_rectangle(self, rectangle):
        self.rectangles.append(rectangle)
        self.fitness += rectangle.width * rectangle.height #Yerleştirilen dikdörtgenin alanını fitness değerine ekleme işlemi