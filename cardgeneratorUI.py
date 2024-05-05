from tkinter import *
from tkinter import font
from tkinter.filedialog import *
from cardgenerator import generatePdf, read_text_file
from functools import partial

# STATIC VARS #
windowWidth = 750
windowLength = 250

# SET UP #
root = Tk()
root.title("ProxyGen")
root.maxsize(windowWidth, windowLength)
root.geometry(f"{windowWidth}x{windowLength}")
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
frame = Frame(root, padx=10, pady=10)
frame.grid(sticky=EW)
frame.grid_columnconfigure(0, weight=1)
frame.grid_rowconfigure(0, weight=1)
i = PhotoImage(width=1, height=1)

# OPTIONS #
options = {
    'adj_font': 0,
    'preview': 0,
    'timestamp': 0,
    'page_num': 0
}

# FUNCTIONS #
# Open file dialog box
def open_file(): 
    file = askopenfilename(filetypes =[("txt files", "*.txt")]) 
    read_text_file(file)
    file_path.insert(END, file)

    #Run button
    Button(run_frame, text = 'Run', image=i, compound='c', command = partial(generatePdf, options),
            justify='center', width = 100, height = 50).grid(column=0, row=0)

#checkbox modify options
def modify_options(option):
    options[option] = 1 - options[option]

# TITLE #
title = Label(frame, text = "ProxyGen", font=('Helvetica', 18, 'bold'))
title.grid(column=0, row=0, pady=5, columnspan=2, sticky=N)

# TEXT FILE SECTION #
#Text file frame
file_frame = Frame(frame)
file_frame.grid(column=0, row=1, pady=10, columnspan=2, sticky=W)

#Select text file title
title_file = Label(file_frame, text = "Select Text File", font=('Helvetica', 13, 'bold'))
title_file.grid(column=0, row=0, columnspan=2, sticky=W)

#Text file button
file_button = Button(file_frame, text ='Browse', command = open_file)
file_button.grid(column=0, row=1)

#Text file label
file_path = Text(file_frame, height=1)
file_path.grid(column=1, row=1, ipadx=2, ipady=2)

# OPTIONS SECTION #
#Options frame
options_frame = Frame(frame)
options_frame.grid(column=0, row=2, pady=10, sticky=W)

#Options title
title_options = Label(options_frame, text = "Options", font=('Helvetica', 13, 'bold'))
title_options.grid(column=0, row=0, columnspan=2, sticky=W)

#Adjustable Font option
font_box = Checkbutton(options_frame, text="Adjustable Font", command=partial(modify_options, "adj_font"))
font_box.grid(column=0, row=1, sticky=W)

#Preview option
preview_box = Checkbutton(options_frame, text="Preview PDF", command=partial(modify_options, "preview"))
preview_box.grid(column=1, row=1, sticky=W)

#Timestamp option
timestamp_box = Checkbutton(options_frame, text="Timestamp", command=partial(modify_options, "timestamp"))
timestamp_box.grid(column=0, row=2, sticky=W)

#Page number option
pagenumber_box = Checkbutton(options_frame, text="Page Number", command=partial(modify_options, "page_num"))
pagenumber_box.grid(column=1, row=2, sticky=W)

# RUN BUTTON #
#Run card generator frame
run_frame = Frame(frame)
run_frame.grid(column=1, row=2, sticky=SE)

root.mainloop()