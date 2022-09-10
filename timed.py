import PySimpleGUI as sg # Docs : https://www.pysimplegui.org/en/stable/
import datetime
import pygame
import json

# region | Json
def get_json_content(json_file):
    with open(json_file) as file:
        file = json.load(file)
    return file
def add_ringtone(name, path, json_file="settings/user_settings.json"):
    content = {"name": name, "path": path, "id": len(get_ringtone_list())}
    json_content.get("ringtones").append(content)
    with open(json_file, "w") as file:
        json.dump(json_content, file, indent=4)
def add_task(task_type, name="", json_file="settings/user_settings.json"):
    content = {"type": task_type, "name": name, "id": len(get_task_list())}
    json_content.get("tasks").append(content)
    with open(json_file, "w") as file:
        json.dump(json_content, file, indent=4)
def get_ringtone():
    global json_content
    return json_content.get("settings").get("current_ringtone")
def get_ringtone_id():
    global json_content
    return json_content.get("settings").get("current_ringtone_id")
def change_ringtone(new_name, new_id, json_file="settings/user_settings.json"):
    json_content.get("settings")["current_ringtone"] = new_name
    json_content.get("settings")["current_ringtone_id"] = new_id
    with open(json_file, "w") as file:
        json.dump(json_content, file, indent=4)
def change_theme(new_theme, json_file="settings/user_settings.json"):
    json_content.get("settings")["current_theme"] = new_theme
    with open(json_file, "w") as file:
        json.dump(json_content, file, indent=4)
def get_theme():
    global json_content
    return json_content.get("settings").get("current_theme")
def get_ringtone_list():
    global json_content
    return [i.get("name") for i in json_content.get("ringtones")]
def get_task_list():
    global json_content
    task_list = []
    for i in json_content.get("tasks"):
        if i.get("name"):
            task_list.append((i.get("name"), i.get("type")))
        else:
            task_list.append(i.get("type"))
    return task_list
json_content = get_json_content("settings/user_settings.json")
# endregion

# region | Variables
small_text = ('Courier', 14, 'bold')
medium_text = ('Courier', 18, 'bold')
big_text = ('Courier', 24, 'bold')
bigger_text = ('Courier', 69, 'bold')
reset_timer_end = datetime.datetime(2007,2,14)
timer_end = reset_timer_end
timer = '00:00'
relaunch = True
# endregion

# region | Lists
TASKS_DICT = [
    {'task': 'Break',   'timer': 300},
    {'task': 'Lesson',  'timer': 1500},
    {'task': 'Workout', 'timer': 900}
]
TYPE_LIST = [tasks.get("task") for tasks in TASKS_DICT]
tasks_list = get_task_list()
seconds_list = []
for i in range(60):
    seconds = f'0{str(i)}' if len(str(i)) == 1 else str(i)
    seconds_list.append(seconds)
minutes_list = []
for i in range(60):
    minutes = f'0{str(i)}' if len(str(i)) == 1 else str(i)
    minutes_list.append(minutes)
ringtones = get_ringtone_list()
# endregion

