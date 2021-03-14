from configparser import ConfigParser
from main import startAlgorithm

import importlib as imp

import tkinter as tk
from tkinter import ttk 

config = ConfigParser()
config.read('config.ini')

algoritmos = config.sections()

algs_modules = ConfigParser()
algs_modules.read('algs_modules.ini')

class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.geometry('500x500')
        master.title('Algoritmos Bioinspirados')
        self.pack()
        self.create_combobox()

    def create_combobox(self):
        algoritmos_label = ttk.Label(self, text="Algoritmo: ")
        algoritmos_label.grid(column = 0, row=1, pady=(10,30))

        self.algoritmos_combobox = ttk.Combobox(self, values = algoritmos)
        self.algoritmos_combobox.bind('<<ComboboxSelected>>', self.mod_algorithm)
        self.algoritmos_combobox.grid(column = 1, row = 1, pady=(10,30))

    def mod_algorithm(self, event):
        self.textboxes = []

        if hasattr(self, 'bottomframe'):
            self.bottomframe.grid_remove()

        self.selectedAlgorithm = self.algoritmos_combobox.get()

        self.bottomframe = tk.Frame(self, width='350')
        self.bottomframe.grid()

        i = 3        
        for key in [option for option in config[self.selectedAlgorithm]]:
            self.create_textboxes(key, i)
            i+=1

        self.create_button(self.selectedAlgorithm)
    
    def create_textboxes(self, key, row):
        algoritmos_label = ttk.Label(self.bottomframe, text=key + ':', justify=tk.RIGHT)
        algoritmos_label.grid(column = 0, row=row, pady=5)

        textbox = tk.Entry(self.bottomframe)
        textbox.grid(column = 1, row=row, pady=5)

        self.textboxes.append(textbox)


    def create_button(self, algorithm):
        botao_confirma = tk.Button(self.bottomframe, text="OK", command=self.buttonCallback)
        botao_confirma.grid(sticky=tk.W+tk.E, column=1, columnspan=2, pady=10)

    def buttonCallback(self):
        params = []
        for entries in self.textboxes:
            params.append(entries.get())

        startAlgorithm(self.selectedAlgorithm, params)

root = tk.Tk()
app = Application(master=root)
app.mainloop()
