#malpractice
#last cleaned up: may 10, 13:36. Took one hour.
#classes are capitalized, everything else is camelCase
#underscores are chatgpt's fault.

from tkinter import *
from tkinter import filedialog
import os # just to stop it from erroring on windows
osname = os.name
#import subprocess
#from scrollable import ScrollFrame # when packing the scrollframe, we pack scrollFrame itself (NOT the viewPort)
#import re #apparently needed for splitting by spaces and not tabs
from tkextrafont import Font


def drop(event):
    entry_sv.set(event.data)


if  os.name == "posix":
    assetsDir = "assets/"
else:
    assetsDir = "assets\\"


class Window(Tk):
    
    def __init__(self,title,geometry):
        super().__init__() # Initialize the Tk class, apparently...??
        self.geometry(geometry)
        self.title(title)
        self.resizable(False, False)
        try: #image loading
            icon = PhotoImage(file=f"{assetsDir}icon.png")
            self.iconphoto(True,icon)
            
            self.bgImage = PhotoImage(file=f"{assetsDir}background.png")
            Label(self, image=self.bgImage).place(x=0,y=0)
        except Exception as e:
            print(f"Error loading images in Window.__init__: {e}")
            print("likely not exectuting from the correct directory.")
        
        Button(self,bg="#4AFF00",activebackground="red",font=("Mojangles",12),text="openfile",command=self.openFile).place(x=100,y=0)
        
        Button(self,bg="#4AFF00",activebackground="red",font=("Mojangles",12),text="DND",command=self.dnd).place(x=100,y=40)
     

    def dnd(self):
        from tkinterdnd2 import DND_FILES, TkinterDnD

        dndRoot = TkinterDnD.Tk()  # notice - use this instead of Tk()

        lb = Listbox(dndRoot)
        lb.insert(1, "drag files to here")

        # register the listbox as a drop target
        lb.drop_target_register(DND_FILES)
        lb.dnd_bind('<<Drop>>', lambda e: lb.insert(END, e.data))

        lb.pack()
        Button(dndRoot,bg="#4AFF00",activebackground="red",font=("Mojangles",12),text="Launch",command=(lambda: dndRoot.destroy())).place(x=0,y=50)
        dndRoot.mainloop()


    def openFile(self):
        #global filepath -- still learning how global variables work
        global pathEntry
        filepath = filedialog.askopenfilenames(
            initialdir="/home",
            title="Select a Reborn Appimage",
            filetypes=(("Appimages","*.AppImage"),("something else?","*"))
            )
        print(filepath)

        pathEntry.delete(0,END)
        
        if len(filepath) > 40:
            for i in range(40):
                pathEntry.insert(0,filepath[-(i+1)])
        else:
            pathEntry.insert(0,filepath)
        pathEntry.insert(0,"...")
        pathEntry.config(state="disabled")
    def launch(self):
        pass
root = Window("GUI","400x480")
font = Font(file="assets/mojangles.ttf", family="Mojangles")
root.mainloop()
