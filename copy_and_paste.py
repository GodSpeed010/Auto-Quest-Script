import re
import pyperclip
from pywinauto import Application
from pywinauto.keyboard import send_keys
import keyboard
import time
from tkinter import Tk, filedialog
import warnings
warnings.simplefilter('ignore', category=UserWarning) #hide the 32-bit python warning

def main():
    root = Tk() # pointing root to Tk() to use it as Tk() in program.
    root.withdraw() # Hides small tkinter window.
    root.attributes('-topmost', True) # Opened windows will be active. above all windows despite of selection.

    open_file = filedialog.askopenfilename(title='Select quest text file', filetypes=(('Text Files', '*.txt'),('All Files', '*.*'))) # Returns opened path as str

    infile = open(open_file, 'r', encoding='utf8')
    quests = infile.read()
    infile.close()

    quest_re = re.compile(r'^([\u27a4|\u25E2].+?\*\* \*\*$)', re.MULTILINE | re.DOTALL) #regex for each quest block
    quest_arr = quest_re.findall(quests) # gets a list of all the quests

    input('Enter any key when you are in the desired channel') #prep for pasting the quests
    temp = []
    #not sending last quest(s) because it wasn't full
    while len(quest_arr) >=1: # keep going until no more quests to post
        if get_list_length(temp) + get_list_length(quest_arr) <= 2000: #sum of all remaining quests length is < 2000
            temp = quest_arr #todo we can just get all the quests
            pyperclip.copy('\n'.join(temp))
            quest_arr.clear()
            send_to_discord()
            quit()
    
        if get_list_length(temp) + len(quest_arr[0]) <= 2000: # if another quest will not exceed the discord char limit, add it to the list
            temp.append(quest_arr.pop(0))
        else: # if we can't add any more quests without going over word limit; get_list_length(temp) + len(quest_arr[0]) >= 2000
            pyperclip.copy('\n'.join(temp))
            temp.clear()
            send_to_discord()

def send_to_discord():
    #make discord window focused
    app = Application().connect(title_re='.*Discord') #find application using regex on program name
    window = app.window(title_re='.*Discord') # find application window using regex on program name
    
    window.set_focus()

    send_keys('^v')

    #wait for user to press enter; send the message in channel
    keyboard.wait(hotkey='enter')
    time.sleep(0.2)
   
def get_list_length(list):
    total = 0
    for x in list:
        total += len(x)
    return total

main()