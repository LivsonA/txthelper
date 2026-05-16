import json
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showwarning, showinfo, askyesno
from datetime import datetime
from tkinter import colorchooser
from json import *
import keyboard
import pyperclip
import requests
from bs4 import BeautifulSoup
from urllib import request
from urllib.parse import quote
from PIL import Image, ImageDraw, ImageTk
from langdetect import detect, DetectorFactory


DetectorFactory.seed = 0


def date_():
    a = datetime.now().hour
    if 7 <= a <= 20:
        choice_color_theme('ligth')
    else:
        choice_color_theme('dark')


def choice_color_theme(theme='ligth'):
    global qwe, cov, bob, result1, result2, result3, result4
    if theme == 'dark':
        сolpalet = {
            'C1': '#121212',
            'C2': '#1E1E1E',
            'C3': '#2D2D2D',
            'C4': '#252525',
            'C5': '#333333',
            'C6': '#424242',
            'C7': '#535353',
            'C8': '#616161',
            'C9': '#252525',
            'C10': '#E0E0E0',
            'C11': '#BB86FC',
            'C12': '#03DAC6'}
    else:
        сolpalet = {'C1': '#f5deb3',
            'C2': '#ffffe0',
            'C3': '#c8e6c9',
            'C4': '#b0e0e6',
            'C5': '#b0e0e6',
            'C6': '#c8e6c9',
            'C7': '#ffffe0',
            'C8': '#f5deb3',
            'C9': '#ffffe0',
            'C10': '#000000',
            'C11': '#1E88E5',
            'C12': '#FF5252'}

    frame1.configure(bg=сolpalet['C1'])
    labl.configure(bg=сolpalet['C1'], fg=сolpalet['C10'])
    frame2.configure(bg=сolpalet['C1'])
    labl2.configure(bg=сolpalet['C1'], fg=сolpalet['C10'])
    labl23.configure(bg=сolpalet['C1'], fg=сolpalet['C10'])
    text3.configure(bg=сolpalet['C4'], fg=сolpalet['C10'])
    text90.configure(bg=сolpalet['C4'], fg=сolpalet['C10'])
    labl1.configure(bg=сolpalet['C1'], fg=сolpalet['C10'])
    lenbutt.configure(bg=сolpalet['C6'], fg=сolpalet['C10'])
    labl_m.configure(bg=сolpalet['C1'], fg=сolpalet['C10'])
    lenbutt1.configure(bg=сolpalet['C6'], fg=сolpalet['C10'])
    labl3.configure(bg=сolpalet['C1'], fg=сolpalet['C10'])
    lenbutt2.configure(bg=сolpalet['C6'], fg=сolpalet['C10'])
    labl4.configure(bg=сolpalet['C1'], fg=сolpalet['C10'])
    Entr.configure(bg=сolpalet['C4'], fg=сolpalet['C10'])
    labl41.configure(bg=сolpalet['C1'], fg=сolpalet['C10'])
    lenbutt11.configure(bg=сolpalet['C6'], fg=сolpalet['C10'])
    Morfbutt.configure(bg=сolpalet['C6'], fg=сolpalet['C10'])
    result1 = сolpalet['C2']
    result2 = сolpalet['C2']
    result3 = сolpalet['C2']
    result4 = сolpalet['C2']


def prov():
    rt = Entr.get().strip()
    o = ''
    for s in rt:
        if 'А' <= s.upper() <= 'Я':
            o += s.lower()
    return o


def cl():
    text90.configure(state=NORMAL)
    text90.delete(1.0, END)
    text90.insert(END, horoscope())
    text90.configure(state=DISABLED)


def cl2():
    text90.configure(state=NORMAL)
    text90.delete(1.0, END)
    text90.insert(END, razbor2())
    text90.configure(state=DISABLED)


