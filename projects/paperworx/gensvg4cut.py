# python3
"""
    create an "art" object from python, svg, a laser cutter, cardboard and some paint
    Round corners contributed by Hugo
"""

import random
import xml.etree.ElementTree as ET
SE = ET.SubElement

class G():
    layers = {}
    #  the following colors represent the colored papers, which we have available
    #  to make our laser cuts.
    colors = "FCD7AE FAF3C2 F76E5A F5B2C7 EB6184 DB465A C3E4D3 BAE9F2 8BC575 7EED5D 208AD2".split()

    rad = 2.9  # global radius for corners
    px, py = 4, 4      # position of outer frame: 4 mm offset from paper margin
    w, h =  202, 289   # size of outer frame: 8 mm smaller than paper size

    color_style = "stroke-width:0.1; stroke:#000000; fill-rule: evenodd; fill:#{};"
    cut_style = "stroke-width:0.1; stroke:#ff0000; fill:none"

def main():
    myseed = int(random.random() * 100000)
    #myseed = 7948
    random.seed(myseed)
    print("seed: {}".format(myseed))

    calculate_layer(w=G.w, h=G.h, px=G.px, py=G.py, lvl=0)

    for lvl in sorted(G.layers.keys()):
        svg = ET.Element('svg', attrib=dict(version="1.1", xmlns="http://www.w3.org/2000/svg",
                                      width="105.0mm", height="148.5mm",
                                      viewBox="0 0 210 297", preserveAspectRatio="none"))
        pdata = ''.join(G.layers[lvl])
        color_style = G.color_style.format(G.colors[lvl])
        SE(svg, 'path', attrib=dict(d=pdata, style=G.cut_style)) #color_style))

        with open("./svg/layer{:05d}_{}.svg".format(myseed, lvl), 'wb') as fo:
            fo.write(ET.tostring(svg))

def cut_shape(w, h, px, py):
    r = G.rad
    path = []
    path.append("M {:1.2f},{:1.2f} ".format(px+r, py))
    path.append("l {:1.2f},{:1.2f} ".format(w, 0))
    path.append("a {:1.2f},{:1.2f},0,0,1,{:1.2f},{:1.2f} ".format(r, r, r, r))
    path.append("l {:1.2f},{:1.2f} ".format(0, h))
    path.append("a {:1.2f},{:1.2f},0,0,1,{:1.2f},{:1.2f} ".format(r, r, -r, r))
    path.append("l {:1.2f},{:1.2f} ".format(-w, 0))
    path.append("a {:1.2f},{:1.2f},0,0,1,{:1.2f},{:1.2f} ".format(r, r, -r, -r))
    path.append("l {:1.2f},{:1.2f} ".format(0, -h))
    path.append("a {:1.2f},{:1.2f},0,0,1,{:1.2f},{:1.2f} ".format(r, r, r, -r))
    return ''.join(path)
    
def calculate_layer(w, h, px, py, lvl):

    bw = w - 2*G.rad
    bh = h - 2*G.rad

    m1 = 8      # margin
    m2 = m1+m1
    m3 = m2+m1
    
    if not lvl in G.layers:
        G.layers[lvl] = []
        path = G.layers[lvl]
        path.append(cut_shape(w=G.w-6, h=G.h-6, px=G.px, py=G.py))  # cut outer shape

    if lvl > 0:    
        path = G.layers[lvl-1]
        path.append(cut_shape(w=bw, h=bh, px=px, py=py))

    if min(w, h) < 3.01 * m1 : return

    if random.random() < (0.3 + lvl * 0.1):
        # deeper levels are less likely to be split up
        calculate_layer(w-m2, h-m2, px+m1, py+m1, lvl+1)
        return

    divide = random.random() * 0.7 + 0.15 # a value between 0.15 and 0.85

    if w > h: # split horizontally
        w0 = w - m3
        w1 = w0 * divide
        w2 = w0-w1
        calculate_layer(w1, h-m2, px+m1,    py+m1, lvl+1)
        calculate_layer(w2, h-m2, px+m2+w1, py+m1, lvl+1)
    else:     # split vertically
        h0 = h - m3
        h1 = h0 * divide
        h2 = h0-h1
        calculate_layer(w-m2, h1, px+m1, py+m1, lvl+1)
        calculate_layer(w-m2, h2, px+m1, py+m2+h1, lvl+1)
    return


if __name__ == '__main__':
    main()
