# Ein einfaches Beispielskript zur Spracherkennung 
# mit Eingabe per Mikrofon oder einer Audiodatei.
# Dieses Skript funktioniert mit User Interface und Auswahldialog.
import sys
import speech_recognition as sr
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal

class MicrophoneThread(QThread):
    audio_signal = pyqtSignal(object)

    def run(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
        self.audio_signal.emit(audio)
class SpeechRecognitionDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ausgerechnet Algorithmen: Einfache Spracherkennung")
        self.setFixedSize(400, 200)
        self.layout = QVBoxLayout()

        self.title_label = QLabel("Einfache Spracherkennung")
        self.title_label.setObjectName("titleLabel")
        self.layout.addWidget(self.title_label, alignment=QtCore.Qt.AlignCenter)

        self.file_button = QPushButton("Audio-Datei auswählen")
        self.file_button.setObjectName("fileButton")
        self.file_button.clicked.connect(self.file_input)

        self.mic_button = QPushButton("Mikrofon verwenden")
        self.file_button.setObjectName("micButton")
        self.mic_button.clicked.connect(self.mic_input)

        self.result_label = QLabel()
        self.result_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 20px;")
        self.result_label.setText("Ergebnis wird hier angezeigt.")

        self.layout.addWidget(self.file_button, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.mic_button, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.result_label, alignment=QtCore.Qt.AlignCenter)

        self.setLayout(self.layout)

        # Setzt das Stylesheet für das title_label
        self.setStyleSheet("""
            #titleLabel {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 20px;
            }
            #fileButton, #micButton {   
                color:#000;
            }
        """)


    def file_input(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Audio-Datei auswählen")
        if file_path:
            recognizer = sr.Recognizer()
            self.result_label.setText("Verarbeite Audio...")
            QApplication.processEvents() 
            audio_file = sr.AudioFile(file_path)
            with audio_file as source:
                audio = recognizer.record(source)
                self.process_audio(audio)

    def mic_input(self):
        self.result_label.setText("Verarbeite Spracheingabe...")
        self.thread = MicrophoneThread()
        self.thread.audio_signal.connect(self.process_audio)
        self.thread.start()

    def process_audio(self, audio):
        recognizer = sr.Recognizer()
        try:
            text = recognizer.recognize_google(audio, language="de-DE")
            self.result_label.setText("Erkannter Text: {}".format(text))
        except sr.UnknownValueError:
            self.result_label.setText("Sprache nicht erkannt.")
        except sr.RequestError:
            self.result_label.setText("Fehler bei der Verbindung zur Spracherkennung.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = SpeechRecognitionDialog()
    dialog.show()
    sys.exit(app.exec_())