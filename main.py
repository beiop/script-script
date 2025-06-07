import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os

THUMBNAIL_SIZE = (100, 100)
SUPPORTED_FORMATS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.cr2', '.cr3', '.crw', '.arw')

root = tk.Tk()
root.title("Image Tool")
root.geometry("800x600")


def center_window(win, width=None, height=None):
    win.update_idletasks()
    if width is None or height is None:
        width = win.winfo_width()
        height = win.winfo_height()
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    win.geometry(f'{width}x{height}+{x}+{y}')


# ---------- Preview Area ----------
preview_container = tk.Frame(root, height=250)
preview_container.pack(fill="x")

canvas = tk.Canvas(preview_container, height=250)
scroll_x = tk.Scrollbar(preview_container, orient="horizontal", command=canvas.xview)
scroll_y = tk.Scrollbar(preview_container, orient="vertical", command=canvas.yview)
canvas.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

thumb_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=thumb_frame, anchor="nw")

canvas.pack(side="left", fill="both", expand=True)
scroll_x.pack(side="bottom", fill="x")
scroll_y.pack(side="right", fill="y")


def update_scrollregion(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))


thumb_frame.bind("<Configure>", update_scrollregion)

# ---------- Main Area ----------
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

button_frame = tk.Frame(main_frame)
button_frame.pack(side="bottom", fill="x", pady=10)

image_labels = []


def clear_preview():
    for label in image_labels:
        label.destroy()
    image_labels.clear()


def open_folder_or_image():
    clear_preview()

    # Allow selecting multiple image files
    file_paths = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[("Images", "*.png *.jpg *.jpeg *.gif *.bmp *.cr2 *.cr3 *.crw *.arw")]
    )

    if file_paths:
        if len(file_paths) == 1:
            show_single_image(file_paths[0])
        else:
            show_multiple_images(file_paths)
        return

    # If no file selected, try selecting a folder
    folder_path = filedialog.askdirectory(title="Select a Folder")
    if folder_path and os.path.isdir(folder_path):
        show_folder_thumbnails(folder_path)


def show_single_image(path):
    clear_preview()
    for widget in thumb_frame.winfo_children():
        widget.destroy()

    try:
        img = Image.open(path)
        width, height = canvas.winfo_width(), canvas.winfo_height()
        if width == 1 or height == 1:
            width, height = 800, 250
        img.thumbnail((width, height), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        label = tk.Label(thumb_frame, image=img_tk)
        label.image = img_tk
        label.pack(expand=True)
        image_labels.append(label)
    except Exception as e:
        print(f"Error loading image {path}:", e)


def show_multiple_images(paths):
    clear_preview()
    for widget in thumb_frame.winfo_children():
        widget.destroy()

    for path in paths:
        try:
            img = Image.open(path)
            img.thumbnail(THUMBNAIL_SIZE)
            img_tk = ImageTk.PhotoImage(img)
            label = tk.Label(thumb_frame, image=img_tk)
            label.image = img_tk
            label.pack(side="left", padx=5, pady=5)
            image_labels.append(label)
        except Exception as e:
            print(f"Failed to load {path}: {e}")


def show_folder_thumbnails(folder_path):
    clear_preview()
    for widget in thumb_frame.winfo_children():
        widget.destroy()

    images = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
              if f.lower().endswith(SUPPORTED_FORMATS)]
    show_multiple_images(images)


# ---------- Operation Popup ----------
def operation_func_1():
    print("Running operation 1")


def operation_func_2():
    print("Running operation 2")


def operation_func_3():
    print("Running operation 3")


def show_operation_popup():
    popup = tk.Toplevel(root)
    popup.title("Operation")
    popup.geometry("300x250")
    center_window(popup, 300, 250)

    tk.Label(popup, text="Select Operation:").pack(pady=(10, 0))
    selected_option = tk.StringVar()
    dropdown = ttk.Combobox(popup, textvariable=selected_option, state="readonly")
    dropdown['values'] = ['Operation 1', 'Operation 2', 'Operation 3']
    dropdown.pack(pady=5)

    dynamic_frame = tk.Frame(popup)
    dynamic_frame.pack(pady=10, fill="x")

    def update_dynamic_content(event=None):
        for widget in dynamic_frame.winfo_children():
            widget.destroy()

        option = selected_option.get()
        if option == "Operation 1":
            tk.Label(dynamic_frame, text="Options for Operation 1").pack()
            tk.Button(dynamic_frame, text="Run", command=operation_func_1).pack()
        elif option == "Operation 2":
            tk.Label(dynamic_frame, text="Settings for Operation 2").pack()
            tk.Button(dynamic_frame, text="Run", command=operation_func_2).pack()
        elif option == "Operation 3":
            tk.Label(dynamic_frame, text="Tools for Operation 3").pack()
            tk.Button(dynamic_frame, text="Run", command=operation_func_3).pack()

    dropdown.bind("<<ComboboxSelected>>", update_dynamic_content)


def convert():
    messagebox.showinfo("Convert", "Conversion started!")


# ---------- Buttons ----------
btn_open = tk.Button(button_frame, text="Open Folder or Image", command=open_folder_or_image)
btn_operation = tk.Button(button_frame, text="Operation", command=show_operation_popup)
btn_convert = tk.Button(button_frame, text="Convert", command=convert)

btn_open.pack(side="left", expand=True, padx=10)
btn_operation.pack(side="left", expand=True, padx=10)
btn_convert.pack(side="left", expand=True, padx=10)

# ---------- Start ----------
center_window(root, 800, 600)
root.mainloop()