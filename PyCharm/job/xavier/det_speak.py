import os

from gtts import gTTS
from playsound import playsound

text = "위험합니다. 되돌아가세요."
file = "hello.mp3"

if not os.path.isfile(file):
    tts = gTTS(text = text, lang = 'ko')
    tts.save(file)
    playsound(file)
else:
    playsound(file)
