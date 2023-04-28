import speech_recognition as sr
import playsound
from gtts import gTTS
import os
from threading import Thread
def listen():
    input = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = input.listen(source)
        try:
            data = input.recognize_google(audio)
            print("You said: " + data)
        except sr.UnknownValueError:
            print("Sorry, I didn't get that. Please try again!")
            data = listen()
    return data

def speak(text):
    response = gTTS(text=text, lang="en", slow=False)
    response.save("response.mp3")
    playsound.playsound("response.mp3", True)
    os.remove("response.mp3")

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
            
    def join(self, *args):
        Thread.join(self, *args)
        return self._return