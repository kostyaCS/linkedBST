# from gtts import gTTS
# from pydub import AudioSegment
# from pydub.playback import play

# def text_to_speech(text, lang='en'):
#     tts = gTTS(text=text, lang=lang)
#     tts.save('output.mp3')
#     speech = AudioSegment.from_mp3('output.mp3')
#     play(speech)

# text = "Hello, how are you?"
# text_to_speech(text)

import pyttsx3

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Example usage
text = "Hello, how are you?"
text_to_speech(text)