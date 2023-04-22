import webbrowser
from tkinter import *
import tkinter.font as font
import os


def middle(c):
    if c == 1:
        mmenu.destroy()
        os.system('python3 realtimeTimetable.pyw')
    elif c == 2:
        mmenu.attributes('-topmost',False)
        webbrowser.open_new('https://gems.phoenixclassroom.com/Account/login')
    elif c == 3:
        mmenu.attributes('-topmost', False)
        webbrowser.open_new('https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley')


mmenu = Tk()
mmenu.title('Main Menu')
canvas = Canvas(mmenu, width=470, height=270, bg='#1CAFEE')
canvas.grid(rowspan=4, columnspan=3)

bg = PhotoImage(file='icons/bg.png')
bglabel=Label(mmenu, image = bg)
bglabel.place(x=0,y=0)

mainlabel = Label(mmenu, text='MAIN MENU', bg='#1CBCF3')
mainlabel['font']=font.Font(family='Futura',weight='bold',size=14)
mainlabel.grid(row=0, column=0, columnspan=3)
rlabel = Label(mmenu, text = "Hold Shift + Esc to Return to Main Menu")
rlabel.grid(row=3, column = 1)


tticon = PhotoImage(file='icons/tticon.png')
ttbutton = Button(mmenu, height=75, width=75, bg = '#20D2FA', image=tticon, borderwidth=0, command=lambda: middle(1))
ttbutton.grid(row=1, column=0)
ttlabel = Label(mmenu, text='Realtime\nTimetable', bg='#1CBCF3')
ttlabel['font']=font.Font(family='Futura',size=10)
ttlabel.grid(row=2, column=0)


n1icon = PhotoImage(file='icons/phicon.png')
n1button = Button(mmenu, height=75, width=75, bg = '#1C9FE8', image=n1icon, borderwidth=0, command=lambda: middle(2))
n1button.grid(row=1, column=1)
n1label = Label(mmenu, text='Open Pheonix\nClassroom', bg='#1C9FE8')
n1label['font']=font.Font(family='Futura',size=10)
n1label.grid(row=2, column=1)


n2icon = PhotoImage(file='icons/ukicon.png')
n2button = Button(mmenu, height=75, width=75, bg = '#2A80D5', image=n2icon, borderwidth=0, command=lambda: middle(3))
n2button.grid(row=1, column=2)
n2label = Label(mmenu, text='Something 2', bg='#2A80D5')
n2label['font']=font.Font(family='Futura',size=10)
n2label.grid(row=2, column=2)

mmenu.attributes('-topmost',True)

mmenu.mainloop()