def horoscope():
    text12 = Entr.get().strip()
    print(detect(text12))
    if detect(text12)=='cy':
        showwarning(title='внимание', message='напиши слово на русском языке!')

    else:
        try:
            if text12.isalpha() == True:
                otv = ''
                url = 'https://morphologyonline.ru/{0}'.format(quote(text12))
                test = requests.get(url)
                bs = BeautifulSoup(test.text, 'html.parser')
                abc = bs.find('ol').get_text().split('.')
                for st in abc:
                    otv += st.strip().replace('Часть речи ', '', 1) + '\n'
                return otv
            else:
                showwarning(title='Внимание', message='Сначала напиши слово')
        except AttributeError:
            showwarning(title='Внимание', message=f'Напиши правильно слово {text12}')



def razbor2():
    word = Entr.get().strip()
    if detect(word) == 'cy':
        showwarning(title='внимание', message='напиши слово на русском языке!')
        print(detect(word))
    else:
        print(detect(word))
        try:
            if word.isalpha() == True:
                firstlet=word[0].upper()
                Url='https://morphemeonline.ru/{1}/{0}'.format(word, firstlet )
                test = requests.get(Url)
                bs = BeautifulSoup(test.text, 'html.parser')
                result=bs.find(class_='fs-5 bg-light d-inline-block p-3').get_text().replace(':', '\n')
                return result
            else:
                showwarning(title='Внимание', message='Сначала напиши слово')
        except AttributeError:
            showwarning(title='Внимание', message=f'Напиши правильно слово {word}')



def paste_():
    text3.insert(1.0, pyperclip.paste())

def copy():
    copytxt=pyperclip.copy(str(text3.selection_get()))


def esc():
    a = askyesno(title='Внимание!', message='Вы точно хотите выйти?')
    if a:
        mainwind.destroy()


def analyze():
    m = Mystem()
    a = text.get(1.0, END)
    analyz = m.analyze(a)
    print(analyz[0]['analysis'][0]['gr'])
    analyzer = pymorphy2.MorphAnalyzer()
    analyzer = analyzer.parse((text.get(1.0, END)))[0]
    print(type(analyzer))


def sloyw():
    # b = len([x for x in text3.get(1.0, END) if x.isalpha()])

    labl_m.configure(text=len(text3.get(1.0, END).split()))


def lentext():
    labl23.configure(text=len(text3.get(1.0, END)) - 1)


def lentext1():
    labl1.configure(text=len(text3.get(1.0, END).replace(' ', '').strip().replace(',', '').replace("'", '')))


def clouse(window):
    window.grab_release()
    window.destroy()


def otrisovka():
    im = Image.new("RGB", (31, 31), "white")
    draw = ImageDraw.Draw(im)
    draw.rectangle([0, 0, 30, 30], fill=result2, outline='#000', width=1)
    photo = ImageTk.PhotoImage(im)
    imLab = Label(new_win, image=photo)
    imLab.image = photo
    imLab.place(x=5, y=75)

    im2 = Image.new("RGB", (31, 31), "white")
    draw2 = ImageDraw.Draw(im2)
    draw2.rectangle([0, 0, 30, 30], fill=result1, outline='#000', width=1)
    photo2 = ImageTk.PhotoImage(im2)
    imLab2 = Label(new_win, image=photo2)
    imLab2.image = photo2
    imLab2.place(x=5, y=210)

    im3 = Image.new("RGB", (31, 31), "white")
    draw3 = ImageDraw.Draw(im3)
    draw3.rectangle([0, 0, 30, 30], fill=result3, outline='#000', width=1)
    photo3 = ImageTk.PhotoImage(im3)
    imLab3 = Label(new_win, image=photo3)
    imLab3.image = photo3
    imLab3.place(x=5, y=120)
    imLab3.update_idletasks()

    im4 = Image.new("RGB", (31, 31), "white")
    draw4 = ImageDraw.Draw(im4)
    draw4.rectangle([0, 0, 30, 30], fill=result4, outline='#000', width=1)
    photo4 = ImageTk.PhotoImage(im4)
    imLab4 = Label(new_win, image=photo4)
    imLab4.image = photo4
    imLab4.place(x=5, y=165)


