from PySide6.QtWidgets import QMenuBar
from PySide6.QtCore import Qt
from fileSelector import FileSelector

class MyMenuBar(QMenuBar):
    def __init__(self):
        super().__init__()

        self.fileSelector = FileSelector()

        self.addAction("Ouvrir un fichier", self.fileSelector.open_file)
        self.addAction("Ajouter un dossier", self.fileSelector.open_folder)