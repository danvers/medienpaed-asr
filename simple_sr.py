# Ein einfaches Beispielskript zur Spracherkennung 
# mit Eingabe per Mikrofon ohne User Interface.
# Das Skript wird im Terminal ausgeführt.
import speech_recognition as sr
sr = sr.Recognizer()
with sr.Microphone() as source:
    print("Ins Mikrofon sprechen...")
    audio = sr.listen(source)
try:
    print("Das kam an: " + sr.recognize_google(audio))
except sr.UnknownValueError:
    print("Audio konnte nicht erfasst werden.")
except sr.RequestError as e:
    print("Ergebnisse konnten nicht erfasst werden; {0}".format(e))