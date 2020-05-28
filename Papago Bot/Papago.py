import subprocess
from tkinter import *

window = Tk()
window.title("Papago")
window.iconbitmap(default="Papago.ico")
window.resizable(False, False)

def Start():
    window.destroy()
    subprocess.call(["python", "source/PapagoMain.py"])

label = Label(text="\n본 프로그램은 디스코드 봇 프로그램으로\nPapago API를 사용하였습니다.")
label.pack()

button = Button(window, text="계속", command=Start)
button.pack()

window.mainloop()