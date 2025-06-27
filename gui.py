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
import messagebox
import tkinter as tk
from datetime import datetime, timedelta




#def drop(event):
#    entry_sv.set(event.data)


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
        self.center_window(self,400,480)
        try: #image loading
            icon = PhotoImage(file=f"{assetsDir}icon.png")
            self.iconphoto(True,icon)
            
            self.bgImage = PhotoImage(file=f"{assetsDir}background.png")
            Label(self, image=self.bgImage).place(x=0,y=0)
        except Exception as e:
            print(f"Error loading images in Window.__init__: {e}")
            print("likely not exectuting from the correct directory.")
        
        Button(self,bg="#4AFF00",activebackground="red",font=("Mojangles",12),text="openfile",command=self.openFile).place(x=0,y=0)
        Button(self,bg="#4AFF00",activebackground="red",font=("Mojangles",12),text="launch",command=self.launch).place(x=0,y=80)
        Button(self,bg="#4AFF00",activebackground="red",font=("Mojangles",12),text="DND",command=self.dnd).place(x=0,y=40)
        
        
        #that thing
        def calculate_offset_seconds():
            try:
                # Get values from offset fields, default to 0 if empty
                years = int(entry_years.get() or 0)
                months = int(entry_months.get() or 0)
                days = int(entry_days.get() or 0)
                hours = int(entry_hours.get() or 0)
                minutes = int(entry_minutes.get() or 0)
                seconds = int(entry_seconds.get() or 0)

                # Use a base datetime
                base = datetime(1970, 1, 1)

                # Approximate months as 30 days and years as 365 days
                total_offset = timedelta(
                    days=(years * 365 + months * 30 + days),
                    hours=hours,
                    minutes=minutes,
                    seconds=seconds
                )

                # Get total seconds of offset
                offset_seconds = int(total_offset.total_seconds())

                label_offset_result.config(text=f"Offset in Seconds: {offset_seconds}")
            except ValueError:
                label_offset_result.config(text="Error: Enter valid integers.")

        # Offset input labels and entries
        Label(self, text="Years:").pack()
        entry_years = Entry(self, width=5)
        entry_years.pack()

        Label(self, text="Months:").pack()
        entry_months = Entry(self, width=5)
        entry_months.pack()

        Label(self, text="Days:").pack()
        entry_days = Entry(self, width=5)
        entry_days.pack()

        Label(self, text="Hours:").pack()
        entry_hours = Entry(self, width=5)
        entry_hours.pack()

        Label(self, text="Minutes:").pack()
        entry_minutes = Entry(self, width=5)
        entry_minutes.pack()

        Label(self, text="Seconds:").pack()
        entry_seconds = Entry(self, width=5)
        entry_seconds.pack()

        Button(self, text="Calculate Offset (in seconds)", command=calculate_offset_seconds).pack()
        self.label_input_timestamp = Label(self, text="")
        self.label_input_timestamp.pack()
        label_offset_result = Label(self, text="")
        label_offset_result.pack()
        


    #that thing in reverse
    def from_epoch(self,epoch):
        try:
            
            # Convert to datetime
            return datetime.fromtimestamp(epoch)

            
        except ValueError:
            messagebox.showerror("Error", "Invalid epoch time (must be an integer).")

    def center_window(self,win, width=None, height=None):
        win.update_idletasks()
        if width is None or height is None:
            width = win.winfo_width()
            height = win.winfo_height()
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        win.geometry(f'{width}x{height}+{x}+{y}')


    def dnd(self):
        from tkinterdnd2 import DND_FILES, TkinterDnD

        dndself = TkinterDnD.Tk()  # notice - use this instead of Tk()

        lb = Listbox(dndself)
        lb.insert(1, "drag files to here")

        # register the listbox as a drop target
        lb.drop_target_register(DND_FILES)
        lb.dnd_bind('<<Drop>>', lambda e: lb.insert(END, e.data))

        lb.pack()
        Button(dndself,bg="#4AFF00",activebackground="red",font=("Mojangles",12),text="Launch",command=(lambda: dndself.destroy())).place(x=0,y=50)
        dndself.mainloop()


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
        timestamp = self.from_epoch(1561675987.509)
        
        self.label_input_timestamp.config(text=f"File original {timestamp}")
self = Window("GUI","400x480")
font = Font(file="assets/mojangles.ttf", family="Mojangles")
self.mainloop()
