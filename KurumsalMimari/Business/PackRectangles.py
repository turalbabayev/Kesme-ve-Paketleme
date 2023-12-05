from Entity.Bin import Bin
from Business.ValidLocation import ValidLocation



class PackingRectangles():

    def is_valid_location(bin,rect,x,y):
        
        validLocation = ValidLocation.is_valid_location(bin,rect,x,y)

        return validLocation

    #Next-Fit Algoritması için Yerleştirme Fonsksiyonu
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

    #Genetik Algoritma için Yerleştirme Fonksiyonu
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

