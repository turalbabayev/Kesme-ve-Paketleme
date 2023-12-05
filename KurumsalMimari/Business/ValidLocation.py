
class ValidLocation():
    #Uygun Konum Belirleme Fonksiyonu
    def is_valid_location(bin, rect, x, y):
        if x + rect.width > bin.width or y + rect.height > bin.height:
            return False
        for r in bin.rectangles:
            if (x < r.x + r.width and x + rect.width > r.x and
                y < r.y + r.height and y + rect.height > r.y):

                return False
        return True