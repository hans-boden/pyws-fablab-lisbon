# python3
"""
    create an "art" object from python, svg, a laser cutter, cardboard and some paint
    Round corners contributed by Hugo
    This version is developed further, combining the image and cut functions.
    It tries to be more understandable and with explanations of code and logic.
    And of course eliminates a few (not so) minor errors
"""

import random
import xml.etree.ElementTree as ET
SE = ET.SubElement

class G():
    #  put here all parameters of the process, which we want to control
    #  using numbers directly in the code is usuall the second best solution
    #  declaring parameters here allows to explain their usage in one context
    
    #  the following colors represent the colored papers, which we have available
    #  to make our laser cuts. The number of available coulors may be too small,
    #  depending on the random results, eventually extend the below list by
    #  repeating some colors
    colors = "FCD7AE FAF3C2 F76E5A F5B2C7 EB6184 DB465A C3E4D3 " \
             "BAE9F2 8BC575 7EED5D 208AD2 " \
             "FCD7AE FAF3C2 F76E5A".split()
    #colors = "000066 0000aa 0000ff 006600 00aa00 00ff00 660000 " \
    #         "aa0000 ff0000 aa6600 ccaa00 ffff00 " \
    #         "FCD7AE FAF3C2 F76E5A F5B2C7 EB6184 DB465A C3E4D3 " \
    #         "BAE9F2 8BC575 7EED5D 208AD2".split()
    width, height = 297, 210  # cut medium (card board) size in mm
    marg = 8   # minimum margin between cut lines
    px, py = 5, 5   # position of outer frame: n mm offset from paper margin
    w, h = width - 2*px, height- 2*py # cut size
    rad = marg/2  # global radius for corners

    color_style = "stroke-width:0.5; stroke:#000000; " \
                  "fill-rule: evenodd; fill:#{};"
    cut_style = "stroke-width:0.1; stroke:#ff0000; fill:none"

    layers = []  # list of layers, each layer is a list of tuples

def main():
    myseed = int(random.random() * 100000)
    myseed = 40478  # freeze the random generator
    random.seed(myseed)  # the 'myseed' value appears in the file names

    calculate_layers(G.w, G.h, G.px, G.py, lvl=0)

    arrange_layers()  # change sequence of layers
    
    output_image(myseed)  # output as html file
    output_cutlayers(myseed)  # output as a series of svg files

def arrange_layers():
    # we must draw the layers in a different order from which they were calculated
    new = []
    for lay in G.layers[1:]:
        new.insert(0, lay)
    new.insert(0, G.layers[0])
    G.layers = new
    
def output_image(seed):
    zoom_w = G.width / 2   # zoom 50%
    zoom_h = G.height / 2
    svg = ET.Element('svg', attrib=dict(version="1.1", xmlns="http://www.w3.org/2000/svg",
                            width="{}mm".format(zoom_w), height="{}mm".format(zoom_h),
                            viewBox="0 0 {} {}".format(G.width, G.height),
                            preserveAspectRatio="none"))
    for ndx, layer in enumerate(G.layers):
        pdata = calculate_path(layer)
        color_style = G.color_style.format(G.colors[ndx])
        SE(svg, 'path', attrib=dict(d=pdata, style=color_style))

    with open("./svg/layer{:05d}.html".format(seed), 'wb') as fo:
        fo.write(ET.tostring(svg))

def output_cutlayers(seed):
    for ndx, layer in enumerate(G.layers):
        svg = ET.Element('svg', attrib=dict(version="1.1", xmlns="http://www.w3.org/2000/svg",
                                width="{}mm".format(G.width), height="{}mm".format(G.height),
                                viewBox="0 0 {} {}".format(G.width, G.height),
                                preserveAspectRatio="none"))
        pdata = calculate_path(layer)
        SE(svg, 'path', attrib=dict(d=pdata, style=G.cut_style))

        with open("./svg/layer{:05d}_{}.svg".format(seed, ndx), 'wb') as fo:
            fo.write(ET.tostring(svg))

def calculate_layers(w, h, px, py, lvl):
    
    m1, m2, m3, m4, m5, m6 = ((x+1) * G.marg for x in range(6))
    
    if lvl >= len(G.layers):
        frames = []
        G.layers.append(frames)
        # every new layer starts with a cut of the outer shape
        frames.append( (G.w, G.h, G.px, G.py) )  # outer shape

    frames = G.layers[lvl] # point frames to the current layer

    if lvl > 0:
        #for the very first frame, this is identical to the outer shape
        frames.append( (w, h, px, py) )

    if min(w, h) <= m3:  # small frame can have nothing inside
        return

    split = random.random() > (0.75 - lvl * 0.1)  # probability of a split frame
    # deeper levels are less likely to be split up
    
    if not split or min(w, h) < m5:
        # this frame is not split: random result or frame too small
        calculate_layers(w-m2, h-m2, px+m1, py+m1, lvl+1)
        return

    divide = random.random() 

    if w > h: # split horizontally
        w0 = w - m6
        w1 = m1 + w0 * divide
        w2 = w - m3 - w1
        calculate_layers(w1, h-m2, px+m1,    py+m1, lvl+1)
        calculate_layers(w2, h-m2, px+m2+w1, py+m1, lvl+1)
    else:     # split vertically
        h0 = h - m6
        h1 = m1 + h0 * divide
        h2 = h - m3 - h1
        calculate_layers(w-m2, h1, px+m1, py+m1, lvl+1)
        calculate_layers(w-m2, h2, px+m1, py+m2+h1, lvl+1)
    return


def calculate_path(layer):
    path = []
    for frame in layer:
        w, h, px,py = frame
        path.append(cut_shape(w, h, px, py))
    return ' '.join(path)
                    
def cut_shape(w, h, px, py):
    # translate the shape dimensions into an SVG path
    r = G.rad
    bw = w - 2*r
    bh = h - 2*r
    path = []
    path.append("M {:1.2f},{:1.2f} ".format(px+r, py))
    path.append("l {:1.2f},{:1.2f} ".format(bw, 0))
    path.append("a {:1.2f},{:1.2f},0,0,1,{:1.2f},{:1.2f} ".format(r, r, r, r))
    path.append("l {:1.2f},{:1.2f} ".format(0, bh))
    path.append("a {:1.2f},{:1.2f},0,0,1,{:1.2f},{:1.2f} ".format(r, r, -r, r))
    path.append("l {:1.2f},{:1.2f} ".format(-bw, 0))
    path.append("a {:1.2f},{:1.2f},0,0,1,{:1.2f},{:1.2f} ".format(r, r, -r, -r))
    path.append("l {:1.2f},{:1.2f} ".format(0, -bh))
    path.append("a {:1.2f},{:1.2f},0,0,1,{:1.2f},{:1.2f} ".format(r, r, r, -r))
    return ''.join(path)


if __name__ == '__main__':
    main()
