# Module
from gtts import gTTS
import os

#remove
os.remove("test.mp3")

#input
text = input("text: ")

#gtts
out = gTTS(text=text, lang='ko', slow=False)
out.save("test.mp3")

#play
os.system("start test.mp3")
