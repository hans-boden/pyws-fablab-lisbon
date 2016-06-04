# python3
'''
    Load font files from the Windows font folder, zip and convert them into
    a base64 data stream. The font data is written to a .py file,
    together with a few lines of python code, which unpacks the font files.
'''

import zipfile
import io
import base64

class G():
    srcfont = r'C:\windows\fonts\consola{}.ttf'
    trgname = 'monolith{}.ttf'
    fontspec = (('', 'r'), ('b','b'), ('i','i'), ('z','bi'))
    
sio = io.BytesIO()
with zipfile.ZipFile(sio, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
    for fss, fst in G.fontspec:
        fn = G.srcfont.format(fss)
        name = G.trgname.format(fst)
        zf.write(fn, arcname=name)
xio = io.BytesIO(sio.getbuffer())
bdata = xio.read()
data = base64.b64encode(bdata)
with open("monolith.py", 'wb') as fo:
    fo.write(b"""# python3
'''\n    decode and unzip font files and put them into the kivy fonts path
    this script is created programmatically, search for packmono.py\n'''
import kivy\nimport zipfile\nimport io\nimport base64\nimport os.path\n
b64data = '''\n""")
    for p in range(0, len(data), 128):
        fo.write(data[p:p+128]+b'\n    ')
    fo.write(b"""'''\n
tpath = os.path.join(kivy.__path__[0], r'data\\fonts')
sio = io.BytesIO(base64.b64decode(b64data))
with zipfile.ZipFile(sio) as zf:
    zf.extractall(path=tpath)\n""")
             
