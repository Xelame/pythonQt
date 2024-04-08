from PySide6.QtWidgets import QFileDialog
import os

class FileSelector(QFileDialog):
    def __init__(self):
        super().__init__()

    def open_file(self):
        self.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.setNameFilter("Fichiers audio (*.mp3 *.wav)")
        self.setWindowTitle("Ouvrir un fichier audio")

        if self.exec() == QFileDialog.DialogCode.Accepted:
            selected_file = self.selectedFiles()[0]
            print("Fichier sélectionné:", selected_file)
        else:
            selected_file = []
            print("Aucun fichier sélectionné")

        return selected_file
    
    def open_folder(self):
        self.setFileMode(QFileDialog.FileMode.Directory)
        self.setWindowTitle("Ajouter un dossier")

        if self.exec() == QFileDialog.DialogCode.Accepted:
            selected_folder = self.selectedFiles()[0]
            selected_files = self.list_audio_files(selected_folder)
            for file in selected_files:
                print("Fichiers sélectionnés:", file)
        else:
            print("Aucun fichier sélectionné")

    def list_audio_files(self, directory):
        audio_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(('.mp3', '.wav', '.ogg', '.flac')):  # Ajoutez d'autres extensions si nécessaire
                    audio_files.append(os.path.join(root, file))
        return audio_files