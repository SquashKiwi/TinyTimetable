from tkinter import *
from tkinter.ttk import Progressbar
from openpyxl import load_workbook
import datetime
import keyboard
import os

try:
    import winsound
except:
    pass

# GUI
root = Tk()
root.title('Realtime Timetable')

canvas = Canvas(root, width=400, height=150, bg='#dbf6e9')
canvas2 = Canvas(root, width=400, height=50, bg='#ffffff')
canvas.grid(rowspan=4, columnspan=3)
canvas2.grid(columnspan=3)

progress = Progressbar(root, orient=HORIZONTAL, length=250, mode='determinate')
progress.grid(row=4, column=1, columnspan=2)
prgLabel = Label(text='Progress: ', bg='#ffffff')
prgLabel.grid(row=4, column=0)

sound = True

# Current Period
# Display
curr_prd = StringVar()
curr_prd.set("Current Period")
current = Button(root, state=DISABLED, textvariable=curr_prd, height=6, width=13, bg='#ff7f3b',
                 disabledforeground='black')
current.grid(column=1, row=1)

# Label
currLabel = Label(text='This Period:', bg='#dbf6e9')
currLabel.grid(row=0, column=1)

curr_end = StringVar()
curr_end_label = Label(root, textvariable=curr_end, bg='#dbf6e9')
curr_end.set('Ends in: ')
curr_end_label.grid(row=3, column=1)

# Next Period
# Label
nextLabel = Label(text='Next Period:', bg='#dbf6e9')
nextLabel.grid(row=0, column=2)

# Display
next_prd = StringVar()
next_prd.set('Next Period')
next = Button(root, state=DISABLED, textvariable=next_prd, height=3, width=10, bg='#ffc93c', disabledforeground='black')
next.grid(row=1, column=2)

# Previous Period
# Label
prevLabel = Label(text='Last Period: ', bg='#dbf6e9')
prevLabel.grid(row=0, column=0)

# Display
prev_prd = StringVar()
prev_prd.set('Prev Period')
prev = Button(root, state=DISABLED, textvariable=prev_prd, height=3, width=10, bg='#ffc93c', disabledforeground='black')
prev.grid(row=1, column=0)

# Break and End Labels
brk_time = StringVar()
brk_time.set('Next Break in: ')
brkLabel = Label(textvariable=brk_time, bg='#dbf6e9')
brkLabel.grid(row=3, column=0)

end_time = StringVar()
end_time.set('School ends in: ')
endLabel = Label(textvariable=end_time, bg='#dbf6e9')
endLabel.grid(row=3, column=2)

# Logic
wb = load_workbook('Timetable.xlsx')
sh = wb['Timetable']


def getPrds():  # gets todays periods from excel sheet
    now = datetime.datetime.now()
    day = now.strftime('%a')
    day_dict = {'Sun': '2', 'Mon': '3', 'Tue': '4', 'Wed': '5', 'Thu': '6'}
    prd = 'BCDEFGHIJKLMNOPQRSTUVWXYZ'
    if day not in day_dict:
        return None
    else:
        prdList = []
        for i in prd:
            pos = i + day_dict[day]
            if sh[pos].value is not None:
                prdList.append(sh[pos].value)
            else:
                break
        prdList.append('End')
        return prdList


def notSchoolDay():  # if today is not a working day, this function is called
    curr_prd.set("You don't have\n school today!")
    curr_end.set("Enjoy your day :)")
    next_prd.set(':)')
    prev_prd.set(':)')
    brk_time.set('Have fun!')
    end_time.set('Have fun!')


def getTime():  # Taking duration of period from excel sheet, making a list of starting time of each period
    timeList = [sh['B7'].value]
    for i in prdList:
        if i == 'BREAK':
            a = add_delta(timeList[-1], sh['B9'].value)
            timeList.append(datetime.time(int(a.strftime('%H')), int(a.strftime('%M'))))
        elif i == 'End':
            break
        else:
            a = add_delta(timeList[-1], sh['B8'].value)
            timeList.append(datetime.time(int(a.strftime('%H')), int(a.strftime('%M'))))
    return timeList


def add_delta(tm, delta):  # Adds x number of minutes to y time (Eg: 07:40 + 10 = 07:50)
    return (datetime.datetime.combine(datetime.date.today(), tm) + datetime.timedelta(minutes=delta)).time()


def timeDiff(a, b):  # Returns difference between 2 times (Eg: 7:50 - 7:40 = 0:10)
    dta = datetime.datetime.combine(datetime.date.today(), a)
    dtb = datetime.datetime.combine(datetime.date.today(), b)
    return dtb - dta


def check():  # Main logic of program
    if keyboard.is_pressed('esc+shift') == True:
            root.destroy()
            os.system('python mainmenu.py')
            exit()

    global ind, sound
    timenow = datetime.datetime.now().time()
    if timenow > prdTime[-1]:  # If current time is past school hours, do this:
        progress['value'] = 100
        curr_prd.set("You're done!")
        curr_end.set('Have a nice day :D')
        next_prd.set('Enjoy!')
        end_time.set('School over :)')
        brk_time.set('School over :)')
        prev_prd.set(prdList[-2])
        if sound is True:  # And play beeping sound
            winsound.Beep(2500, 350)
            winsound.Beep(2000, 350)
            sound = False

    elif timenow < prdTime[0]:  # if current time is before school hours, do this:
        curr_prd.set("Yet to start")
        brk_time.set('Get ready for class')
        end_time.set('Get ready for class')
        curr_end.set(f'Starts in: {str(timeDiff(timenow, prdTime[ind]))[:7]}')
        next_prd.set(prdList[0])

    else:  # if current time is within school hours, do this:
        for i in prdTime[ind:]:
            if timenow > i:  # Determines current period
                curr_prd.set(prdList[prdTime.index(i)])
                next_prd.set(prdList[prdTime.index(i) + 1])
                ind += 1
                progress['value'] = (ind / 10) * 100
                if ind > 1:
                    prev_prd.set(prdList[prdTime.index(i) - 1])
                    winsound.Beep(2500, 350)

        curr_end.set(
            f'Time till Period Ends:\n {str(timeDiff(timenow, prdTime[ind]))[2:7]}')  # calculate time remaining in current period

        if 'BREAK' in prdList[ind:]:  # calculate time till next break
            brk_time.set(
                f'Time till Next Break:\n {str(timeDiff(timenow, prdTime[ind:][prdList[ind:].index("BREAK")]))[:7]}')

        else:
            brk_time.set('No more breaks :/')
        end_time.set(
            f'Time till School Ends:\n {str(timeDiff(timenow, prdTime[-1]))[:7]}')  # calculate time remaining for school to end
    root.after(1000, check)


ind = 0
curr = datetime.time(0, 0)
prdList = getPrds()
if prdList is not None:  # Check if today is a working day
    prdTime = getTime()
    root.after(1, check)
else:
    notSchoolDay()

root.attributes('-topmost',True)

root.mainloop()
