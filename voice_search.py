import speech_recognition as sr

def search():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # read the audio data from the default microphone
        audio_data = r.record(source, duration=5)
        # convert speech to text
        type = r.recognize_google(audio_data)
        type = str(type).title()
        return type
    
