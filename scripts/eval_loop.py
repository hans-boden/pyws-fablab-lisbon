# python3
""" Interpret text lines from a file and produce output similar to the Python shell

Each line is treated ether as expression (v=evaluate) or as statement (x=execute)
"""
import sys
from io import StringIO
from reportlab.pdfgen.canvas import Canvas

infile  = 'source\\oots_{}_commands.txt'
outfile = 'output\\oots_{}_resolved.{}'

output_hdr = """
   ###    Python Shell Simulator    ###
      Execute statements from the '{}'-command set

   A lines, which starts with '>>>' shows the shell input, '...' is for multiline input
   '==>' shows the result of the evaluation, a 'p()'-line shows printed output
   '#' is for comment lines.

"""
cor_red = (1.0, 0.3, 0.0)
cor_vio = (0.5, 0.0, 0.6)
cor_tur = (0.0, 0.1, 0.8)
cor_blu = (0.6, 0.0, 0.6)
cor_grn = (0.0, 0.7, 0.0)
cor_blk = (0.0, 0.0, 0.0)
cor_gry = (0.6, 0.6, 0.6)

cortab = {}
cortab['>'] = cor_blk  # statement
cortab['.'] = cor_blk  # statement continued
cortab['~'] = cor_tur  # evaluation
cortab['?'] = cor_blu  # print output
cortab['!'] = cor_red  # error
cortab['#'] = cor_grn  # comment



def xmain():
    command_sets = {'F1': 'Functions(1)', 'C': 'Collections',
                    'V': 'Variables', 'HT1': 'HowTo(1)',
                    'B': 'Basic', 'T': 'Test'}

    for tag in ('HT1',):  #'C', 'T', 'F1', 'B'):
        cmdset = command_sets[tag]
        oots_script(tag, cmdset)


def oots_script(tag, cmdset):
    print("\nProcess OOTS Script: {} - {}".format(tag, cmdset))
    lines = get_lines(infile.format(cmdset))
    rc, data = capture(oots_evaluation, lines)

    text_output(data, cmdset, tag)
    pdf_output(data, cmdset, tag)

def text_output(data, cmdset, tag):
    with open(outfile.format(cmdset, 'txt'), 'w') as fo:
        fo.write(output_hdr.format(cmdset))
        for _, prefix, text in oots_parse(data.splitlines(), tag):
            fo.write(prefix + text + '\n')

def pdf_output(data, cmdset, tag):
    pdfw = OotsSlider(outfile.format(cmdset, 'pdf'), cmdset)
    for tagtype, prefix, text in oots_parse(data.splitlines(), tag):
        pdfw.putline(tagtype, prefix, text)
    pdfw.close()

def oots_parse(lines, tag):
    lino = 0
    linodigits = 3
    numformat = '{:03d}'
    nonumber = ' '*linodigits

    prefixformat = '{}{} '
    notag = prefixformat.format(' '*len(tag), ' '*linodigits)
    otag = {'p':'    ', '>': '>>> ', '.':'... ',
            '~':'==> ', '!':'err!', '#':'  # ', '?':'p() '}
    for line in lines:
        if '' == line.strip():
            yield '0', '', ''   # empty line
            continue

        if line[0] == '~':
            tagtype = line[1]
            data = line[3:]
        else:
            tagtype = '?'
            data = line

        if tagtype == '>':  # only command tags are numbered
            lino += 1
            numstr = numformat.format(lino)
            prefix = prefixformat.format(tag, numstr)
        else:
            prefix = notag

        yield tagtype, prefix + otag[tagtype], data

def oots_evaluation(lines):
    # the print() output of this function is mixed with the output of executed/evaluated
    # print statements. To get one continuous stream of output, we must print.
    prepend = ''
    for line in lines:
        # line = line.strip()
        if not line:
            print()
            continue
        ltype = line[0]
        text = line[2:]
        text = text.replace('°', '"')

        if ltype == '#':  # comment
            print('~#', text)
            continue

        if ltype == 'p':  # page header (major comment)
            print('~p', text)
            continue

        if ltype == 'j':  # statement, which will be continued (join)
            if prepend:
                print("~.", text)
            else:
                print("~>", text)
            prepend += text + '\n'

        if ltype == 'v':   # expression which will be evaluated
            if prepend:
                print("~.", text)
                text = prepend + text
                prepend = ''
            else:
                print("~>", text)

            try:
                r = eval(text)
                if not r is None:
                    print("~~", repr(r))  # evaluation result
            except Exception as e:
                print("~!",repr(e))   # exception
            continue

        # y and z statements may only be used between j statements
        if ltype == 'y':  # display only statement
            print("~.", text)
        if ltype == 'z':  # execute only
            prepend += text + '\n'

        if ltype == 'x':    # expression will be executed
            if prepend:
                print("~.", text)
                text = prepend + text + '\n'
                prepend = ''
            else:
                print("~>", text)
            try:
                #print("exec code:\n", text)
                exec(text)
            except Exception as e:
                print("~!", repr(e))

