from PIL import Image
from operator import itemgetter


class captchasolver():

    def __init__(self):
        chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
        imgs = [Image.open('characters/%s.png' % (c)) for c in chars]
        self.chars = {}
        for c, i in [(chars[n], imgs[n]) for n in range(len(chars))]:
            self.chars[c] = i
       

    def get_blackwhite_img(self, origimg):
        black = 0
        white = 255
        # make an all black image
        newimg = Image.new('P', origimg.size, black) 
        his = origimg.histogram()

        values = {}
        for i in range(256):
            values[i] = his[i]
        colour_mask = sorted(values.items(), key=itemgetter(1), reverse=True)[0][0]

        for y in range(origimg.size[1]):
            for x in range(origimg.size[0]):
                pix = origimg.getpixel((x,y))[0]
                if pix == colour_mask:
                    newimg.putpixel((x,y), white)

        return newimg


    def find_character_bounds(self, img):
        inchar = False
        foundchar=False
        start = 0
        end = 0
        char_positions = []
        # we want to get a verticle strip of pixels and check if they
        #  are mostly (well 15%) black, if so we are in a character
        allwhite = 255 * img.size[1]
        tolerance = 255 * (img.size[1] * 0.15)
        for x in range(img.size[0]):
            strip = allwhite
            for y in range(img.size[1]):
                strip -= img.getpixel((x,y))
            if strip > tolerance:
                inchar = True
            if foundchar == False and inchar == True:
                foundchar = True
                start = x
            if foundchar == True and inchar == False:
                foundchar = False
                end = x
                char_positions.append((start,end))
            inchar = False
        return char_positions


    def create_single_char_imgs(self, img, char_positions):
        return [img.crop((c[0], 0, c[1], img.size[1])) for c in char_positions]


    def compare_image(self, charimg, img, position):
        start = 0
        end = 1
        diff_pixels = [0.0, 0.0]
        num_pixels = 0.0

        for x in range(charimg.size[0]):
            for y in range(charimg.size[1]):
                # we can go out of bounds here, careful!
                num_pixels += 1
                char_pixel = charimg.getpixel((x,y))
                if char_pixel != img.getpixel((x + position[start],y)):
                    diff_pixels[start] += 1
                if char_pixel != img.getpixel((x + position[end] - charimg.size[0],y)):
                    diff_pixels[end] += 1

        return 1 - (min(diff_pixels) / num_pixels)


    def determine_character(self, img, position):
        start = position[0]
        end = position[1]
        best_fit = ''
        best_score = 0

        for c, i in self.chars.iteritems():
            score = self.compare_image(i, img, position)
            if score > best_score:
                best_score = score
                best_fit = c

        return best_fit


    def write_single_char_imgs(self, imgs, prefix="charimg-"):
        count = 0
        for i in imgs:
            i.save('%s%d.png' % (prefix, count))
            count += 1

    def write_separator_image(self, img, char_positions):
        for i in chars:
            x = i[0]
            for y in range(img.size[1]):
                img.putpixel((x,y), 100)
            x = i[1]
            for y in range(img.size[1]):
                img.putpixel((x,y), 150)
        img.save("sep.png")

    def solve_captcha(self, origimg):
        bwimg = self.get_blackwhite_img(origimg)
        charpos = self.find_character_bounds(bwimg)
        cap = ''
        for cp in charpos:
            cap += self.determine_character(bwimg, cp)
        return cap


# instantiate the captcha solver once
solver = captchasolver()

def solve_captcha(img):
    return solver.solve_captcha(img)





# For testing
if __name__ == "__main__":
    test_imgs = ["03699a.png", "2eec07.png", "44a250.png", "6ba9ba.png", "8955bc.png",
                 "27213b.png", "3daebc.png", "5a4a58.png", "6c5430.png", "8b1a6c.png",
                 "27e6f3.png", "42190f.png", "684dc1.png", "74da1d.png", "d0e76d.png"]
    s = captchasolver()
    failed = 0

    for f in test_imgs:
        print "Solving %s ..." % (f),
        img = Image.open("captchas/" + f)
        cap = s.solve_captcha(img)
        if f.split('.')[0] != cap:
            failed += 1
            print "%s FAILURE" % (cap)
        else:
            print "%s SUCCESS" % (cap)

    print "Failed to solve %d of %d" % (failed, len(test_imgs))
