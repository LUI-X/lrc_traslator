from pydub import AudioSegment
import speech_recognition as sr
"""
# files
src = "files/mp3/one.mp3"
dst = "files/mp3/prueba.wav"

# convert wav to mp3
sound = AudioSegment.from_mp3(src)
sound.export(dst, format="wav")
"""

audio_file = 'files/mp3/prueba.wav'

r = sr.Recognizer()

with sr.AudioFile(audio_file) as source:
    audio = r.record(source)  # read the entire audio file

    print("Transcription: " + r.recognize_google(audio))