import time

from PIL import Image

from gui4image import DynamicDisplay
from fractal_bands import get_band


class G():
    mbdata = {}

mbsets = """
baby     0.0001    -0.90485     -0.2519
apple    2.2       -0.74587     -0.09966
valley   0.4       -0.74587     -0.09966
nebula   0.3       -1.1         -0.19966
spiral   0.00004   -0.74587     -0.09966
wave     0.000038  -0.746034     0.099985
clumsy   0.0014    -0.10340      0.92215
pastry   0.000057  -0.10485      0.92206
"""
size_s =  450, 300  # small
size_m =  900, 600  # medium
size_l = 1500, 900  # large
size_x = 1920,1080  # extra large
size_h = 3000,2000  # huge
size_g = 4500,3000  # giant

def main():
    parse_mbsets(mbsets)

    mandelbrot('clumsy', 'smooth', size_s, 500)

def mandelbrot(mbname, color_name, size, depth):
    im = Image.new("RGB", size)
    im.completed = False
    gui = DynamicDisplay(im, fps=10, title="MB {} {} {}".format(mbname, color_name, depth))

    mat = draw_mb(im, size, mbname, color_name, depth)
    im.completed = True
    return mat

def draw_mb(image, size, mbname, color_name, depth):

    start = time.time()
    cortab = get_band(color_name)
    zoom = G.mbdata[mbname]['zoom']
    cx = G.mbdata[mbname]['xpos']
    cy = G.mbdata[mbname]['ypos']

    pixels = image.load()  # PixelAccess object, load before starting gui

    dimx, dimy = size

    ratio = float(dimx)/float(dimy)
    xa = cx - zoom * ratio
    xb = cx + zoom * ratio
    ya = cy - zoom
    yb = cy + zoom
    print("coordinates: x={}..{}, y={}..{}".format(xa,xb,ya,yb))
    xcoords = [(x, xa + x * (xb-xa)/(dimx-1)) for x in range(dimx)]
    ycoords = [(y, ya + y * (yb-ya)/(dimy-1)) for y in range(dimy)]

    for y, cy in ycoords:
        for x, cx in xcoords:
            c = complex(cx, cy)
            z = 0
            for i in range(depth):
                if abs(z) > 2.0:
                    pixels[x, y] = cortab[i%len(cortab)]
                    break
                z = z * z + c
            else:
                pixels[x, y] = (0,0,0)
    print("finished after {:1.1f}".format(time.time()-start))
    return

def parse_mbsets(text):

    for line in text.splitlines():
        line = line.split('#',1)[0].strip()
        if not line:
            continue
        tup = line.split()
        name = tup[0]
        zoom, xpos, ypos = [float(x) for x in tup[1:4]]
        G.mbdata[name] = dict(name=name, zoom=zoom, xpos=xpos, ypos=ypos)


if __name__ == '__main__':
    main()
