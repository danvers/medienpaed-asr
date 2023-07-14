# Ein einfaches Beispielskript zur Spracherkennung mit Eingabe per Mikrofon.
import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Ins Mikrofon sprechen...")
    audio = r.listen(source)
try:
    print("Das kam an: " + r.recognize_google(audio))
except sr.UnknownValueError:
    print("Audio konnte nicht erfasst werden.")
except sr.RequestError as e:
    print("Ergebnisse konnten nicht erfasst werden; {0}".format(e))