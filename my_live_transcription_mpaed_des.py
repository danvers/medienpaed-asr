#Ein komplexeres Beispiel zur automatischen Spracherkennung und Textvisualisierung mit der Google Cloud Speech Recognition.
from __future__ import division
from google.cloud import speech
import re
import sys
import pyaudio
import queue

#Aufzeichnungsparameter
RATE = 16000
CHUNK = int(RATE / 10)  #100ms
language_code = "de-DE"

class MicrophoneStream(object):
    # Öffnet einen Aufnahmestream als Generator, der die Audioblöcke erzeugt.
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # Die API unterstützt derzeit nur 1-Kanal-Audio (Mono)
            # https://goo.gl/z757pE
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            # Der audio stream wird asynchron ausgeführt, um den Puffer zu füllen.
            # Das ist notwendig, damit der Puffer des Eingabegeräts nicht
            # überläuft, während der aufrufende Thread bspw. Netzwerkanfragen stellt.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        # Schließt den audio stream 
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        # Sammelt fortlaufend Daten aus dem audio stream im Puffer.
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        # So lange der audio stream offen ist werden gepufferte Daten verarbeitet.
        while not self.closed:
            # Blockierendes get(), um sicherzustellen, dass mindestens einen DatenChunk
            # vorhanden ist, und stoppen der Iteration, wenn der Chunk None ist. 
            # Ist der Chunk None, wird das Ende des audio streams angezeigt.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Jetzt werden alle anderen Daten verarbeitet, die noch gepuffert sind.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)


def listen_print_loop(responses):
    # Iteriert durch die Serverantworten und gibt sie aus.
    # Die übermittelte Serverantwort ist ein Generator, der solange blockiert, 
    # bis eine Antwort vom Server geliefert wird. Jede Antwort kann mehrere Ergebnisse enthalten.
    # Jedes Ergebnis kann mehrere Alternativen enthalten (mehr unter https://goo.gl/tjCPAU).  
    # In diesem Beispiel wird nur die Transkription für die oberste Alternative des 
    # obersten Ergebnisses zurückgegeben. Es werden auch Antworten für Zwischenergebnisse geliefert. 
    # Wenn die Antwort eine Zwischenantwort ist, wird am Ende ein Zeilenvorschub gedruckt, 
    # damit damit das nächste Ergebnis es überschreiben kann, bis die Antwort eine finale ist. 
    # Für die finale Antwort wird ein Zeilenumbruch gedruckt, 
    # damit die endgültige Transkription erhalten bleibt.
    
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # Die result-Liste ist fortlaufend. Für den Stream interessiert uns nur
        # das erste Ergebnis, das berücksichtigt wird, denn sobald es `is_final` ist,
        # wird die nächste Äußerung verarbeitet.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Zeigt die erste Alternative an
        transcript = result.alternatives[0].transcript

        # Zwischenergebnisse anzeigen, aber mit einem Carriage Return ('\r') 
        # am Ende der Zeile, so dass nachfolgende Zeilen diese überschreiben.
        # Wenn das vorherige Ergebnis länger war als dieses, müssen
        # einige zusätzliche Leerzeichen gesetzt werden, 
        # um das vorherige Ergebnis zu überschreiben.
        overwrite_chars = " " * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + "\r")
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            print(transcript + overwrite_chars)
            # Wird das Wort exit oder tschüss erkannt, bricht das Skript ab
            if re.search(r"\b(quit|tschüss)\b", transcript, re.I):
                print("Bis bald!...")
                break

            num_chars_printed = 0


def main():
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )
        responses = client.streaming_recognize(streaming_config, requests)
        
        listen_print_loop(responses)

if __name__ == "__main__":
    main()