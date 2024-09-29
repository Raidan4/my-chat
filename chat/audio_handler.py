import os
import speech_recognition as sr
from gtts import gTTS

# Speech to Text Function
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("تحدث الآن...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language='ar')
            return text
        except sr.UnknownValueError:
            return "لم يتم التعرف على الصوت"
        except sr.RequestError:
            return "فشل الاتصال بخدمة التعرف على الصوت"

# Text to Speech Function
def text_to_speech(text):
    tts = gTTS(text=text, lang='ar')
    tts.save("response.mp3")
    os.system("start response.mp3")