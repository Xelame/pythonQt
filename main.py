from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget
from PySide6.QtCore import SIGNAL
from toolbar import ToolBar
import sys
from seekSlider import SeekSlider

class AudioPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lecteur audio")

        toolbar = ToolBar()
        self.addToolBar(toolbar)

        # Créer les boutons de contrôle
        self.playButton = QPushButton("Play")
        self.pauseButton = QPushButton("Pause")
        self.stopButton = QPushButton("Stop")
        self.slider = SeekSlider()


        # Créer la mise en page
        layout_horizontal = QHBoxLayout()
        layout_horizontal.addWidget(self.playButton)
        layout_horizontal.addWidget(self.pauseButton)
        layout_horizontal.addWidget(self.stopButton)

        self.playButton.clicked.connect(self.slider.start)
        self.pauseButton.clicked.connect(self.slider.pause)

        layout_vertical = QVBoxLayout()
        layout_vertical.addWidget(self.slider)
        layout_vertical.addLayout(layout_horizontal)

        central_widget = QWidget()
        central_widget.setLayout(layout_vertical)
        self.setCentralWidget(central_widget)

        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AudioPlayer()
    window.show()
    sys.exit(app.exec())