def newwin():
    global new_win, result2, result3
    global mystyle
    new_win = Toplevel()
    new_win.title("Персонализация")
    new_win.geometry('250x840+0+20')
    new_win.configure(bg='#b8b2b2')
    new_win.protocol("WM_DELETE_WINDOW", lambda: clouse(new_win))
    close_button = Button(new_win, text="❌", font=(20), command=lambda: clouse(new_win), bg='#f70202')
    close_button.place(relx=0.879999, rely=0)

    flagbut = IntVar()
    flagbut.set(0)
    radbutt = Radiobutton(new_win, text='молочная тема', value=1, variable=flagbut, bg='#b8b2b2', command=lambda: choice_color_theme('ligth'))
    radbutt.place(x=20, y=20)
    radbutt2 = Radiobutton(new_win, text='тёмная тема', value=2, variable=flagbut, bg='#b8b2b2', command=lambda: choice_color_theme('dark'))
    radbutt2.place(x=20, y=40)
    buttchosen = Button(new_win, text='сменить цвет обоев', command=choice_color)
    buttchosen.place(x=50, y=80)
    buttchosen1 = Button(new_win, text='сменить цвет всех кнопок', command=choice_colorbutt)
    buttchosen1.place(x=50, y=125)
    buttchosen2 = Button(new_win, text='сменить цвет всех окн ввода текста', command=choice_colorеtext)
    buttchosen2.place(x=50, y=170)
    buttchosen3 = Button(new_win, text='сменить цвет всех шрифтов', command=choice_colorеfont)
    buttchosen3.place(x=50, y=215)

    otrisovka()

    new_win.update_idletasks()
    new_win.grab_set()
    new_win.overrideredirect(True)


def choice_colorbutt():
    global result3, imLab3, imLab2, imLab
    result = colorchooser.askcolor(initialcolor="black")
    result3 = result[1]
    lenbutt.configure(bg=result[1])
    lenbutt2.configure(bg=result[1])
    lenbutt1.configure(bg=result[1])
    lenbutt11.configure(bg=result[1])
    otrisovka()


def choice_colorеtext():
    global result4, imLab3, imLab2, imLab
    result = colorchooser.askcolor(initialcolor="black")
    result4 = result[1]
    text3.configure(bg=result[1])
    text90.configure(bg=result[1])
    otrisovka()


def choice_colorеfont():
    global result1, imLab3, imLab2, imLab
    result = colorchooser.askcolor(initialcolor="black")
    result1 = result[1]
    labl.configure(fg=result[1])
    labl23.configure(fg=result[1])
    text3.configure(fg=result[1])
    text90.configure(fg=result[1])
    lenbutt.configure(fg=result[1])
    lenbutt1.configure(fg=result[1])
    lenbutt2.configure(fg=result[1])
    labl1.configure(fg=result[1])
    labl_m.configure(fg=result[1])
    labl3.configure(fg=result[1])
    labl4.configure(fg=result[1])
    Entr.configure(fg=result[1])
    labl2.configure(fg=result[1])
    labl41.configure(fg=result[1])
    otrisovka()


def choice_color():
    global result2, imLab3, imLab2, imLab
    resultw = colorchooser.askcolor(initialcolor="black")
    result2 = resultw[1]
    frame2.configure(bg=resultw[1])
    frame1.configure(bg=resultw[1])
    labl.configure(bg=resultw[1])
    labl2.configure(bg=resultw[1])
    otrisovka()


result4 = 0
result1 = 0
result2 = 0
result3 = 0
mainwind = Tk()
mainwind.state('zoomed')
mainwind.title('проект')
mainwind.overrideredirect(True)

main_menu = Menu()

