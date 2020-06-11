# Module
from gtts import gTTS
import os

# Remove
if os.path.exists("test.mp3"):
    os.remove("test.mp3")

# Input
text = input("text: ")

# Gtts
out = gTTS(text=text, lang='ko', slow=False)
out.save("test.mp3")

# Play
os.system("start test.mp3")
