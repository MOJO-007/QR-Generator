import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pyqrcode
import pandas as pd
import os
import zipfile
import subprocess
import ctypes


hwnd = ctypes.windll.kernel32.GetConsoleWindow()
ctypes.windll.user32.ShowWindow(hwnd, 6)

def process_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    # print("Selected file:", file_path)
    if file_path:
        return file_path
    else:
        messagebox.showinfo("Message","The file was not selected!")
        root.destroy()
        return 0
        
        

def createQRCode(file_path):
    df=pd.read_csv(file_path)
    for index, values in df.iterrows():

        number=values["Number"]
        
        data=f'''{number}'''
    
        image=pyqrcode.create(data)

        image.png(f"qrcodes/{number}.png",scale="5")

def zip_directory(directory, zip_file_name):
    with zipfile.ZipFile(zip_file_name, "w") as zip_file:
        for root, directories, files in os.walk(directory):
            for file in files:
                zip_file.write(os.path.join(root, file))

def callProcess():
    filename=process_csv()
    createQRCode(filename)
    directory = "./qrcodes"
    zip_file_name = "QRCODES.zip"
    zip_directory(directory, zip_file_name)

    file_list = os.listdir(directory) 

    messagebox.showinfo("Message", "The QR codes are generated")
    root.destroy()

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

root = tk.Tk()
root.geometry("400x300")
center_window(root)
root.title("QR-CODE GENARATOR")
root.resizable(False, False)






canvas = tk.Canvas(root, width=400, height=300)
canvas.pack()

color1 = "#7AD7F0"  
color2 = "#F5FCFF"
gradient_rect = canvas.create_rectangle(0, 0, 400, 300, fill=color1, width=0)
canvas.itemconfigure(gradient_rect, fill=color1, outline=color1)
canvas.itemconfigure(gradient_rect, fill=color2, outline=color2)

button = tk.Button(root, text="Select CSV File", command=callProcess)
button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

root.mainloop()
