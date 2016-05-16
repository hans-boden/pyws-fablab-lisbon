# python3
"""
    use ffmpeg as a converter tool to convert flv videos into mp4 format
"""

import os, os.path
import subprocess
import time

class G():
    ffmpeg = r'c:\_h_\_tools_\ffmpeg\bin\ffmpeg.exe'
    args = "-i input.flv -c copy -copyts output.mp4 -nostats -loglevel error"
    flvsource = os.path.abspath(r'.')
    mp4target = os.path.abspath(r'.\new')
    donetarget = os.path.abspath(r'.\done')

def main():    
    assert os.path.exists(G.mp4target)
    assert os.path.exists(G.donetarget)

    tsg = gen_tstamp()
    logfn = "log_{}.txt".format(next(tsg))
    with open(logfn, 'wb') as fo:
        G.fo = fo
        G.fo.write(b"FFMpeg Batch Conversion\n")

        while True:
            flist = list(gen_file_list(G.flvsource, '.flv'))
            print("found {} files".format(len(flist)))

            ans = input("convert how many? - (0 or >0) ")
            if ans == '':
                continue
            if ans == '0':
                break
            try:
                num = int(ans)
            except ValueError:
                print("again ...")
                continue
            convert(flist[:num])

def convert(flist):
    G.fo.write(b"Start converting ")
    G.fo.write(str(len(flist)).encode())
    G.fo.write(b" files\n")
               
    for fn in flist:
        print("\n\nStart conversion: {}\n\n".format(fn))
        G.fo.write(b"\nStart conversion: ")
        G.fo.write(fn.encode('utf-8'))
        G.fo.write(b"\n")
                 
        cmd = [G.ffmpeg]
        cmd.extend(G.args.split())

        cmd[2] = os.path.join(G.flvsource, fn)
        newfn = os.path.splitext(fn)[0] + '.mp4'
        newpath = os.path.join(G.mp4target, newfn)
        cmd[6] = newpath
        if os.path.exists(newpath):
            print("remove {}".format(newfn))
            os.remove(newpath)  
            # pass  # what happens to ffmpeg question?
            # => it is invisible, but can be ansered

        try:
            odata = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as excp:
            print("FFMpeg raised an error", excp)
            odata = b"FFMPeg raised an error\n"
        G.fo.write(odata)
        G.fo.write(b'\n')
        
        donefn = os.path.join(G.donetarget, fn)
        try:
            os.rename(fn, donefn)
        except FileExistsError:
            print("\nouch, fn already exists: {}\n".format(donefn))

        

def gen_file_list(path, ext):
    # Generator for filenames in path
    for fn in os.listdir(path):
        if not os.path.splitext(fn)[1] == ext:
            continue
        yield fn
        
def gen_tstamp():
    # get a timestamp
    while True:
        t = time.time()/367899
        t2 = t-int(t)
        t3 = int(t2*999999)
        yield str(t3)                                

def batch_rename():
    for fn in os.listdir(G.donetarget):
        base, ext = os.path.splitext(fn)
        if ext != ".mp4":
            continue
        oldfn = os.path.join(G.donetarget, fn)
        newfn = os.path.join(G.donetarget, base+'.flv')
        os.rename(oldfn, newfn)
        
# batch_rename()        
main()
