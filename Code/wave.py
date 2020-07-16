import tkinter as tk
from tkinter import *
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.filedialog import askopenfilename



class waveformViewer():
    def __init__(self):
        self.root= Tk()

        #menu
        self.menu()

        #top row
        self.topframe = Frame(self.root)
        self.topframe.pack()
        self.top()

        #Bottom Row
        self.botframe= Frame(self.root)
        self.botframe.pack( side = BOTTOM )
        
        #left
        self.leftframe = Frame(self.botframe)
        self.leftframe.pack( side = LEFT )
        self.left1 = Frame(self.leftframe)
        self.left1.pack()
        self.left2 = Frame(self.leftframe)
        self.left2.pack()
        self.left3 = Frame(self.leftframe)
        self.left3.pack()
        self.sst()
        self.typeSig()
        self.Filter()

        #right
        self.rightframe = Frame(self.botframe)
        self.rightframe.pack( side = LEFT )
        self.graph()

        #start
        self.root.mainloop()

    def top(self):
        for i in range(4):
            self.button1 = Button(self.topframe, text="cut")
            self.button1.pack( side = LEFT)

            self.button2 = Button(self.topframe, text="paste")
            self.button2.pack(side=LEFT)
        
        self.fromlabel=Label(self.topframe,text='From: ')
        self.fromlabel.pack(side=LEFT)

        self.From = Text(self.topframe, height=1,width=10)
        self.From.pack(side=LEFT)
        
        self.tolabel=Label(self.topframe,text='To: ')
        self.tolabel.pack(side=LEFT)

        self.To = Text(self.topframe, height=1,width=10)
        self.To.pack(side=LEFT)

    def sst(self):
        self.label=Label(self.left1,text='SST')
        self.label.pack(side=TOP)

        self.listbox = Listbox(self.left1) 
        self.listbox.pack(side = LEFT, fill = BOTH) 
          
        self.scrollbar = Scrollbar(self.left1) 
        self.scrollbar.pack(side = RIGHT, fill = BOTH) 
        for i in range(20): 
            self.listbox.insert(END, "file "+str(i)) 
        self.listbox.config(yscrollcommand = self.scrollbar.set) 
        self.scrollbar.config(command = self.listbox.yview)

    def typeSig(self):
        self.label1=Label(self.left2,text='Type | Signals')
        self.label1.pack(side=TOP)

        self.listbox1 = Listbox(self.left2) 
        self.listbox1.pack(side = LEFT, fill = BOTH) 
          
        self.scrollbar1 = Scrollbar(self.left2) 
        self.scrollbar1.pack(side = RIGHT, fill = BOTH) 
        for i in range(20): 
            self.listbox1.insert(END, "wire "+str(i)) 
        self.listbox1.config(yscrollcommand = self.scrollbar1.set) 
        self.scrollbar1.config(command = self.listbox1.yview)

    def Filter(self):
        self.flabel=Label(self.left3,text='Filter: ')
        self.flabel.pack(side=LEFT)

        self.filter = Text(self.left3, height=1,width=10)
        self.filter.pack(side=LEFT)
    
    def graph(self):
        data1 = {'Country': ['US','CA','GER','UK','FR'],
        'GDP_Per_Capita': [45000,42000,52000,49000,47000]}
        df1 = DataFrame(data1,columns=['Country','GDP_Per_Capita'])
        figure1 = plt.Figure(figsize=(6,5), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, self.rightframe)
        bar1.get_tk_widget().pack()
        df1 = df1[['Country','GDP_Per_Capita']].groupby('Country').sum()
        df1.plot(kind='bar', legend=True, ax=ax1)
        ax1.set_title('Country Vs. GDP Per Capita')

    def openFile(self):
        filename = askopenfilename()
        self.open.configure(text=filename)

    def read(self):
        try:
            #Tk().withdraw()
            filename = 'map9v3_tb.vcd'#askopenfilename()   
            file=open(filename,'r')
        except:
            print('file not found')
            return

        wires={}
        for line in file.readlines():
            if '$var' in line:
                params=line.split()
                print(params)

        print(self.variables)

    def menu(self):
        def donothing(self):
            pass
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=donothing)
        filemenu.add_command(label="Open", command=self.openFile)
        filemenu.add_command(label="Save", command=donothing)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)      
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Cut", command=donothing)
        editmenu.add_command(label="Copy", command=donothing)
        editmenu.add_command(label="Paste", command=donothing)
        editmenu.add_command(label="Duplicate Line", command=donothing)
        editmenu.add_command(label="Toggle Case", command=donothing)
        menubar.add_cascade(label="Edit",menu=editmenu)
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=donothing)
        helpmenu.add_command(label="About...", command=donothing)
        menubar.add_cascade(label="Help", menu=helpmenu)
        self.root.config(menu=menubar)

wf=waveformViewer()
