from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QAbstractSlider, QSlider, QApplication, QMainWindow
from pydub import AudioSegment
from PySide6.QtCore import Qt, Slot, QTimer
import pyaudio
import wave
import sys
import os


class SeekSlider(QSlider):

    def __init__(self):
        super().__init__()

        self._current_time = 0
        self._current_position = 0

        self.audio : AudioSegment = AudioSegment.from_file("/home/xelame/Music/Fuji Kaze/Fujii Kaze - Michi Teyu Ku (Overflowing).mp4")

        # Exporter le fichier MP3 en WAV
        self.audio.export('output.wav', format='wav')

        self.wf = wave.open('output.wav', 'rb')

        # Instantiate PyAudio and initialize PortAudio system resources (2)
        p = pyaudio.PyAudio()

        # Open stream using callback (3)
        self._stream : pyaudio._Stream = p.open(format=p.get_format_from_width(self.wf.getsampwidth()),
                        channels=self.wf.getnchannels(),
                        rate=self.wf.getframerate(),
                        output=True,
                        stream_callback=self._callback)

        self.setRange(0, 100)
        self.setValue(0)
        self.setTickInterval(100)

        self.setOrientation(Qt.Orientation.Horizontal)

        # Créer un temporisateur pour mettre à jour la position de lecture régulièrement
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_slider_position())
        self.timer.start(100)  # Mettre à jour toutes les 100 millisecondes

    def _callback(self, in_data, frame_count, time_info, status):
        data = self.wf.readframes(frame_count)
        self.update_slider_position()
        """
        print("\033[H\033[J", end="")
        print(self.getPosition(), " %")
        """
        return (data, pyaudio.paContinue)
    
    def pause(self):
        if not self._stream.is_stopped():
            self._stream.stop_stream()

    def start(self):
        if self._stream.is_stopped():
            self._stream.start_stream()
    
    # Mettre à jour la position du curseur en fonction de la position de lecture
    def update_slider_position(self) -> None:
        self.updatePosition()

        # self.setSliderPosition(position) -> même chose que setValue mais avec un signal
        self.setValue(self._current_position)

    def updatePosition(self):
        self._current_time = int(self.wf.tell() / (self.wf.getframerate() * self.wf.getsampwidth()) * self.wf.getnchannels())
        self._current_position = int(self._current_time / self.audio.duration_seconds * 100) 
        
    
    def closeEvent(self, event: QCloseEvent) -> None:
        print("Fermeture de l'application")
        self._stream.stop_stream()
        self._stream.close()
        # os.remove('output.wav')
        return super().closeEvent(event)
    
    def positionToTime(self, position : float) -> float:
        return position / self.maximum() * self.audio.duration_seconds
    
    def timeToPosition(self, time : float) -> float:
        return time / self.audio.duration_seconds * self.maximum()
    
    def sliderChange(self, change: QAbstractSlider.SliderChange) -> None:
        print("\033[H\033[J", end="")
        print(self._current_position, "%")
        print(self._current_time, "s")
        return super().sliderChange(change)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    seekSlider = SeekSlider()
    window.setCentralWidget(seekSlider)
    window.show()
    sys.exit(app.exec())
