from PIL import Image, ImageDraw, ImageFont

from gui4image import DynamicDisplay


def main():

    size = dimx, dimy = 1700, 900

    im = Image.new("RGB", (dimx, dimy))
    pixels = im.load()  # PixelAccess object, load before starting gui
    draw = ImageDraw.Draw(im)
    gui = DynamicDisplay(im, fps=200, title="Color Bands")

    bands(draw, pixels, size)
    im.completed = True

def bands(draw, pixels, size):
    # FB - 201003151
    # drawing area (xa < xb and ya < yb)
    def counter():
        x = 0
        while True:
            yield x
            x+=1

    row = counter()

    maxIt = 256 # iterations

    dimx, dimy = size
    for name in "cortab1 cortab2 cortab3 cortab4 cortab5 dawn deep_dawn better other " \
                "smooth redwave yellow bandix default".split():
        draw_band(draw, pixels, dimx, next(row), get_band(name), name)


def draw_band(draw, pixels, length, row, cortab, name):
    bandpos = 20 + row*60

    font = ImageFont.truetype("consola.ttf", 15)
    resolution = reso = 2
    for i in range(length//reso):
        cor = cortab[i%len(cortab)]

        for posx in range(reso*i, reso+reso*i):
            for posy in range(bandpos, bandpos+40):
                pixels[posx, posy] = cor

    draw.text((20, bandpos-13), name, font=font)

def get_band(name):
    func = globals().get('f_'+name, None)
    if func:
        return func()
    data = globals().get(name, default)
    prev_color = 0,0,0  # r, g, b colors
    band = []
    for line in data.splitlines():
        line = line.split('#',1)[0].strip()
        if not line:
            continue
        rf, gf, bf, iter = [int(x) for x in line.split()]  # final colors
        rp, gp, bp = prev_color
        prev_color = rf, gf, bf
        rd, gd, bd = rf-rp, gf-gp, bf-bp   # color deltas
        for step in range(iter):
            factor = (step+1) / iter
            rn = rp + int(factor*rd)
            gn = gp + int(factor*gd)
            bn = bp + int(factor*bd)
            band.append((rn, gn, bn))
    return band


def f_cortab1():
    tab = [(i%2*128, i%8*32, i%4*64) for i in range(128)]
    return tab

def f_cortab2():
    tab = [(i%64*4, i%32*8, i%16*16) for i in range(256)]
    return tab

def f_cortab3():
    tab = [(32+i%64*3, 16+i%32*7, 8+i%16*15) for i in range(256)]
    return tab

def f_cortab4():
    tab = [(i,  i%2*128, i%4*64) for i in range(256)]
    return tab

def f_cortab5():
    tab = [(140+(i*3)%100,  150+(i*2)%80, 200-(i*4)%130) for i in range(999)]
    return tab


better = """
    150 220 200   1
    200 100 250  50
    220 250 220   1
    250 120  80  50
    250  80  60   1
    50  220 120  50
    220 250 220   1
    250 120  80  50
    200 100 250   1
    150 220 200  50
"""
smooth = """
    200 255 255   1  # white
     60  60  60  60  # dark grey
     40  40 250  40  # blue
    120 180 255  30  # light blue
    150 240 120  30  # light green
    240 240  60  40  # yellow
    255 100  20  40  # red
    200   0   0  20  # red
    255 180 150  40  # red
    255 255 228  20
    180 120 255  40
     80  60 245  40
     60  60  60  40
"""

redwave = """
    200 255 255   1  # white
    # 120 180 255  20  # light blue
    150 240 120  40  # light green
    255 255  60  60  # yellow
    255 100  20  60  # red
    200   0   0  30  # red
    255 180 150  40  # bright red
    255 255 228  40  # white
    180 120 255  60  # violet
     80  60 245  80  # blue
     60  60  60  80  # dark grey
     40  40 250  80  # blue
     40  20  40 200  # grey
"""

yellow = """
    255 255 200    1
    255 255 100  120
    150 255   0   40
     80 220  40   20
    150 250 120   20
    240 240  60   40
    255 100  20   40
    200   0   0   40
    255 180 150   50
    255 255 228   20
    180 120 255   40
     80  60 245   40
     60  60  60   40
"""

other = """
    220 150  20    1 # yellow
    255 240  50   15 # bright yellow
    255 255 120   30 # light green
    255 220  80   10 # red
    255 180  40   10 # red
    255   0   0  100 # red
    200   0 120  100 # violet
    180   0 180   50 # bright green
      0   0 120  100 # blue
      0  80  80   80 # violet
    220 150  20  200 # blue
"""

dawn = """
      0   0  50    1 # dark blue
     50   0 150    7 # violet
    100   0 200    7 # rose
    150   0 180    6 # rose
    200   0 100    6 # pink
    255   0  50   12 # red
    255  50   0   20 # orange
    255 150   0   22 # orange
    255 200   0   12 # yellow
    255 255   0   12 # yellow
    255 255 100   12 # orange
    255 255 150   10 # orange
    255 255 255   20 # white
    255 255 255  500 # white
    50  255 50   400 # green
      0  80  80   80 # violet
      0   0  50  200 # blue
"""

deep_dawn = """
      0   0  50    1 # dark blue
     20   0 150   30 # violet
    100   0 200   10 # rose
    150   0 180   5 # rose
    200   0 100   5 # pink
    255   0  50   10 # red
    255  50   0   10 # orange
    255 150   0   12 # orange
    255 200   0   12 # yellow
    255 255   0   12 # yellow
    255 255 100   12 # orange
    255 255 150   10 # orange
    255 255 255   20 # white
    255 255 255   50 # white
    50  255 50    50 # green
      0  80  80   80 # violet
      0   0  50  200 # blue
"""

default = """
     80  80  80 1
    180 180 180 1
"""

bandix = """
    100 100 100   1
    120 120 120  10
    250 200   0  20
    100 100 100  10
    """

def test():
    print(get_band(bandix))
    for x in globals():
        print(x)
        if x == 'bandix':
            print(globals()['bandix'])

if __name__ == '__main__':
    #print("test-call"); test()
    main()
