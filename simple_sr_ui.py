# Ein einfaches Beispielskript zur Spracherkennung 
# mit Eingabe per Mikrofon oder einer Audiodate.
# Dieses Skript funktioniert mit User Interface und Auswahldialog.
import sys
import speech_recognition as sr
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QFileDialog, QLabel

class SpeechRecognitionDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ausgerechnet Algorithmen: Einfache Spracherkennung")
        self.layout = QVBoxLayout()
        
        self.file_button = QPushButton("Audio-Datei auswählen")
        self.file_button.clicked.connect(self.file_input)

        self.mic_button = QPushButton("Mikrofon verwenden")
        self.mic_button.clicked.connect(self.mic_input)

        self.result_label = QLabel()
        self.result_label.setText("Ergebnis wird hier angezeigt.")

        self.layout.addWidget(self.file_button)
        self.layout.addWidget(self.mic_button)
        self.layout.addWidget(self.result_label)

        self.setLayout(self.layout)

    def file_input(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Audio-Datei auswählen")
        if file_path:
            self.process_audio(file_path)

    def mic_input(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            audio = recognizer.listen(source)

        self.process_audio(audio)

    def process_audio(self, audio):
        recognizer = sr.Recognizer()
        try:    
            with sr.AudioFile(audio) as source:
                audio_data = recognizer.record(source)                  
        
            text = recognizer.recognize_google(audio_data, language="de-DE")

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