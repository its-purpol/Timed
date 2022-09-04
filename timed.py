import PySimpleGUI as sg # Docs : https://www.pysimplegui.org/en/stable/
import datetime
import pygame

# Variables | region
small_text = ('Courier', 14, 'bold')
medium_text = ('Courier', 18, 'bold')
big_text = ('Courier', 24, 'bold')
bigger_text = ('Courier', 69, 'bold')
reset_timer_end = datetime.datetime(2007,2,14)
timer_end = reset_timer_end
timer = '00:00'
# endregion

# Lists | region
TYPE_LIST = ['', 'Lesson', 'Workout']
tasks_list = []
tasks_dict = [
    {'task': 'Break',   'timer': 300},
    {'task': 'Lesson',  'timer': 1500},
    {'task': 'Workout', 'timer': 900}
]
seconds_list = []
for i in range(60):
    seconds = f'0{str(i)}' if len(str(i)) == 1 else str(i)
    seconds_list.append(seconds)
minutes_list = []
for i in range(60):
    minutes = f'0{str(i)}' if len(str(i)) == 1 else str(i)
    minutes_list.append(minutes)
ringtones = [
    {'path': './sounds/sunflower.mp3', 'id': '0'},
    {'path': './sounds/never-gonna-give-you-up.mp3', 'id': '1'}
] # Add a feature to add ringtones within the app
ringtones_paths = [ringtone.get('path') for ringtone in ringtones]
# endregion

# Functions | region
def search(path, ringtones):
    return [element for element in ringtones if element['path'] == path]
def get_time(formated=True):
    if formated:
        return datetime.datetime.now().strftime('%H:%M:%S')
    else:
        return datetime.datetime.now()
def get_date():
    return datetime.datetime.now().strftime('%d/%m/%Y')
def new_timer(add_seconds=0):
    return datetime.datetime.now() + datetime.timedelta(seconds=add_seconds)
def check_type():
    task_type = 'Lesson'
    length = 25
    return task_type, length
def open_main_window():
    global reset_timer_end
    global timer_end
    global timer

    menu_def = [['&Timed', ['&Settings', '&Save::savekey', '---', '&Properties', 'E&xit']],
                ['&Edit', ['&Paste', ['Special', 'Normal', ], 'Undo'], ],
                ['&Debugger', ['Popout', 'Launch Debugger']],
                ['&Toolbar', ['Command &1', 'Command &2', 'Command &3', 'Command &4']],
                ['&Help', '&About...']]

    layout = [
        [sg.Menu(menu_def)],
        [
            sg.Text(text='', expand_x=True, justification='left', font=medium_text, key='-DATE-'),
            sg.Text(text='', expand_x=True, justification='right', font=medium_text, key='-TIME-')
        ],
        [sg.HSeparator()],
        [sg.Text(text='', expand_x=True, justification='center', font=bigger_text, pad=(100, 100), key='-TIMER-')],
        [sg.HSeparator()],
        [
            sg.Button('Start', font=small_text, key='-START_TIMER-'),
            sg.Button('Stop', font=small_text, key='-STOP_RINGTONE-'), 
            sg.Frame('', 
            [
                [
                    sg.Combo(minutes_list, font=medium_text, default_value='00', readonly=True, key='-MINUTES-'), 
                    sg.Combo(seconds_list, font=medium_text, default_value='00', readonly=True, key='-SECONDS-')
                ]
            ], 
            border_width=0, element_justification='right', expand_x=True)
        ],
        [
            sg.Listbox(values=tasks_list, font=small_text, expand_x=True, size=(None, 10), key='-LIST-')
        ],
        [
            sg.Text('Task:', font=medium_text), 
            sg.Input(font=medium_text, size=(0, None), expand_x=True, key='-TASK-'),
            sg.Combo(values=TYPE_LIST, font=medium_text, readonly=True, key='-TYPE-'), 
            sg.Button('Add', font=small_text, key='-ADD-')
        ]
    ]

    window = sg.Window('Timed', layout)

    while True:
        event, values = window.read(timeout=1)
        
        if event in [None, 'Exit']:
            break
        if event == '-ADD-':
            if values['-TYPE-']:
                timer_end = new_timer(tasks_dict[1].get('timer'))
                if values['-TASK-']:
                    list_timer = str(tasks_dict[1].get('timer')/60).split(".")
                    tasks_list.append(f"{list_timer[0]}min{list_timer[1]}0s | " + values['-TASK-'] + " " + values['-TYPE-'])
                else:
                    tasks_list.append(values['-TYPE-'])
            elif values['-TASK-']:
                tasks_list.append(values['-TASK-'])
            window['-LIST-'].update(values=tasks_list)
            window['-TASK-'].update('')
        if event == '-START_TIMER-':
            timer_end = new_timer(60*int(values['-MINUTES-'])+int(values['-SECONDS-'])+1)
            timer = ''.join(':'.join(str(timer_end - get_time(False)).split(':')[1:]).split('.')[:1])
        if event == '-STOP_RINGTONE-':
            timer_end = reset_timer_end
            timer = '00:00'
            pygame.mixer.music.stop()
        if event == 'Settings':
            settings_window = open_settings_window()

        local_time = get_time()
        local_date = get_date()
        if timer != '00:00':
            timer = ''.join(':'.join(str(timer_end - get_time(False)).split(':')[1:]).split('.')[:1])
        if get_time() == timer_end.strftime('%H:%M:%S'):
            timer_end = reset_timer_end
            pygame.mixer.music.play()
        if values['-MINUTES-'] == '00' and values['-SECONDS-'] == '00':
            window['-SECONDS-'].update('01')

        window['-DATE-'](local_date)
        window['-TIME-'](local_time)
        window['-TIMER-'](timer)
    window.close()
