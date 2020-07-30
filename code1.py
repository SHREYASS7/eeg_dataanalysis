import tkinter as tk
from tkinter import font  as tkfont
from PIL import Image, ImageTk
import os
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
import numpy as np
import cv2


file_path1 = ''
path_img = ''

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller, master = None, *pargs):
        tk.Frame.__init__(self, parent, master, *pargs)
        self.controller = controller
        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        self.image = Image.open('E:/eeg_analysis/bg1.PNG')
        self.img_copy= self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = tk.Label(self, image=self.background_image)
        self.background.pack(fill="both", expand= True)
        self.background.bind('<Configure>', self._resize_image)

        def themlmodel():
            global file_path1
            file_path = 'E:/eeg_analysis/log_1.csv'
            data = pd.read_csv(file_path)

            y = data.O

            features = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N']

            X = data[features]

            data1 = pd.read_csv(file_path1)
            features1 = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N']
            lm = data1[features1]


            model = DecisionTreeRegressor(random_state=0)
            model.fit(X, y)

            val = (model.predict(lm))
            if val == [1]:
                path_img = 'E:/eeg_analysis/stress.PNG'
            else:
                path_img = 'E:/eeg_analysis/relaxed.PNG'

            label6 = tk.Label(self, text='Not uploaded',fg='white',bg='red',relief='raised',font=('Times New Roman',20,'bold'))
            label6.place(x=850,y=360)
            img = cv2.imread(path_img)
            cv2.imshow('OUTPUT',img)


        def fileDialog():
            global file_path1
            filename = filedialog.askopenfilename(initialdir =  "/", title = "Select A File" )
            label6.destroy()
            label7 = tk.Label(self, text='   Uploaded   ',fg='white',bg='green',relief='raised',font=('Times New Roman',20,'bold'))
            label7.place(x=850,y=360)
            file_path1 =  filename

        global file_path1

        label5 = tk.Label(self, text=" UPLOAD: ",fg='white',bg='BLUE',relief='raised',font=('Times New Roman',20,'bold'))
        label5.place(x=550,y=360)

        button1 = tk.Button(self,text="Browse",relief='raised',font=('Times New Roman',16,'bold'), command=fileDialog)
        button1.place(x=730,y=360)

        button2 = tk.Button(self,text="     TEST     ",relief='raised',font=('Times New Roman',16,'bold'), command=themlmodel)
        button2.place(x=713,y=410)

        label6 = tk.Label(self, text='Not uploaded',fg='white',bg='red',relief='raised',font=('Times New Roman',20,'bold'))
        label6.place(x=850,y=360)
        label1 = tk.Label(self,text='                    Stress Detection using EEG Signals                   ',fg='white',bg='red',relief='raised',font=('Times New Roman',45,'bold'))
        label1.place(x=17,y=8)

    def _resize_image(self,event):
        new_width = event.width
        new_height = event.height
        self.image = self.img_copy.resize((new_width, new_height))
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image =  self.background_image)

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
