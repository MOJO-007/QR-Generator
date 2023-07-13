import pyqrcode
import pandas as pd
import os
import zipfile

 
def createQRCode():
    df=pd.read_csv("data.csv")
    for index, values in df.iterrows():

        number=values["Number"]
        
        data=f'''

        Roll:{number}\n
        '''
        image=pyqrcode.create(data)

        image.png(f"qrcodes/{number}.png",scale="5")


        # image.svg(f"{number}.svg",scale="5")
createQRCode()


def zip_directory(directory, zip_file_name):
    with zipfile.ZipFile(zip_file_name, "w") as zip_file:
        for root, directories, files in os.walk(directory):
            for file in files:
                zip_file.write(os.path.join(root, file))

directory = "./qrcodes"
zip_file_name = "QRCODES.zip"
zip_directory(directory, zip_file_name)