def open_settings_window():
    layout = [
        [sg.Text('Settings', font=big_text)], [sg.HSeparator()],
        [sg.Text('Ringtone: ', font=medium_text), sg.Combo(ringtones_paths, size=(None, 10), readonly=True, key='-RINGTONE-')],
        [sg.Text('Theme: ', font=medium_text), sg.Combo(themes, size=(None, 10), readonly=True, key='-THEME-')],
        [sg.Button('Apply', key='-APPLY-'), sg.Button('Exit', key='-EXIT-')]]
    settings_window = sg.Window('Settings', layout)
    while True:
        event, values = settings_window.read()
        if event in (None, '-EXIT-'): break
        if event == '-APPLY-':
            if values['-RINGTONE-']:
                try:
                    pygame.mixer.music.load(ringtones[int(search(values['-RINGTONE-'], ringtones)[0].get("id"))].get('path'))
                except IndexError:
                    sg.PopupNoBorder("Ringtone can't be empty!")
            if values['-THEME-']:
                print('New Theme') # add json support and close the window after setting theme
    settings_window.close()
# endregion

# PyGame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(ringtones[0].get('path'))

sg.LOOK_AND_FEEL_TABLE["Main"] = {"BACKGROUND": "#ffffff", "TEXT": "#C100FF", "INPUT": "#dae0e6", "TEXT_INPUT": "#C100FF", "SCROLL": "#C100FF", "BUTTON": ("#FFFFFF", "#C100FF"), "PROGRESS": ("FFFFFF", "C100FF"), "BORDER": 1, "SLIDER_DEPTH": 0, "PROGRESS_DEPTH": 0, "ACCENT1": "#C100FF", "ACCENT2": "#C100FF", "ACCENT3": "#C100FF"}
sg.LOOK_AND_FEEL_TABLE["Dark Main"] = {"BACKGROUND": "#000000", "TEXT": "#C100FF", "INPUT": "#050505", "TEXT_INPUT": "#C100FF", "SCROLL": "#C100FF", "BUTTON": ("#FFFFFF", "#C100FF"), "PROGRESS": ("FFFFFF", "C100FF"), "BORDER": 1, "SLIDER_DEPTH": 0, "PROGRESS_DEPTH": 0, "ACCENT1": "#C100FF", "ACCENT2": "#C100FF", "ACCENT3": "#C100FF"}
themes = sg.ListOfLookAndFeelValues()

# PySimpleGUI
sg.ChangeLookAndFeel('Dark Main')
sg.set_global_icon('icons/Logo.ico')
sg.set_options(font=small_text)

open_main_window()