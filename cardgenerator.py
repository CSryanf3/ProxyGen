from fpdf import FPDF  # fpdf class
import subprocess
import datetime

#static vars
pagew = 210
pageh = 297
spacingw = 63.5
spacingh = 88.9
title_font = [9]
font = "Times"

#global vars
marginw = (pagew - (3 * spacingw)) / 2 #210 is page width
marginh = (pageh - (3 * spacingh)) / 2 #297 is page height
titles = []
subtexts = []
texts = []

def read_text_file(txt_file):
    #getting text from text document
    f = open(txt_file, "r")

    #read rest of file
    for x in f:
        splitarray = x.strip().replace("\n", "").split("/")

        #add title, subtext, and text to arrays
        if (len(splitarray[0]) > 90):
            print("Your title may be too long:", splitarray[0])
        titles.append(splitarray[0])

        if (len(splitarray[1]) > 90):
            print("Your subtext may be too long:", splitarray[1])
        subtexts.append(splitarray[1])

        if (len(splitarray[1]) > 290):
            print("Your card text may be too long, consider changing the font size:", splitarray[2])
        texts.append(splitarray[2])

def testing_wrapping(num_char):
    for x in range(num_char):
        test_string = "X" * x
        titles.append(str(x))
        subtexts.append(test_string)
        texts.append(str(spacingw) + " " + str(spacingh/2))

#pdf class, includes table generation
class PDF(FPDF):
    def card_grid(self, numcards): #for printing the card grid
        i = 0
        for row in range(3):
            for col in range(3):
                if (i >= numcards): #if no more cards to print, stop
                    break
                self.set_xy(marginw + (col) * (spacingw), marginh + row * (spacingh)) #set x & y pointer to spot for next card
                self.multi_cell(spacingw, spacingh, "", border=1, align="L",
                        max_line_height=self.font_size)
                i += 1
            if (i >= numcards): #if no more cards to print, stop
                break
            self.ln()
 
    def card_title(self, titles): #card titles
        self.set_font(style="B")
        i = 0
        for row in range(3):
            for col in range(3):
                if (i >= len(titles)): #if no more cards to print, stop
                    break
                self.set_xy(marginw + (col) * (spacingw), marginh + row * (spacingh)) #set x & y pointer to spot for next card
                self.multi_cell(spacingw, spacingh/4, "\n" + titles[i], align="C",
                        max_line_height=self.font_size)
                i += 1
            if (i >= len(titles)): #if no more cards to print, stop
                break
            self.ln()
        
    def card_subtext(self, subtexts):
        self.set_font(style="")
        i = 0
        for row in range(3):
            for col in range(3):
                if (i >= len(subtexts)):
                    break
                self.set_xy(marginw + (col) * (spacingw), marginh + spacingh/4 + row * (spacingh))
                self.multi_cell(spacingw, spacingh/2, subtexts[i], align="C",
                        max_line_height=self.font_size)
                i += 1
            if (i >= len(subtexts)):
                break
            self.ln()

    def card_text(self, texts): #card text
        self.set_font(style="")
        i = 0
        for row in range(3):
            for col in range(3):
                if (i >= len(texts)): #if no more cards to print, stop
                    break
                self.set_xy(marginw + (col) * (spacingw), marginh + spacingh/4 + row * (spacingh)) #set x & y pointer to spot for next card
                self.multi_cell(spacingw, spacingh * 3/4, texts[i], align="C",
                        max_line_height=self.font_size)
                i += 1
            if (i >= len(texts)): #if no more cards to print, stop
                break
            self.ln()
    
    def print_time(self):
        self.set_font(style="")
        self.set_xy(1, pageh - 6)
        now = datetime.datetime.now()
        self.write(5, now.strftime(("%m/%d/%y %X")))
    
    def page_num(self, page):
        self.set_font(style="")
        self.set_xy(pagew - (len(str(page)) * 3) - 2, pageh - 6)
        self.write(5, str(page))

def generatePdf(options):  
    #inital PDF setup
    pdf = PDF()

    #page set up for font, margins and removing page break
    pdf.set_font(font, size = 15)
    pdf.set_margins(0,0,0)
    pdf.set_auto_page_break(auto=False)

    #adjustable font
    if(options['adj_font']):
        print("testing")

    #page generation
    pages = 0
    maxcards = 9
    while((pages * maxcards) <= len(titles)):
        pdf.add_page('P')

        currenttitles = titles[(pages * maxcards):min(len(titles), ((pages + 1) * maxcards))]
        currentsubtexts = subtexts[(pages * maxcards):min(len(subtexts), ((pages + 1) * maxcards))]
        currenttexts = texts[(pages * maxcards):min(len(texts), ((pages + 1) * maxcards))]

        pdf.card_grid(len(titles) - (pages * maxcards))
        pdf.card_title(currenttitles)
        pdf.card_subtext(currentsubtexts)
        pdf.card_text(currenttexts)

        if(options['timestamp']):
            pdf.print_time()

        if(options['page_num']):
            pdf.page_num(pages + 1)
        
        pages = pages + 1

    #output the pdf
    pdf.output('test.pdf')
    if(options['preview']):
        subprocess.Popen(['test.pdf'],shell=True)