def capture(func, *more, **keywords):
    """ execute any function and return the stdout data"""
    data = ''

    saved_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        rc = func(*more, **keywords)
    finally:
        data = sys.stdout.getvalue()
        sys.stdout.close()
        sys.stdout = saved_stdout
    return rc, data

def get_lines(filename):
    with open(filename, mode='r', encoding="utf-8") as fi:
        for line in fi:
            yield line.rstrip()

class OotsSlider():
    def __init__(self, filename, cmdset):
        self.filename = filename
        self.page_dimx, self.page_dimy = 600.0, 400.0
        self.code_font_size = 11
        self.max_line_offs = 16
        self.code_font_width = self.code_font_size * 0.6
        self.code_margins = (70, 30, 30, 50)  # top, bottom, left, right
        self.text_posx = self.code_margins[2] + self.code_font_width * 12  # offset behind
        # prefix
        self.pageno = 0

        self.pdf = Canvas(self.filename, pagesize=(self.page_dimx, self.page_dimy))
        # page content
        self.page_title = 'OOTS Command Evaluation'
        self.page_foot_left = 'OOTS Script: '+cmdset
        self.page_foot_right = 'Python Workshop'
        self.code_lines = []

    def putline(self, ltype, prefix='', line=''):
        if ltype == 'p':
            self._newpage()
            self.page_title = line
            return
        self.code_lines.append((ltype, prefix, line))

    def yfromtop(self, offs):
        return self.page_dimy - offs

    def close(self):
        self._newpage()
        self.pdf.save()

    def set_text(self,title=None, foot_left=None, foot_right=None):
        if title:
            self.page_title = title
        if foot_left:
            self.page_foot_left = foot_left
        if foot_right:
            self.page_foot_right = foot_right

    def _newpage(self):
        if not self.code_lines:
            return
        self._show_frame()
        self._show_code()
        self.pdf.showPage()

    def _show_code(self):
        nol = len(self.code_lines)
        space = self.page_dimy - self.code_margins[0] - self.code_margins[1]
        yoffs = min(self.max_line_offs, space / nol)
        print("lines {}, space {}, yoffs {}".format(nol, space, yoffs))
        if yoffs < self.code_font_size:
            print("warning, too many lines on page", self.pageno)
        ypos = self.code_margins[0]
        for line in self.code_lines:
            self._show_codeline(ypos, line)
            ypos += yoffs
        self.code_lines = []   # clear list

    def _show_codeline(self, ypos, line_item):
        # print("ypos {}".format(ypos), line_item)
        ltype, prefix, line = line_item
        if ltype == '0':  # empty line
            return
        cor = cortab[ltype]
        self.putcode(self.code_margins[2], ypos, cor_gry, prefix)
        if ltype == '#':
            self.puttext(self.text_posx, ypos, cor, line)
        else:
            self.putcode(self.text_posx, ypos, cor, line, bold=False)
        pass

    def puttext(self, xpos, ypos, cor, text):
        self.pdf.setFont("Times-Roman", self.code_font_size)
        self.pdf.setFillColorRGB(cor[0], cor[1], cor[2])
        self.pdf.drawString(xpos, self.yfromtop(ypos), text)

    def putcode(self, xpos, ypos, cor, text, bold=False):
        pos = text.rfind('#')  # a comment?
        if pos > -1:
            code, comment = text[:pos+1], text[pos+1:]
            cpos = xpos + self.code_font_width * len(code)
            self.puttext(cpos, ypos, cortab['#'], comment)
            text = code
        if bold and cor == cor_blk:
            self.pdf.setFont("Courier-Bold", self.font_size)
        else:
            self.pdf.setFont("Courier", self.code_font_size)
        self.pdf.setFillColorRGB(cor[0], cor[1], cor[2])
        self.pdf.drawString(xpos, self.yfromtop(ypos), text)

    def _show_frame(self):
        if self.page_title:
            self.pdf.setFont("Helvetica-Bold", 20)
            self.pdf.setFillColorRGB(0.5, 0.5, 0.5)
            ypos = self.yfromtop(self.code_margins[0]-30)
            self.pdf.drawString(self.text_posx, ypos, self.page_title )

        ypos = self.yfromtop(self.page_dimy - self.code_margins[1] + 12)
        self.pdf.setFont("Helvetica", 12)
        self.pdf.setFillColorRGB(0.3, 0.3, 0.3)

        self.pageno += 1
        xpos = self.page_dimx * 0.45
        self.pdf.drawString(xpos, ypos, str(self.pageno))

        if self.page_foot_left:
            self.pdf.drawString(self.code_margins[2], ypos, self.page_foot_left )
        if self.page_foot_right:
            self.pdf.drawRightString(self.page_dimx - self.code_margins[3],
                                     ypos, self.page_foot_right )



if __name__ == '__main__':
    xmain()
