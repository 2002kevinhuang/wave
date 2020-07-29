import tkinter as tk
from tkinter import ttk
import ttkwidgets
from tkinter import *
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.filedialog import askopenfilename
import vcd_info
import mplcursors

menuList = ["cut", "copy", "paste", "zoom fit", "zoom in", "zoom out", "undo", "previous", "next"]

mplcursors.cursor(hover=True)

class waveformViewer():
    def __init__(self):
        self.root = Tk()
        self.root.title('Waveform Viewer')

        # fields
        self.scope = ''
        self.scopes = []
        self.selected = []
        self.emptyGraph=True

        # menu
        self.menu()

        # top row
        self.topframe = Frame(self.root)
        self.topframe.pack(pady=10, anchor='w', padx=10)
        self.top()

        # Bottom Row
        self.botframe = Frame(self.root)
        self.botframe.pack(side=BOTTOM)

        # left
        self.leftframe = Frame(self.botframe, padx=10, pady=20)
        self.leftframe.pack(side=LEFT)
        self.left1 = Frame(self.leftframe)
        self.left1.pack()
        self.space(self.leftframe)
        self.left2 = Frame(self.leftframe)
        self.left2.pack()
        self.space(self.leftframe)
        self.left3 = Frame(self.leftframe, highlightbackground="Grey", highlightthickness=1)
        self.left3.pack()
        self.space(self.leftframe)
        self.left4 = Frame(self.leftframe, highlightbackground="Grey", highlightthickness=1)
        self.left4.pack()
        self.sst()
        self.typeSig('start')
        self.Filter()
        self.botbuttons()

        # mid
        self.midframe = Frame(self.botframe, highlightbackground="Grey", highlightthickness=1)
        self.midframe.pack(side=LEFT, anchor='n')

        # right
        self.rightframe = Frame(self.botframe, padx=10)
        self.rightframe.pack(side=LEFT, anchor='n')
        self.graph()
        self.signals()

        # start
        self.root.mainloop()

    def space(self, frame):
        label = Label(frame, text=' ')
        label.pack()

    def top(self):
        global menuList
        for x in menuList:
            self.button2 = Button(self.topframe, text=x)
            self.button2.pack(side=LEFT)

        self.fromlabel = Label(self.topframe, text='From: ')
        self.fromlabel.pack(side=LEFT)

        self.From = Text(self.topframe, height=1, width=10)
        self.From.pack(side=LEFT)

        self.tolabel = Label(self.topframe, text='To: ')
        self.tolabel.pack(side=LEFT)

        self.To = Text(self.topframe, height=1, width=10)
        self.To.pack(side=LEFT)

    def sst(self):
        def selectItem(a):
            curItem = self.tree.item(self.tree.focus())['text']
            if curItem != self.scope:
                self.scope = curItem
                self.typeSig(self.scope)
                self.signals.delete(0, END)
                if self.emptyGraph==False:
                    self.graph()

        self.tree = ttk.Treeview(self.left1, height=6)
        self.tree.column("#0", width=150, minwidth=150, stretch=NO)
        self.tree.heading("#0", text="SST", anchor=W)
        self.tf = self.tree.insert("", "end", text="map9v3_tb.vcd")  # put file name here
        for x in vcd_info.scopeList:
            self.scopes.append(x.split()[0])
            self.tree.insert(self.tf, "end", text=x.split()[0])
        self.tree.bind('<ButtonRelease-1>', selectItem)
        treeScroll = ttk.Scrollbar(self.left1)
        treeScroll.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=treeScroll.set)
        treeScroll.pack(side=RIGHT, fill=Y)
        self.tree.pack(side=LEFT)

    def typeSig(self, scope):  # you have to cntl click to selected multiple
        def selectItem(a):
            self.selected = [self.tree1.item(i) for i in self.tree1.selection()]
            self.signals.delete(0, END)
            sel=[]
            sel2=[]
            for row in self.selected:
                text = row['text'] + ' ' + ' '.join(row['values'])
                if len(text.split()) == 2:
                    self.signals.insert(END, text)
                elif len(text.split()) == 3:
                    self.signals.insert(END, text.split()[0] + " " + text.split()[1] + str([0]))
                for sc in vcd_info.signal_abbreviation:
                    for signal in sc:
                        if signal ==' '.join(text.split()[1:len(text.split())]):
                            sel+=sc[signal]
                            sel2.append(text)
            self.graph(sel,sel2)

        if scope == 'start':
            self.tree1 = ttk.Treeview(self.left2, selectmode="extended")  # ttkwidgets.Checkbox
            self.tree1["columns"] = (1)
            self.tree1.column("#0", width=50, minwidth=50, stretch=NO)
            self.tree1.heading("#0", text="Type", anchor=W)
            self.tree1.column(1, width=100, minwidth=100, stretch=NO)
            self.tree1.heading(1, text="Signals", anchor=W)
            self.tree1.bind('<ButtonRelease-1>', selectItem)
            treeScroll = ttk.Scrollbar(self.left2)
            treeScroll.configure(command=self.tree1.yview)
            self.tree1.configure(yscrollcommand=treeScroll.set)
            self.tree1.pack(side=LEFT)
            treeScroll.pack(side=RIGHT, fill=Y)
        elif scope == 'map9v3_tb.vcd':
            for row in self.tree1.get_children():
                self.tree1.delete(row)
            for s in vcd_info.type_signal:
                for x in s:
                    self.tree1.insert("", "end", text=x.rstrip()[:-2], values=(s[x].replace(' ', '\ ')))  # .lstrip()))
        elif scope in self.scopes:
            for row in self.tree1.get_children():
                self.tree1.delete(row)
            for scopeName in vcd_info.scopeList:
                if scope == scopeName[:-2]:
                    for x in vcd_info.type_signal[int(scopeName[-1])]:
                        self.tree1.insert("", "end", text=x.rstrip()[:-2],
                                          values=(vcd_info.type_signal[int(scopeName[-1])][x].replace(' ', '\ ')))

    def Filter(self):
        self.flabel = Label(self.left3, text='Filter: ')
        self.flabel.pack(side=LEFT)

        self.filter = Text(self.left3, height=1, width=10)
        self.filter.pack(side=LEFT)

    def botbuttons(self):
        self.abutton = Button(self.left4, text="Append")
        self.abutton.pack(side=LEFT)

        self.ibutton = Button(self.left4, text="Insert")
        self.ibutton.pack(side=LEFT)

        self.rbutton = Button(self.left4, text="Replace")
        self.rbutton.pack(side=LEFT)

    def signals(self):
        self.slabel = Label(self.midframe, text='Signals', width=10, anchor='w')
        self.slabel.pack()

        self.signals = Listbox(self.midframe, width=20, height=30)
        self.signals.pack(fill=BOTH)

    def graph(self,ab='empty',ylabels='empty'):
        if ab=='empty':
            try:
                self.canvas.get_tk_widget().destroy()
            except:
                pass
            self.emptyGraph=True
            figure = plt.Figure(figsize=(5, 4), dpi=120)
            plot = figure.add_subplot(1, 1, 1, yticks=[0, 1], xticks=[0, 1], facecolor='black', title="Waveform", ylabel='Amplitude',xlabel="Time (Seconds)")
            self.canvas = FigureCanvasTkAgg(figure, self.rightframe)
            self.canvas.get_tk_widget().pack(side=RIGHT)
            plot.plot([0,1],[0,1],color="black", linewidth=.5, drawstyle='steps-post')
        elif len(ab)==1:
            self.emptyGraph=False
            self.canvas.get_tk_widget().destroy()
            figure = plt.Figure(figsize=(5, 4), dpi=120)
            plot = figure.add_subplot(1, 1, 1, yticks=[0, 1], facecolor='black', title="Waveform", ylabel=ylabels[0],xlabel="Time (Seconds)")
            self.canvas = FigureCanvasTkAgg(figure, self.rightframe)
            self.canvas.get_tk_widget().pack(side=RIGHT)
            # print(ab[0])
            if ab[0] in vcd_info.signal_change.keys():
                data=vcd_info.signal_change[ab[0]]
            else:
                data=vcd_info.signal_change[ab[0]+str([0])]
            y = data[1]
            x = data[0]
            plot.plot(x,y,color="#39ff14", linewidth=.5, drawstyle='steps-post')
        else:
            self.emptyGraph=False
            self.canvas.get_tk_widget().destroy()

            fig, axs = plt.subplots(len(ab),sharex=True)
            fig.suptitle('Waveform')
            bigx=[]
            for i in range(len(ab)):
                # print(ab[i])
                if ab[i] in vcd_info.signal_change.keys():
                    data=vcd_info.signal_change[ab[i]]
                else:
                    data=vcd_info.signal_change[ab[i]+str([0])]
                y=data[1]
                y = list(map(int, y))
                x = data[0]
                x = list(map(int, x))
                print(x,y)
                bigx+=x
                axs[i].plot(x, y,color="#39ff14", linewidth=.5, drawstyle='steps-post')
                axs[i].set_facecolor('black')
                axs[i].set_yticks([0,1])
                axs[i].set(ylabel=ylabels[i])
                axs[i].set(xlabel='Time (Seconds)')
                axs[i].label_outer()

            bigx.sort()
            for ax in axs.flat:
                
                ax.set_xticks(bigx)
                
                
            self.canvas = FigureCanvasTkAgg(fig, self.rightframe)
            self.canvas.get_tk_widget().pack(side=RIGHT)
            
            

    def openFile(self):
        filename = askopenfilename()
        self.open.configure(text=filename)

    '''
    def read(self):
        try:
            # Tk().withdraw()
            filename = 'map9v3_tb.vcd'  # askopenfilename()
            file = open(filename, 'r')
        except:
            print('file not found')
            return

        wires = {}
        for line in file.readlines():
            if '$var' in line:
                params = line.split()
                print(params)

        print(self.variables)'''

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
        editmenu.add_command(label="Past", command=donothing)
        editmenu.add_command(label="Duplicate Line", command=donothing)
        editmenu.add_command(label="Toggle Case", command=donothing)
        menubar.add_cascade(label="Edit", menu=editmenu)
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=donothing)
        helpmenu.add_command(label="About...", command=donothing)
        menubar.add_cascade(label="Help", menu=helpmenu)
        self.root.config(menu=menubar)


wf = waveformViewer()
