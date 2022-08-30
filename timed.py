import PySimpleGUI as sg # Docs : https://www.pysimplegui.org/en/stable/
import datetime

# Lists
TYPE_LIST = ['', 'Lesson', 'Workout']
SECONDS_LIST = ['00', '30', '60']
listbox = []

# Functions
def get_time(formated=True):
    if formated:
        return datetime.datetime.now().strftime('%H:%M:%S')
    else:
        return datetime.datetime.now()

def get_date():
    return datetime.datetime.now().strftime('%d/%m/%Y')

def new_timer(add_seconds=0.0):
    return datetime.datetime.now() + datetime.timedelta(seconds=add_seconds)

def make_new_timer_window():
    layout = [[sg.Input('', size=(None, 10)), sg.Button('New', key='-NEW_TIMER-')]]
    return sg.Window('New timer', layout)

# def check_type():
#     task_type = 'Lesson'
#     length = 25
#     return task_type, length

# PySimpleGUI
sg.theme('Black')

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
        sg.Text(text='', expand_x=True, justification='center', font=('Courier', 69, 'bold'), pad=(100, 100), key='-TIMER-')
    ],
    [
        sg.Frame('', 
        [
            [sg.Combo(SECONDS_LIST, key='-SECONDS-'), sg.Button(image_filename='icon/plus_icon.png', image_size=(50, 50), image_subsample=(10), key='-NEW_TIMER-')]
        ], 
        border_width=0, element_justification='right', expand_x=True)
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

timer_end = new_timer(0)
timer = '00:00'

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
    if event == '-NEW_TIMER-':
        timer_end = new_timer(int(values['-SECONDS-'])+1)
        timer = ''.join(':'.join(str(timer_end - get_time(False)).split(':')[1:]).split('.')[:1])
        window['-SECONDS-'].update('')

    local_time = get_time()
    local_date = get_date()
    if timer != '00:00':
        timer = ''.join(':'.join(str(timer_end - get_time(False)).split(':')[1:]).split('.')[:1])

    window['-DATE-'](local_date)
    window['-TIME-'](local_time)
    window['-TIMER-'](timer)
window.close()