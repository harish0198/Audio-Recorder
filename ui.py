import tkinter as tk
from multi import *
from functools import partial

# Top level window
frame = tk.Tk()
frame.title("Recorder")
frame.geometry('400x200')

# Function for getting Input
# from textbox and printing it
# at label widget
global rec_tim
def Settime():
    
    num = inputtxt.get(1.0, "end-1c")
    lbl.config(text = "Rec time set for: "+num+'sec')
    rec_tim = int(num)
def plybk():
    lbl.config(text = "Playing Recorded audio")
    
# TextBox Creation
inputtxt = tk.Text(frame,height = 1,width = 10)

# Button Creation
settimebt = tk.Button(frame,text = "Set time",command = Settime)
recordbt = tk.Button(frame,text = "Record",command = lambda:record(int(inputtxt.get(1.0, "end-1c"))))
plybkbt = tk.Button(frame,text = "Play back",command = playback)
# Label Creation
lbl = tk.Label(frame, text = "")

inputtxt.pack()
settimebt.pack()
recordbt.pack()
plybkbt.pack()
lbl.pack()
frame.mainloop()
