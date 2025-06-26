from tkinter import *

def dnd(self):
    from tkinterdnd2 import DND_FILES, TkinterDnD

    dndRoot = TkinterDnD.Tk()  # notice - use this instead of Tk()

    lb = Listbox(dndRoot)
    lb.insert(1, "drag files to here")

    # register the listbox as a drop target
    lb.drop_target_register(DND_FILES)
    lb.dnd_bind('<<Drop>>', lambda e: lb.insert(END, e.data))

    lb.pack()
    dndRoot.mainloop()