file_menu = Menu(tearoff=0)
file_menu.add_command(label="Персонализация", font=('Arial black', 10), command=newwin)
main_menu.add_cascade(label="Настройки", menu=file_menu, font=('Arial black', 8))
file_menu.add_command(label='Выйти', font=('Arial black', 10), command=esc)

notebook = ttk.Notebook(mainwind)
notebook.place(relheight=1, relwidth=1, relx=0, rely=0)

frame1 = Frame(notebook)
notebook.place(relheight=1, relwidth=1, relx=0, rely=0)

frame2 = Frame(notebook)
notebook.place(relheight=1, relwidth=1, relx=0, rely=0)

notebook.add(frame1, text="счетчик")
notebook.add(frame2, text="морфологический разбор")

labl = Label(frame1, text='Счетчик', font=('Arial black', 30))
labl.place(relx=0.4, rely=0, )

labl2 = Label(frame2, text='Морфологический разбор', font=('Arial black', 30))
labl2.place(relx=0.25, rely=0, )

text3 = Text(frame1, font=('Arial black', 10))
text3.place(relx=0.25, rely=0.389999, relheight=0.6, relwidth=0.5)

mystyle = ttk.Style()
mystyle.configure('styleScale',
                  background="#b8b2b2")
mystyle.configure("TNotebook.Tab", font=("Arial black", 10, "bold"))

text90 = Text(frame2, font=('Arial black', 10), state=DISABLED, wrap='word')
text90.place(relx=0.35, rely=0.2, relheight=0.5, relwidth=0.4)

lenbutt= Button(frame1, text='Анализировать все символы', font=('Arial black', 10), command=lentext)
lenbutt.place(relx=0.08, rely=0.5, relwidth=0.16)

lenbutt1 = Button(frame1, text='Анализировать кол-во букв', font=('Arial black', 10), command=lentext1)
lenbutt1.place(relx=0.08, rely=0.4, relwidth=0.16)

text1 = Text(frame1, font=('Arial', 10), state=DISABLED)
text1.place(relx=0.75, rely=0.389999, relheight=0.6, relwidth=0.06)

lenbutt11 = Button(frame2, text='Морфологическй разбор', font=('Arial black', 10), command=cl)
lenbutt11.place(relx=0.03, rely=0.25)

Morfbutt = Button(frame2, text='Морфемный разбор', font=('Arial black', 10), command=cl2)
Morfbutt.place(relx=0.03, rely=0.35)


butt = Button(frame1, text='')

lenbutt2 = Button(frame1, text='Анализировать кол-во слов', font=('Arial black', 10), command=sloyw)
lenbutt2.place(relx=0.08, rely=0.6, relwidth=0.16)

labl1 = Label(frame1, text='0', borderwidth=10)
labl1.place(relx=0.76, rely=0.415, relheight=0.045, relwidth=0.042)

labl23 = Label(frame1, text='0', borderwidth=10)
labl23.place(relx=0.76, rely=0.5, relheight=0.045, relwidth=0.042)

labl_m = Label(frame1, text='0', borderwidth=10)
labl_m.place(relx=0.76, rely=0.585, relheight=0.045, relwidth=0.042)

labl3 = Label(frame1, text='кол-во букв', borderwidth=10)
labl3.place(relx=0.82, rely=0.415, relheight=0.045)

labl41 = Label(frame1, text='со всеми символами ', borderwidth=10)
labl41.place(relx=0.82, rely=0.5, relheight=0.045)

labl4 = Label(frame1, text='кол-во слов', borderwidth=10)
labl4.place(relx=0.82, rely=0.585, relheight=0.045)

Entr = Entry(frame2)
Entr.place(relx=0.03, rely=0.2, relheight=0.045, relwidth=0.3)

date_()

keyboard.add_hotkey('Escape', esc)
keyboard.add_hotkey('ctrl+v', paste_)
keyboard.add_hotkey('ctrl+c', copy)
mainwind.config(menu=main_menu)
mainwind.mainloop()
