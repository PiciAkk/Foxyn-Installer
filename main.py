import tkinter as tk
from tkinter import ttk
from tkinter.constants import HORIZONTAL
from tkinter.messagebox import showinfo
import os
import requests
from mega import Mega
import json
from zipfile import ZipFile
import threading
import time

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('FoxynPack telepítő')
        self.configure(background="#C10950")
        self.geometry('600x400')

        self.titleLabel = ttk.Label(self, text='FoxynPack telepítő', font=("Ubuntu", 20), background="black", foreground="white")
        self.titleLabel.pack(pady=20)   

        self.locationEntry = ttk.Entry(self, justify='center')
        self.locationEntry.insert(0, self.getDefaultMCPath())
        self.locationEntry.pack(pady=20)

        self.installThread = threading.Thread(target=self.install)
        self.installBTN = ttk.Button(self, text="Kattints ide a FoxynPack telepítéséhez!", command=lambda: self.installThread.start())
        self.installBTN.pack()
    def installForge(self):
        open("forge.jar", "wb+").write(
            requests.get("https://maven.minecraftforge.net/net/minecraftforge/forge/1.7.10-10.13.4.1614-1.7.10/forge-1.7.10-10.13.4.1614-1.7.10-installer.jar").content
        )
        showinfo(title="Forge", message="Forge telepítő sikeresen letöltve! Nyomj az OK gombra a telepítéséhez!")
        os.system("java -jar forge.jar")
        os.system("clear")
    def getDefaultMCPath(self):
        if os.name == 'nt':
            return os.path.join(os.environ['APPDATA'], 'minecraft/')
        else:
            return os.path.join(os.environ['HOME'], '.minecraft/')
    def setupLauncherProfiles(self):
        self.profiles = json.loads(open(f"{self.installTo}/launcher_profiles.json", "r").read())
        for profileName, profile in self.profiles["profiles"].items():
            if profile["lastVersionId"] == "1.7.10-Forge10.13.4.1614-1.7.10":
                self.profiles["profiles"][profileName]["icon"] = "Red_Sandstone"
                self.profiles["profiles"][profileName]["name"] = "FoxynPack"
        open(f"{self.installTo}/launcher_profiles.json", "w").write(json.dumps(self.profiles))
    def installFoxynPack(self):
        Mega().login().download_url("https://mega.nz/file/8YgWGYgB#037LWLYz8scEEw70MUpyV0vpDSZV4y6JLoMCHsktsbk", f"{self.installTo}/mods/")
        with ZipFile(f"{self.installTo}/mods/foxynpack_client_1.1_generic.zip", 'r') as zipFile:
            zipFile.extractall(f"{self.installTo}")
        showinfo(title="Sikeres telepítés", message=f"FoxynPack sikeresen telepítve ide: {self.installTo}")
    def startProgessBar(self):
        self.progress = ttk.Progressbar(self, orient=HORIZONTAL, length=200, mode='determinate')
        self.progress.pack(pady=50)
        for i in range(100):
            if not self.installThread.is_alive():
                self.progress["value"] = 100
                break
            self.progress["value"] = i
            self.update_idletasks()
            time.sleep(0.5)
    def install(self):
        # start progressbar
        threading.Thread(target=self.startProgessBar).start()
        # get the path to install FoxynPack to
        self.installTo = self.locationEntry.get()
        # install forge
        self.installForge()
        # setup launcher profiles
        if os.path.exists(f"{self.installTo}/launcher_profiles.json"):
            # user is using official minecraft launcher
            self.setupLauncherProfiles()
        # install FoxynPack
        self.installFoxynPack()
def main(): 
    App().mainloop()
if __name__ == "__main__":
    main()