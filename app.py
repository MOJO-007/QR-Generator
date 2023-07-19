import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pyqrcode
import pandas as pd
import os
import zipfile
import ctypes
from PIL import Image, ImageDraw, ImageFont
import time
from tqdm import tqdm

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
        
def shortenName(Full_name):
    name_parts=Full_name.split()
    if len(name_parts) >= 3:
        if len(name_parts[0]) == 1:
            if len(name_parts[1])== 1:
                full_first_name= name_parts[-1] if len(name_parts[-1]) > 0 else ""
                second_initial = name_parts[0][0]
                third_initial = name_parts [1][0]
            else:
                second_initial = name_parts[0][0]
                full_first_name = name_parts[1]
                third_initial = name_parts[-1][0] if len(name_parts[-1]) > 0 else ""
        
        elif len(name_parts[1])== 1:
            full_first_name = name_parts[0]
            second_initial= name_parts[1][0]
            third_initial= name_parts [-1][0]

        else:
            full_first_name = name_parts[0]
            second_initial = name_parts[1][0] if len(name_parts[1]) > 0 else ""
            third_initial = name_parts[-1][0] if len(name_parts[-1]) > 0 else ""

    elif len(name_parts) == 2:
        if len(name_parts[0]) == 1:
            full_first_name=name_parts[1]
            second_initial=name_parts[0][0]
            third_initial=""

        else:
            full_first_name = name_parts[0]
            second_initial = name_parts[-1][0] if len(name_parts[-1]) > 0 else ""
            third_initial=""

    elif len(name_parts) == 1:
        full_first_name = name_parts[0]
        second_initial=""
        third_initial=""

    shortName=full_first_name+" "+second_initial+" "+third_initial
    return shortName


def createQRCode(file_path):
    df=pd.read_csv(file_path)
    maxrows=len(df)
    
    for index, values in tqdm(df.iterrows(), total=maxrows, desc="Creating QR Codes", unit="code"):

        number=values["Number"]
        name = values["Name"]
        name=shortenName(name)  
        print(name)
        data=f'''{number}'''
        image=pyqrcode.create(data)
        image.png(f"qrcodes/{number}.png",scale="17")


        template_image=Image.open("Template.png")
        qr_image=Image.open(f"qrcodes/{number}.png")
        Image.Image.paste(template_image,qr_image,(285,600))
        template_image.save(f"qrcodes/{number}.png")


        img= Image.open(f"qrcodes/{number}.png")
        d=ImageDraw.Draw(img)
        fnt= ImageFont.truetype("Montserrat/Montserrat-VariableFont_wght.ttf",70)
        fnt2=ImageFont.truetype("Montserrat/Montserrat-VariableFont_wght.ttf",90)
        text_color = 'black'
        d.text((325,1335),name,font=fnt,fill=text_color, stroke_width=3, align='left')
        d.text((375,1450),number,font=fnt,stroke_width=4,align='center',fill='#BDA8E9')
        img.save(f"qrcodes/{number}.png")
        


def zip_directory(directory, zip_file_name):
    with zipfile.ZipFile(zip_file_name, "w") as zip_file:
        for root, directories, files in os.walk(directory):
            for file in files:
                zip_file.write(os.path.join(root, file))

def callProcess():
    start_time=time.time()
    filename=process_csv()
    createQRCode(filename)
    directory = "./qrcodes"
    zip_file_name = "qrcodes.zip"
    zip_directory(directory, zip_file_name)

    end_time=time.time()
    time_taken=end_time-start_time
    messagebox.showinfo("Message", "The QR codes are generated in : {:.1f} seconds".format(time_taken))
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
