import PySimpleGUI as sg # Docs : https://www.pysimplegui.org/en/stable/
from datetime import datetime

# Lists
TYPE_LIST = ['', 'Lesson', 'Workout']
listbox = []

# Functions
def update():
    return datetime.now().strftime('%H:%M:%S'), datetime.now().strftime('%d/%m/%Y')

# def check_type():
#     task_type = 'Lesson'
#     length = 25
#     return task_type, length

# PySimpleGUI
sg.theme('reddit')

menu_def = [['&File', ['!&Open', '&Save::savekey', '---', '&Properties', 'E&xit']],
            ['&Edit', ['!&Paste', ['Special', 'Normal', ], 'Undo'], ],
            ['&Debugger', ['Popout', 'Launch Debugger']],
            ['&Toolbar', ['Command &1', 'Command &2', 'Command &3', 'Command &4']],
            ['&Help', '&About...']]

layout = [
    # [
    #     sg.Menu(menu_def)
    # ],
    [
        sg.Text(text='', expand_x=True, justification='left', font=('Courier', 18, 'bold'), key='-DATE-'),
        sg.Text(text='', expand_x=True, justification='right', font=('Courier', 18, 'bold'), key='-TIME-')
    ],
    [
        sg.HSeparator()
    ],
    [
        sg.Text(text='0:00', expand_x=True, justification='center', font=('Courier', 69, 'bold'), pad=(100, 100), key='-STOPWATCH-')
    ],
    # [
    #     sg.Listbox(values=listbox, expand_x=True, size=(None, 5), key='-LIST-')
    # ],
    # [
    #     sg.Input(key='-TASK-'), 
    #     sg.Combo(values=TYPE_LIST, key='-TYPE-'), 
    #     sg.Button('Add', key='-ADD-')
    # ]
]

window = sg.Window('Timed', layout)      

while True:
    event, values = window.read(timeout=1)
    
    if event in [None, 'Exit']:
        break

    if event == '-ADD-':
        print(values['-TASK-'])
        print(values['-TYPE-'])
        listbox.append((values['-TASK-'] + " " + values['-TYPE-']))
        window['-LIST-'].update(values=listbox)
        window['-TASK-'].update('')
    
    local_time, local_date = update()
    window['-TIME-'](local_time)
    window['-DATE-'](local_date)
window.close()