# region | Functions
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
    global json_content
    json_content = get_json_content("settings/user_settings.json")
    global reset_timer_end
    global timer_end
    global timer
    global relaunch
    relaunch = False

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
        
        if event in [None, 'Exit'] or relaunch:
            break
        if event == '-ADD-':
            add_task(values['-TYPE-'], values['-TASK-'])
            # if values['-TYPE-']:
            #     timer_end = new_timer(TASKS_DICT[1].get('timer'))
            #     if values['-TASK-']:
            #         list_timer = str(TASKS_DICT[1].get('timer')/60).split(".")
            #         tasks_list.append(f"{list_timer[0]}min{list_timer[1]}0s | " + values['-TASK-'] + " " + values['-TYPE-'])
            #     else:
            #         tasks_list.append(values['-TYPE-'])
            # elif values['-TASK-']:
            #     tasks_list.append(values['-TASK-'])
            window['-LIST-'].update(values=get_task_list())
            window['-TASK-'].update('')
        if event == '-START_TIMER-':
            timer_end = new_timer(60*int(values['-MINUTES-'])+int(values['-SECONDS-'])+1)
            timer = ''.join(':'.join(str(timer_end - get_time(False)).split(':')[1:]).split('.')[:1])
        if event == '-STOP_RINGTONE-':
            timer_end = reset_timer_end
            timer = '00:00'
            pygame.mixer.music.stop()
        if event == 'Settings':
            open_settings_window()

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
    global relaunch
    ringtone_add = [
        [sg.Text('Set:', font=medium_text), sg.Combo(ringtones, size=(None, 10), readonly=True, expand_x=True, key='-RINGTONE-')],
        [sg.Button('Add', expand_x=True, key='-ADD-')]
    ]
    ringtone_add_settings = [
        [sg.Text('Path:', font=medium_text), sg.Input(size=(None, 10), expand_x=True, key='-PATH-'), (sg.FileBrowse())],
        [sg.Text('Name:', font=medium_text), sg.Input(size=(None, 10), expand_x=True, key='-NAME-'), sg.Button('Add', key='-ADD_RINGTONE-')],
    ]
    layout = [
        [sg.Text('Settings', font=big_text)],
        [sg.HSeparator()],
        [sg.Text('Ringtone', font=medium_text, enable_events=True, key='-TITLE-')],
        [sg.Column(ringtone_add, key='-1-'), sg.Column(ringtone_add_settings, visible=False, key='-2-')],
        [sg.HSeparator()],
        [sg.Text('Theme', font=medium_text)],
        [sg.Text('Set:', font=medium_text), sg.Combo(themes, size=(None, 10), readonly=True, expand_x=True, key='-THEME-')],
        [sg.HSeparator()],
        [sg.Button('Apply', key='-APPLY-'), sg.Button('Exit', key='-EXIT-')]]
    settings_window = sg.Window('Settings', layout)
    while True:
        event, values = settings_window.read()
        if event in (None, '-EXIT-'): break
        if event == '-APPLY-':
            if values['-RINGTONE-']:
                try:
                    pygame.mixer.music.load(json_content.get("ringtones")[ringtones.index(values['-RINGTONE-'])].get("path"))
                    change_ringtone(values['-RINGTONE-'], json_content.get("ringtones")[ringtones.index(values['-RINGTONE-'])].get("id"))
                except IndexError:
                    sg.PopupNoBorder("Ringtone can't be empty!")
            if values['-THEME-']:
                relaunch = True
                sg.theme(values['-THEME-'])
                change_theme(values['-THEME-'])
        if event == '-ADD-':
            settings_window['-TITLE-']('Ringtone > Add')
            settings_window['-2-'](visible=True)
            settings_window['-1-'](visible=False)
        if event == '-TITLE-':
            settings_window['-TITLE-']('Ringtone')
            settings_window['-1-'](visible=True)
            settings_window['-2-'](visible=False)
        if event == '-ADD_RINGTONE-':
            add_ringtone(values['-NAME-'], values['-PATH-'])
            ringtones.append(values['-NAME-'])
            settings_window['-RINGTONE-'](values=ringtones)
            settings_window['-PATH-']('')
            settings_window['-TITLE-']('Ringtone')
            settings_window['-1-'](visible=True)
            settings_window['-2-'](visible=False)
    settings_window.close()
# endregion

# PyGame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(json_content.get("ringtones")[get_ringtone_id()].get("path"))

sg.LOOK_AND_FEEL_TABLE[".Main"] = {"BACKGROUND": "#ffffff", "TEXT": "#C100FF", "INPUT": "#dae0e6", "TEXT_INPUT": "#C100FF", "SCROLL": "#C100FF", "BUTTON": ("#FFFFFF", "#C100FF"), "PROGRESS": ("FFFFFF", "C100FF"), "BORDER": 1, "SLIDER_DEPTH": 0, "PROGRESS_DEPTH": 0, "ACCENT1": "#C100FF", "ACCENT2": "#C100FF", "ACCENT3": "#C100FF"}
sg.LOOK_AND_FEEL_TABLE[".DarkMain"] = {"BACKGROUND": "#000000", "TEXT": "#C100FF", "INPUT": "#050505", "TEXT_INPUT": "#C100FF", "SCROLL": "#C100FF", "BUTTON": ("#FFFFFF", "#C100FF"), "PROGRESS": ("FFFFFF", "C100FF"), "BORDER": 1, "SLIDER_DEPTH": 0, "PROGRESS_DEPTH": 0, "ACCENT1": "#C100FF", "ACCENT2": "#C100FF", "ACCENT3": "#C100FF"}
themes = sg.ListOfLookAndFeelValues()

# PySimpleGUI
sg.ChangeLookAndFeel(get_theme())
sg.set_global_icon('icons/Logo.ico')
sg.set_options(font=small_text)

while relaunch:
    open_main_window()