## Ausgerechnet Algorithmen

[Dan Verständig](https://www.uni-bielefeld.de/ew/verstaendig), [Janne Stricker](https://www.uni-bielefeld.de/ew/stricker)

Universität Bielefeld

## Allgemeine Informationen

Gesprochene Sprache ist für Menschen ein besonders wichtiges Kommunikationsmittel, und die Mehrheit der Weltbevölkerung verlässt sich auf Sprache, um miteinander zu kommunizieren. [Automatische Systeme der Spracherkennung](https://de.wikipedia.org/wiki/Spracherkennung) (ASR) übersetzen gesprochene Sprachen in Text. Es gibt verschiedene Beispiele für ASR. Zum Beispiel erkennt [Siri](https://de.wikipedia.org/wiki/Siri_(Software)) von Apple die Sprache und wandelt diese in Text um. Auch [Alexa](https://de.wikipedia.org/wiki/Amazon_Alexa) von Amazon erkennt automatisch Sprache und verarbeitet Befehle, die an die Geräte gehen. Die automatische Erkennung von Sprache ist ein komplexer Prozess. Ganz einfach erklärt kann er wie folgt dargestellt werden.

![image](img/asr-prozess.png)

Zunächst wird die Spracheingabe in elektronische bzw. digitale Daten umgewandelt. Mit einem stochastischen Modell werden die strukturierten Spracheingabedaten in Text umgewandelt. Hier könnte ein [Hidden Markov Model (HMM)](https://de.wikipedia.org/wiki/Hidden_Markov_Model) die Grundlage bilden.

Auch Soziale Medien bieten inzwischen auch verschiedene Möglichkeiten der Verarbeitung von Spracheingabe an. Gerade für Menschen mit Behinderungen könnten Anwendungen zur Spracherkennung hilfreich bei der Artikulation oder Teilhabe sein. Dennoch gibt es sowohl technische als auch menschliche Faktoren, die Entwicklungen in diesem Bereich ausbremst.

Der hier abgelegte Code dient zur Exploration von Spracherkennung und steht im Zusammenhang zur Publikation Ausgerechnet Algorithmen (2023). Die Publikation geht auf die Präsentation der Forschung zu Teilhabefragen und ASR am Beispiel von TikTok  auf der Herbsttagung der Sektion Medienpädagogik an der Universität Bielefeld im Jahr 2022 zurück. Der Code setzt sich aus einem einfachen Skript zur Spracherkennung allgemein und einem Live System, welches mit [Google Speech Recognition](https://cloud.google.com/speech-to-texthttps:/) arbeitet.

## Wie man den Code benutzen kann

Die Skripte sind kommentiert. Anhand der Kommentierungen sollte man grundlegend die funktionsweise der Skripte nachvollziehen und unterschiedlichen Zielgruppen erklären können. Der Code kann ausgeführt und erprobt werden. Es sind sehr einfache und grundlegende Beispiele, die erweitert werden können.

Der Code dient zur Grundlage, um über die Systeme und Wirkweisen in medienpädagogischen Settings ins Gespräch zu kommen.

Die Skripte erfordern [Python 3](https://www.python.org/downloads/) und eine Entwicklungsumgebung. Wir empfehlen [Microsoft Visual Code](https://code.visualstudio.comhttps:/). Python kann mit [diesem Codeschnipsel von Michael Currin](https://gist.github.com/MichaelCurrin/57caae30bd7b0991098e9804a9494c23) installiert werden.

### Einfache Spracherkennung: simple_sr.py

Das Skript nutzt die Bibliothek [SpeechRecognition](https://pypi.org/project/SpeechRecognition/). Es handelt sich um eine Umgebung mit Unterstützung für verschiedene Engines und Schnittstellen, die Spracherkennung sowohl online als auch offline ermöglichen.

### ASR mit Google Cloud

Die Nutzung des Skripts erfordert eine Internetverbindung sowie einen Google Account. Die Authentifizierung erfolgt über [`gcloud auth`](https://cloud.google.com/sdk/gcloud/reference/auth).

Die Google-Spracherkennungs-API ist eine einfache Methode, um Sprache in Text umzuwandeln, aber sie erfordert eine Internetverbindung. Zudem werden die Daten mit Google verarbeitet. Da Google als Dienstanbieter agiert, können auch Kosten bei der Nutzung von Cloud-Diensten entstehen.
