from PIL import Image
from operator import itemgetter


class char_image():

    def __init__(self, char, path='characters/'):
        self.char = char
        
class solver():

    def __init__(self):
        chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
        imgs = [Image.open('characters/%s.png' % (c)) for c in chars]
        self.chars = {}
        for c, i in [(chars[n], imgs[n]) for n in range(len(chars))]:
            self.chars[c] = i

    def create_img_profile(self, img):
        profile = []
        for y in range(img.size[1]):
            p_y = 0
            for x in range(img.size[0]):
                p_y += img.getpixel((x,y))
            profile.append(p_y)
        return profile

    def get_char_profiles(self):
        self.profiles = {}
        for c, i in self.chars.iteritems():
            self.profiles[c] = self.create_img_profile(i)
            

    def get_blackwhite_img(self, origimg):
        black = 0
        white = 255
        # make an all black image
        newimg = Image.new('P', origimg.size, black) 
        his = origimg.histogram()

        values = {}
        for i in range(256):
            values[i] = his[i]
        #colour_masks = [x[0] for x in sorted(values.items(), key=itemgetter(1), reverse=True)[:5]]
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


    def cmp_profiles(self, a, b):
        diff = 0
        for n in range(len(a)):
            diff += a[n] - b[n]
        return diff

    def create_single_char_imgs(self, img, char_positions):
        return [img.crop((c[0], 0, c[1], img.size[1])) for c in char_positions]

    def determine_character(self, img):
        img_profile = self.create_img_profile(img)
        diff = 10000
        char = ''
        for c, p in self.profiles.iteritems():
            if self.cmp_profiles(img_profile, p) < diff:
                char = c
        return c


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

    def solve_captcha():
        pass


iname = "44a250.png"
origimg = Image.open("captchas/" + iname)

s = solver()
s.get_char_profiles()
bwimg = s.get_blackwhite_img(origimg)
charpos = s.find_character_bounds(bwimg)
scimgs = s.create_single_char_imgs(bwimg, charpos)
for i in scimgs:
    print s.determine_character(i)
