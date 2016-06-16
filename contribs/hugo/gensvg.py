# python3
"""
    create an "art" object from python, svg, a laser cutter, cardboard and some paint
"""

import random
import xml.etree.ElementTree as ET
SE = ET.SubElement

class G():
    layers = {}
    colors = "EB6184 FCD7AE DB465A F76E5A F5B2C7 208AD2 FAF3C2 8BC575  C3E4D3 7EED5D BAE9F2".split()
    #  the following colors represent the colored papers, which we have available
    #  to make our laser cuts. So if you prepare your real paper work, use these colors
    #  EB6184 FCD7AE DB465A F76E5A F5B2C7 208AD2 FAF3C2 8BC575  C3E4D3 7EED5D BAE9F2


def main():
    myseed = int(random.random() * 100000)
    #myseed = 3118
    random.seed(myseed)
    print("seed: {}".format(myseed))

    calculate_layer(w=200, h=290, px=0, py=0, lvl=0) #HANS... fail by 1

    root = ET.Element('html')
    head = ET.SubElement(root, 'head')
    ttle = ET.SubElement(head, 'title')
    ttle.text = "I MADE ART"
    body = ET.SubElement(root, 'body')
    ttle = ET.SubElement(body, 'h3')
    ttle.text = "LaserCutCardboxArt"


    svg = SE(body, 'svg', attrib=dict(version="1.1", xmlns="http://www.w3.org/2000/svg",
                                      width="100.0 mm", height="145 mm",
                                      viewBox="0 0 200 290", preserveAspectRatio="none"))
    for lvl in sorted(G.layers.keys()):
        pdata = ''.join(G.layers[lvl])

        SE(svg, 'path', attrib=dict(d=pdata, style="stroke-width:0.1; stroke:#000000; fill:#{}".format(G.colors[lvl])))

    with open("./svg/layer{:05d}.html".format(myseed), 'wb') as fo:
        fo.write(ET.tostring(root))


def calculate_layer(w, h, px, py, lvl):

    r  = 2.9    #round corner radius
    bw = w-2*r
    bh = h-2*r

    m1 = 8      # margin
    m2 = m1+m1
    m3 = m2+m1
    
    if not lvl in G.layers:
        G.layers[lvl] = []
    path = G.layers[lvl]
    path.append("M {:1.2f},{:1.2f} ".format(px+r, py))
    path.append("l {:1.2f},{:1.2f} ".format(bw, 0))
    path.append("a {:1.2f},{:1.2f},0,0,1,{:1.2f},{:1.2f} ".format(r, r, r, r))
    path.append("l {:1.2f},{:1.2f} ".format(0, bh))
    path.append("a {:1.2f},{:1.2f},0,0,1,{:1.2f},{:1.2f} ".format(r, r, -r, r))
    path.append("l {:1.2f},{:1.2f} ".format(-bw, 0))
    path.append("a {:1.2f},{:1.2f},0,0,1,{:1.2f},{:1.2f} ".format(r, r, -r, -r))
    path.append("l {:1.2f},{:1.2f} ".format(0, -bh))
    path.append("a {:1.2f},{:1.2f},0,0,1,{:1.2f},{:1.2f} ".format(r, r, r, -r))

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
