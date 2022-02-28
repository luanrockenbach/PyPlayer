#   LUAN ROCKENBACH DA SILVA
#   26/09/2021
#   importing librarys


import pygame
from tkinter import *
from tkinter import filedialog
from tkinter import font
import json
import os
import time
from mutagen.mp3 import MP3
from colour import Color
from tkinter import ttk
import urllib.request
import re
from moviepy.audio.io.AudioFileClip import AudioFileClip
from PIL import Image, ImageTk
import random
import pytube


#   Initial Variables
is_playing = None
user_name = os.environ.get("USERNAME")
input_tk = None
new_window = None
letter_input_tk = None
is_paused = None
imported_songs = []
song_total_length = None
artist_input = ''
music_name_input = ''
current = 0
stoped = True
slider_active = False
repeat_loop = 0
dict_directory = {}

#   Initialize pygame
pygame.mixer.init()

#   Reading in the json file the last colors player set configurations
try:
    with open('theme.json', 'r', encoding='utf-8', errors='ignore') as jfile:

        reader = json.load(jfile)

        player_bg_color = reader.get('player_bg_color', 'white')
        playlist_viewer_color = reader.get('playlist_viewer_color', 'black')
        playlist_bar_color = reader.get('playlist_bar_color', 'white')
        letter_color = reader.get('letter_color', '#fcb505')
        select_letter_color = reader.get('select_letter_color', 'black')
        song_label_color = reader.get('song_info_label', 'black')


except FileNotFoundError:
    #   Players colors set variables
    player_bg_color = 'white'
    playlist_viewer_color = 'black'
    playlist_bar_color = 'white'
    letter_color = '#fcb505'
    select_letter_color = 'black'
    song_label_color = 'black'

#   Stating Tkinter window
root = Tk()
root.title("PyPlayer")
root.iconbitmap('music-notes.ico')
root.geometry('350x500')
root['bg'] = player_bg_color


#   Add song function
def add_song():
    global user_name

    song_dir = filedialog.askopenfilename(initialdir=f'C:\\Users\\{user_name}\\Music\\', title='Choose A Song')

    #   Removing file path and .mp3 from music name to show in listbox
    song = os.path.basename(song_dir).replace('.mp3', '')

    if song + '\n' not in imported_songs:
        imported_songs.append(song + '\n')
        song_box.insert(END, song)

    #   Turning song box strings into bold
    bolded = font.Font(weight='bold', size='9')  # will use the default font
    song_box.config(font=bolded)

    dict_directory[song] = song_dir


#   Add many songs to the playlist
def add_many_songs():
    songs_dir = filedialog.askopenfilenames(initialdir=f'C:\\Users\\{user_name}\\Music\\', title='Choose Many Songs')

    #   Loop for remove file path and .mp3 from many music names to show in listbox
    for song in songs_dir:
        song_name = os.path.basename(song)
        song_name = song_name.replace('.mp3', '')

        if song + '\n' not in imported_songs:
            imported_songs.append(song_name + '\n')
            song_box.insert(END, song_name)

        #   Turning song box strings into bold
        bolded = font.Font(weight='bold', size='9')  # will use the default font
        song_box.config(font=bolded)

        dict_directory[song_name] = song


#   Remove Song Menu
def remove_song():
    global is_playing

    if is_playing == song_box.get(ACTIVE):
        pygame.mixer.music.stop()
        music_label.config(text='', bg=player_bg_color, fg=song_label_color)
        current_time.config(text='', bg=player_bg_color, fg=song_label_color)
        root.title('PyPlayer')

    song_to_erase = song_box.get(ACTIVE)
    imported_songs.remove(song_to_erase + '\n')
    song_box.delete(ANCHOR)

    dict_directory.pop(song_to_erase)


#   Remove all Songs of the Playlist
def remove_all_songs():
    try:
        pygame.mixer.music.stop()
    except AttributeError:
        pass
    music_label.config(text='', bg=player_bg_color, fg=song_label_color)
    current_time.config(text='', bg=player_bg_color, fg=song_label_color)
    root.title('PyPlayer')

    song_box.delete(0, END)
    imported_songs.clear()
    dict_directory.clear()


#   Get the current time of the playing song
def current_song_length():
    global song_total_length
    global stoped
    global slider_active

    song_box.activate(ACTIVE)
    song_box.select_set(ACTIVE, last=None)

    #   Get the current song time (on ms) and convert to sec
    current = pygame.mixer.music.get_pos() / 1000

    # Get the time converted to sec and put it on time format
    current_song_intime_format = time.strftime('%M:%S', time.gmtime(current))

    #   Set the font size
    font_size = font.Font(size='8')

    #   Get the total length of the current song
    total_song_current = song_box.curselection()
    music_name = song_box.get(total_song_current)
    current_song = f'C:/Users/{user_name}/Music/{music_name}.mp3'
    current_song_mp3 = MP3(current_song)
    song_total_length = current_song_mp3.info.length

    #   Update the Slider position
    if int(current) == int(slider.get()) + 1 or int(current) == 0:
        if is_paused is False:
            slider.config(to=int(song_total_length), value=int(current))
            #   Shows the current time on time format
            current_time.config(text=current_song_intime_format, bg=player_bg_color,
                                fg=song_label_color, font=font_size)
    #   Update the Slider position
    elif int(current) != int(slider.get()) + 1 and is_paused is False:
        if slider_active is True:
            slider_pos = slider.get()
            slider.config(to=int(song_total_length), value=int(slider_pos + 1))
            slider_pos_in_time = time.strftime('%M:%S', time.gmtime(int(slider_pos + 1)))
            current_time.config(text=slider_pos_in_time, bg=player_bg_color, fg=song_label_color, font=font_size)
        elif slider_active is False:
            slider.config(to=int(song_total_length), value=int(current))
            current_time.config(text=current_song_intime_format, bg=player_bg_color,
                                fg=song_label_color, font=font_size)

    #   Converting the total song length to time format
    length_converted_totime = time.strftime('%M:%S', time.gmtime(int(song_total_length)))

    #   Shows the total time
    total_song_time.config(text=length_converted_totime, bg=player_bg_color, fg=song_label_color, font=font_size)

    volume_label.config(text='', bg=player_bg_color, fg=song_label_color)
    repeat_label.config(text='', bg=player_bg_color, fg=song_label_color)

    if current >= song_total_length or current_song_intime_format >= length_converted_totime:
        if stoped is False:
            next_song(True)

    #   Repeat the song current time
    current_time.after(1000, current_song_length)


#   Slider function
def slider_function(x):
    global slider_active

    slider_active = True
    pygame.mixer.music.set_pos(int(slider.get()))


#   Stop Menu button
def stop():
    global stoped
    global slider_active

    slider_active = False

    pygame.mixer.music.stop()
    music_label.config(text='', bg=player_bg_color)
    current_time.config(text='', bg=player_bg_color)
    root.title('PyPlayer')

    stoped = True


#   Play song function
def play():
    global is_playing
    global is_paused
    global song_total_length
    global stoped
    global slider_active

    slider_active = False

    music_name = song_box.get(ACTIVE)

    pygame.mixer.music.load(dict_directory[music_name])
    pygame.mixer.music.play(loops=0)
    current_song_length()

    is_playing = music_name

    bolded = font.Font(weight='bold', size='10', underline=1)
    music_label.config(text=music_name, bg=player_bg_color, fg=song_label_color, font=bolded)

    is_paused = False
    root.title('PyPlayer - ' + music_name)

    pause_label.config(text='', bg=player_bg_color, fg=song_label_color)

    stoped = False


#   Next song button
def next_song(auto_next=False):
    global is_playing
    global is_paused
    global stoped

    #   Get the current song tuple number
    next = song_box.curselection()
    #   Add one to the current song
    next = next[0] + 1

    if repeat_loop == 4 and song_box.get(next) == '':
        #   Move selection bar
        song_box.select_clear(0, END)
        song_box.activate([0])
        song_box.select_set([0], last=None)
    elif repeat_loop == 5 and auto_next is True:
        song_box.select_clear(0, END)
        song_box.activate(next - 1)
        song_box.select_set(next - 1, last=None)
    else:
        #   Move selection bar
        song_box.select_clear(0, END)
        song_box.activate(next)
        song_box.select_set(next, last=None)

    play()


#   Forward song button
def back_song():
    global is_playing
    global is_paused
    global stoped

    #   Get the current song tuple number
    back = song_box.curselection()
    #   Add one to the current song
    back = back[0] - 1
    # Discover the nome of next song
    music_name = song_box.get(back)

    #   Move selection bar
    song_box.select_clear(0, END)
    song_box.activate(back)
    song_box.select_set(back, last=None)

    play()


#   Pause song function
def pause():
    global is_paused

    if is_paused is False:
        pygame.mixer.music.pause()
        is_paused = True
        pause_label.config(text='Paused', bg=player_bg_color, fg=song_label_color)

    elif is_paused is True:
        pygame.mixer.music.unpause()
        pause_label.config(text='', bg=player_bg_color, fg=song_label_color)
        is_paused = False


#   START OF THE PERSONALIZATION FUNCTIONS
#   START OF THE PERSONALIZATION FUNCTIONS
#   START OF THE PERSONALIZATION FUNCTIONS

#   Function to check if an color exist or not
def check_color(color):
    try:
        color = color.replace(' ', '')
        Color(color)
        # if everything goes fine then return True
        return True
    except ValueError:  # The color code was not found
        return False


#   Set the background player color
def bg_color_set():
    global input_tk
    global player_bg_color
    global button_bg
    global song_label_color

    try:

        #   Take the input of the color set window
        if check_color(input_tk.get()) is True:
            player_bg_color = input_tk.get()
            player_bg_color = player_bg_color.replace(' ', '')
        else:
            player_bg_color = 'white'

        new_window.destroy()

        #   Changing the colors
        root.config(background=player_bg_color)
        controls_frame.config(bg=player_bg_color)
        time_frame.config(bg=player_bg_color)
        volume_frame.config(bg=player_bg_color)
        volume_label.config(bg=player_bg_color)
        repeat_label.config(bg=player_bg_color)

        back_btn.config(bg=player_bg_color)
        next_btn.config(bg=player_bg_color)
        pause_btn.config(bg=player_bg_color)
        play_btn.config(bg=player_bg_color)

        plus_btn.config(bg=player_bg_color)
        less_btn.config(bg=player_bg_color)

        shuffle_btn.config(bg=player_bg_color)
        repeat_btn.config(bg=player_bg_color)

        button_bg = player_bg_color

        if player_bg_color == 'white':
            song_label_color = 'black'
            music_label.config(bg=player_bg_color, fg='black')
            pause_label.config(bg=player_bg_color, fg='black')

            current_time.config(bg=player_bg_color, fg='black')
            total_song_time.config(bg=player_bg_color, fg='black')

            btn_black_set()

        elif player_bg_color == 'black':
            music_label.config(bg=player_bg_color, fg='white')
            pause_label.config(bg=player_bg_color, fg='white')

            current_time.config(bg=player_bg_color, fg='white')
            total_song_time.config(bg=player_bg_color, fg='white')
            song_label_color = 'white'

            btn_white_set()

        music_label.config(bg=player_bg_color, fg=song_label_color)
        pause_label.config(bg=player_bg_color, fg=song_label_color)

        current_time.config(bg=player_bg_color, fg=song_label_color)
        total_song_time.config(bg=player_bg_color, fg=song_label_color)

        #   Configure the slider background color
        style.theme_use('alt')
        style.configure('MyStyle.Horizontal.TScale', background=player_bg_color, troughcolor=song_label_color,
                        lightcolor='black', darkcolor='black', bordercolor='black')
        slider.config(style='MyStyle.Horizontal.TScale')

    except:
        new_window.destroy()


# Change player background color
def bg_color():
    global player_bg_color
    global input_tk
    global new_window

    new_window = Toplevel(root)
    new_window.geometry('200x200')
    if check_color(player_bg_color) is True:
        new_window['bg'] = player_bg_color
    else:
        new_window['bg'] = 'white'

    my_label = Label(new_window, text="Write the name of the color \n"
                                      "or RGB color with the # \n"
                                      "to set the player background color", bg='gainsboro', fg='black')
    bolded = font.Font(weight='bold', size='8')  # will use the default font
    my_label.config(font=bolded)
    my_label.pack()

    input_tk = Entry(new_window, width=50, borderwidth=3, bg='gainsboro')
    input_tk.pack(pady=50)
    input_tk.insert(0, 'type the color or RGB code Here ')

    button = Button(new_window, text='Confirm', command=bg_color_set)
    button.pack()

    new_window.mainloop()


#   Set the letters colors
def letter_color_set():
    global letter_color

    try:

        #   Take the input od the color set window
        if check_color(input_tk.get()) is True:
            letter_color = input_tk.get()
            letter_color = letter_color.replace(' ', '')
        else:
            letter_color = '#fcb505'

        new_window.destroy()

        #   Changing the colors
        song_box.config(fg=letter_color)

    except:
        new_window.destroy()


#   Change the letters color
def lt_color():
    global letter_color
    global input_tk
    global new_window

    new_window = Toplevel(root)
    new_window.geometry('200x200')
    if check_color(player_bg_color) is True:
        new_window['bg'] = player_bg_color
    else:
        new_window['bg'] = 'white'

    my_label = Label(new_window, text="Write the name of the color \n"
                                      "or RGB color with the # \n"
                                      "to set the music name letters colors", bg='gainsboro', fg='black')
    bolded = font.Font(weight='bold', size='8')  # will use the default font
    my_label.config(font=bolded)
    my_label.pack()

    input_tk = Entry(new_window, width=50, borderwidth=3, bg='gainsboro')
    input_tk.pack(pady=50)
    input_tk.insert(0, 'type the color or RGB code Here ')

    button = Button(new_window, text='Confirm', command=letter_color_set)
    button.pack()

    new_window.mainloop()


def viewer_color_set():
    global playlist_viewer_color

    try:

        #   Take the input od the color set window
        if check_color(input_tk.get()) is True:
            playlist_viewer_color = input_tk.get()
            playlist_viewer_color = playlist_viewer_color.replace(' ', '')
        else:
            playlist_viewer_color = 'black'

        new_window.destroy()

        #   Changing the colors
        song_box.config(bg=playlist_viewer_color)

    except:
        new_window.destroy()


#   Change the letters color
def viewer_color():
    global letter_color
    global input_tk
    global new_window

    new_window = Toplevel(root)
    new_window.geometry('200x200')
    if check_color(player_bg_color) is True:
        new_window['bg'] = player_bg_color
    else:
        new_window['bg'] = 'white'

    my_label = Label(new_window, text="Write the name of the color \n"
                                      "or RGB color with the # \n"
                                      "to set the playlist viewer color", bg='gainsboro', fg='black')
    bolded = font.Font(weight='bold', size='8')  # will use the default font
    my_label.config(font=bolded)
    my_label.pack()

    input_tk = Entry(new_window, width=50, borderwidth=3, bg='gainsboro')
    input_tk.pack(pady=50)
    input_tk.insert(0, 'tipe the color or RGB code Here ')

    button = Button(new_window, text='Confirm', command=viewer_color_set)
    button.pack()

    new_window.mainloop()


#   Set the color od the selection bar
def bar_color_set():
    global playlist_bar_color

    try:

        #   Take the input od the color set window
        if check_color(input_tk.get()) is True:
            playlist_bar_color = input_tk.get()
            playlist_bar_color = playlist_bar_color.replace(' ', '')
        else:
            playlist_bar_color = 'white'

        new_window.destroy()

        #   Changing the colors
        song_box.config(selectbackground=playlist_bar_color)

    except:
        new_window.destroy()


#   Change the bar color
def bar_color():
    global playlist_bar_color
    global input_tk
    global new_window

    new_window = Toplevel(root)
    new_window.geometry('200x200')
    if check_color(player_bg_color) is True:
        new_window['bg'] = player_bg_color
    else:
        new_window['bg'] = 'white'

    my_label = Label(new_window, text="Write the name of the color \n"
                                      "or RGB color with the # \n"
                                      "to set the playlist bar color", bg='gainsboro', fg='black')
    bolded = font.Font(weight='bold', size='8')  # will use the default font
    my_label.config(font=bolded)
    my_label.pack()

    input_tk = Entry(new_window, width=50, borderwidth=3, bg='gainsboro')
    input_tk.pack(pady=50)
    input_tk.insert(0, 'tipe the color or RGB code Here ')

    button = Button(new_window, text='Confirm', command=bar_color_set)
    button.pack()

    new_window.mainloop()


#   Set the color od the selection bar
def slc_ltt_color_set():
    global select_letter_color

    try:

        #   Take the input od the color set window
        if check_color(input_tk.get()) is True:
            select_letter_color = input_tk.get()
            select_letter_color = select_letter_color.replace(' ', '')
        else:
            select_letter_color = 'black'

        new_window.destroy()

        #   Changing the colors
        song_box.config(selectforeground=select_letter_color)

    except:
        new_window.destroy()


#   Change the selected letter color
def slc_letter_color():
    global select_letter_color
    global input_tk
    global new_window

    new_window = Toplevel(root)
    new_window.geometry('200x200')
    if check_color(player_bg_color) is True:
        new_window['bg'] = player_bg_color
    else:
        new_window['bg'] = 'white'

    my_label = Label(new_window, text="Write the name of the color \n"
                                      "or RGB color with the # \n"
                                      "to set the selected letter color", bg='gainsboro', fg='black')
    bolded = font.Font(weight='bold', size='8')  # will use the default font
    my_label.config(font=bolded)
    my_label.pack()

    input_tk = Entry(new_window, width=50, borderwidth=3, bg='gainsboro')
    input_tk.pack(pady=50)
    input_tk.insert(0, 'tipe the color or RGB code Here ')

    button = Button(new_window, text='Confirm', command=slc_ltt_color_set)
    button.pack()

    new_window.mainloop()


#   Set the music info colors
def song_label_color_set():
    global song_label_color

    try:

        #   Take the input od the color set window
        if check_color(input_tk.get()) is True:
            song_label_color = input_tk.get()
            song_label_color = song_label_color.replace(' ', '')
        else:
            song_label = 'black'

        new_window.destroy()

        #   Changing the colors
        pause_label.config(fg=song_label_color)
        music_label.config(fg=song_label_color)
        total_song_time.config(fg=song_label_color)
        current_time.config(fg=song_label_color)

        #   Slider colors
        style.theme_use('alt')
        style.configure('MyStyle.Horizontal.TScale', background=player_bg_color, troughcolor=song_label_color,
                        lightcolor='black', darkcolor='black', bordercolor='black')
        slider.config(style='MyStyle.Horizontal.TScale')

    except:
        new_window.destroy()


#   Change the music info colors
def song_label_color_info():
    global input_tk
    global new_window

    new_window = Toplevel(root)
    new_window.geometry('200x200')
    if check_color(player_bg_color) is True:
        new_window['bg'] = player_bg_color
    else:
        new_window['bg'] = 'white'

    my_label = Label(new_window, text="Write the name of the color \n"
                                      "or RGB color with the # \n"
                                      "to set the music info colors", bg='gainsboro', fg='black')
    bolded = font.Font(weight='bold', size='8')  # will use the default font
    my_label.config(font=bolded)
    my_label.pack()

    input_tk = Entry(new_window, width=50, borderwidth=3, bg='gainsboro')
    input_tk.pack(pady=50)
    input_tk.insert(0, 'type the color or RGB code Here ')

    button = Button(new_window, text='Confirm', command=song_label_color_set)
    button.pack()

    new_window.mainloop()


#   Function to change the buttons colors to black
def btn_black_set():
    black_bnt = ImageTk.PhotoImage(Image.open("back.png"))
    back_btn.configure(image=black_bnt)
    back_btn.image = black_bnt

    black_bnt = ImageTk.PhotoImage(Image.open('play (1).png'))
    play_btn.configure(image=black_bnt)
    play_btn.photo = black_bnt

    black_bnt = ImageTk.PhotoImage(Image.open("next.png"))
    next_btn.configure(image=black_bnt)
    next_btn.image = black_bnt

    black_bnt = ImageTk.PhotoImage(Image.open("pause (1).png"))
    pause_btn.configure(image=black_bnt)
    pause_btn.image = black_bnt

    black_bnt = ImageTk.PhotoImage(Image.open("minus.png"))
    less_btn.configure(image=black_bnt)
    less_btn.image = black_bnt

    black_bnt = ImageTk.PhotoImage(Image.open("plus.png"))
    plus_btn.configure(image=black_bnt)
    plus_btn.image = black_bnt

    black_bnt = ImageTk.PhotoImage(Image.open("shuffle-black.png"))
    shuffle_btn.configure(image=black_bnt)
    shuffle_btn.image = black_bnt

    black_bnt = ImageTk.PhotoImage(Image.open("repeat.png"))
    repeat_btn.configure(image=black_bnt)
    repeat_btn.image = black_bnt


#   Function to change the buttons colors to white
def btn_white_set():
    white_bnt = ImageTk.PhotoImage(Image.open("white-back.png"))
    back_btn.configure(image=white_bnt)
    back_btn.image = white_bnt

    white_bnt = ImageTk.PhotoImage(Image.open("white-play.png"))
    play_btn.configure(image=white_bnt)
    play_btn.image = white_bnt

    white_bnt = ImageTk.PhotoImage(Image.open("white-next.png"))
    next_btn.configure(image=white_bnt)
    next_btn.image = white_bnt

    white_bnt = ImageTk.PhotoImage(Image.open("white-pause.png"))
    pause_btn.configure(image=white_bnt)
    pause_btn.image = white_bnt

    white_bnt = ImageTk.PhotoImage(Image.open("white-minus.png"))
    less_btn.configure(image=white_bnt)
    less_btn.image = white_bnt

    white_bnt = ImageTk.PhotoImage(Image.open("white-plus.png"))
    plus_btn.configure(image=white_bnt)
    plus_btn.image = white_bnt

    white_bnt = ImageTk.PhotoImage(Image.open("shuffle-white.png"))
    shuffle_btn.configure(image=white_bnt)
    shuffle_btn.image = white_bnt

    white_bnt = ImageTk.PhotoImage(Image.open("repeat-white.png"))
    repeat_btn.configure(image=white_bnt)
    repeat_btn.image = white_bnt


# Create the windows with the options to change buttons color
def bnt_color():
    global new_window

    new_window = Toplevel(root)
    new_window.geometry('200x200')
    if check_color(player_bg_color) is True and player_bg_color != 'black':
        new_window['bg'] = player_bg_color
    else:
        new_window['bg'] = 'white'

    my_label = Label(new_window, text="Chose the color you \n"
                                      "want for your buttons", fg='black')
    bolded = font.Font(weight='bold', size='8')  # will use the default font
    my_label.config(font=bolded)
    my_label.pack(pady=50)

    btn_frame = Frame(new_window, bg=player_bg_color, borderwidth=0)
    btn_frame.pack()

    black_button = Button(btn_frame, text='Black', command=btn_black_set)
    black_button.pack(side=LEFT)

    white_button = Button(btn_frame, text='White', command=btn_white_set)
    white_button.pack(side=RIGHT)

    new_window.mainloop()


#   END OF THE PERSONALIZATION FUNCTIONS
#   END OF THE PERSONALIZATION FUNCTIONS
#   END OF THE PERSONALIZATION FUNCTIONS


#   Plus volume function
def plus_volume():
    current_vol = round(pygame.mixer.music.get_volume(), 1)
    pygame.mixer.music.set_volume(current_vol)
    new_vol = current_vol + 0.1

    if new_vol <= 1.0:
        pygame.mixer.music.set_volume(new_vol)

        volume_label.config(text=int(new_vol * 100), bg=player_bg_color, fg=song_label_color)
    elif new_vol >= 1.0:
        volume_label.config(text=int(current_vol * 100), bg=player_bg_color, fg=song_label_color)


#   Less volume function
def less_volume():
    current_vol = round(pygame.mixer.music.get_volume(), 1)
    pygame.mixer.music.set_volume(current_vol)
    new_vol = current_vol - 0.1

    pygame.mixer.music.set_volume(new_vol)

    volume_label.config(text=int(new_vol * 100), bg=player_bg_color, fg=song_label_color)


#   Search and downloading the music from youtube
def search_and_down():
    global artist_input
    global music_name_input
    global new_window

    bolded = font.Font(weight='bold', size='10', underline=1)
    music_label.config(text='Downloading... ', bg=player_bg_color, fg=song_label_color, font=bolded)

    #   Getting the input write on the entry and replace the spaces for YouTube search style
    artist = artist_input.get().replace(' ', '+')
    music_name = music_name_input.get().replace(' ', '+')

    new_window.destroy()

    try:
        pygame.mixer.music.stop()
    except:
        pass

    #   Searching on YouTube
    ytb_search = urllib.request.urlopen(f'https://www.youtube.com/results?search_query={artist}+'
                                        f'{music_name + "+official+audio"}')
    #   Getting the results ids
    video_ids = re.findall(r'watch\?v=(\S{11})', ytb_search.read().decode())
    #   Full Url of the music to download
    music_url = f'https://www.youtube.com/watch?v={video_ids[0]}'

    #   Start the download
    stream = pytube.YouTube(url=music_url).streams.get_audio_only()
    filename = stream.title
    list_of_remove = ['(Official Video)', '[Official Audio]', '(Official Music Video)',
                      '[Official Music Video]', '[OFFICIAL VIDEO]', '(Áudio Oficial)', '(Audio Oficial)',
                      '(audio oficial)', '(Official Audio)']
    for name in list_of_remove:
        filename = filename.replace(name, '')

    stream.download(f'C:/Users/{user_name}/Music/', filename)

    #   Conversion
    clip = AudioFileClip(f'C:\\Users\\{user_name}\\Music\\' + filename)
    clip.write_audiofile(f'C:\\Users\\{user_name}\\Music\\' + filename + '.mp3')

    #   Delete .mp4
    os.remove(f'C:\\Users\\{user_name}\\Music\\' + filename)

    if filename + '\n' not in imported_songs:
        imported_songs.append(filename + '\n')
        song_box.insert(END, filename)

        dict_directory[filename] = f'C:\\Users\\{user_name}\\Music\\' + filename + '.mp3'

        #   Move selection bar
        song_box.select_clear(0, END)
        song_box.activate(END)
        song_box.select_set(END, last=None)

        play()


#   Download song window function
def download_window():
    global artist_input
    global music_name_input
    global new_window

    new_window = Toplevel(root)
    new_window.geometry('300x350')
    if check_color(player_bg_color) is True:
        new_window['bg'] = player_bg_color
    else:
        new_window['bg'] = 'white'

    #   Input frames
    label_input_frame = Frame(new_window, bg=player_bg_color)
    label_input_frame.pack(pady=50)
    #   Text
    my_label = Label(label_input_frame, text='Write the nome of the artist, band,\n or singer, and the music name',
                     bg='gainsboro', fg='black')
    bolded = font.Font(weight='bold', size='8')  # will use the default font
    my_label.config(font=bolded)
    #   Input artist place
    artist_input = Entry(label_input_frame, width=50, borderwidth=3, bg='gainsboro')
    artist_input.insert(0, 'Artist, Band or Singer nome')

    # Text 2
    label2 = Label(label_input_frame, text='Write the music name', bg='gainsboro', fg='black')
    my_label.config(font=bolded)
    #   Input music name place
    music_name_input = Entry(label_input_frame, width=50, borderwidth=3, bg='gainsboro')
    music_name_input.insert(0, 'Music Name')

    my_label.grid(row=0, column=0, pady=20)
    artist_input.grid(row=1, column=0)
    label2.grid(row=2, column=0, pady=20)
    music_name_input.grid(row=3, column=0)

    button = Button(new_window, text='Confirm', command=search_and_down)
    button.pack(pady=20)

    new_window.mainloop()


#   Shuffle function
def shuffle():
    global imported_songs

    #   Stop the player and clean the listbox before shuffle
    try:
        stop()
    except AttributeError:
        pass
    music_label.config(text='', bg=player_bg_color, fg=song_label_color)
    current_time.config(text='', bg=player_bg_color, fg=song_label_color)
    root.title('PyPlayer')
    song_box.delete(0, END)

    #   Receive the playlist and shuffle the songs order
    shuffle_playlist = imported_songs
    shuffle = random.shuffle(shuffle_playlist)

    for song in shuffle_playlist:
        sg = str(song).replace('\n', '')
        song_box.insert(END, sg)

    play()


#   Repeat function
def repeat():
    global repeat_loop
    if repeat_loop == 0:
        repeat_loop = 4
        repeat_label.config(text='Repeat PLAYLIST activated', bg=player_bg_color, fg=song_label_color)
    elif repeat_loop == 4:
        repeat_loop = 5
        repeat_label.config(text='Repeat SONG activated', bg=player_bg_color, fg=song_label_color)
    elif repeat_loop == 5:
        repeat_loop = 0
        repeat_label.config(text='Repeat DISABLED', bg=player_bg_color, fg=song_label_color)

    print(repeat_loop)


#   Playlist box
song_box = Listbox(root, bg=playlist_viewer_color, fg=letter_color, width=61,
                   selectbackground=playlist_bar_color, selectforeground=select_letter_color)
song_box.pack()

#   Insert the saved songs to the listbox
try:
    with open('save_songs.txt', 'r', encoding='utf-8', errors='ignore') as songs:

        music = songs.readlines()

        for song in music:
            sg = str(song).replace('\n', '')
            song_box.insert(END, sg)
            imported_songs.append(sg + '\n')
            #   Turning song box strings into bold
            bolded = font.Font(weight='bold', size='9')  # will use the default font
            song_box.config(font=bolded)

    with open('directory.json', 'r', encoding='utf-8', errors='ignore') as jfile:
        dict_directory = json.load(jfile)

except:
    pass

#   Music name label
music_label = Label(root, text='', bg=player_bg_color)
music_label.pack(pady=15)

#   Song length label
time_frame = LabelFrame(root, bg=player_bg_color, borderwidth=0)
time_frame.pack()

#   Create the song length slider
# Style and appearance  settings
style = ttk.Style()
style.theme_use('alt')
style.configure('MyStyle.Horizontal.TScale', background=player_bg_color, troughcolor=song_label_color,
                lightcolor='black', darkcolor='black', bordercolor='black')

# Slider
slider = ttk.Scale(time_frame, from_=0, to=100, orient=HORIZONTAL, value=0, length=275,
                   style='MyStyle.Horizontal.TScale', command=slider_function)

current_time = Label(time_frame, text='', bg=player_bg_color, borderwidth=0)
total_song_time = Label(time_frame, text='', bg=player_bg_color, borderwidth=0)

slider.grid(row=0, column=2, pady=5)
current_time.grid(row=0, column=0)
total_song_time.grid(row=0, column=4)

#   Volume label
volume_label = Label(root, text='', bg=player_bg_color)
volume_label.pack()

#   Pause label
pause_label = Label(root, text='', bg=player_bg_color)
pause_label.pack()

#   Player control buttons images
back_img = PhotoImage(file='back.png')
next_img = PhotoImage(file='next.png')
pause_img = PhotoImage(file='pause.png')
play_img = PhotoImage(file='play.png')

plus_vol = PhotoImage(file='plus.png')
less_vol = PhotoImage(file='minus.png')

shuffle_img = PhotoImage(file='shuffle-black.png')
repeat_img = PhotoImage(file='repeat.png')

#   Player control buttons frames
controls_frame = Frame(root, bg=player_bg_color)
controls_frame.pack()

#   Player control buttons
back_btn = Button(controls_frame, image=back_img, borderwidth=0, command=back_song, bg=player_bg_color)
pause_btn = Button(controls_frame, image=pause_img, borderwidth=0, command=pause, bg=player_bg_color)
play_btn = Button(controls_frame, image=play_img, borderwidth=0, command=play, bg=player_bg_color)
next_btn = Button(controls_frame, image=next_img, borderwidth=0, command=next_song, bg=player_bg_color)

#   Player control buttons position
back_btn.grid(row=0, column=0, padx=10)
pause_btn.grid(row=0, column=1, padx=10)
play_btn.grid(row=0, column=2, padx=10)
next_btn.grid(row=0, column=3, padx=10)

#   Player volume buttons frames
volume_frame = Frame(root, bg=player_bg_color)
volume_frame.pack()

#   Player volume buttons
plus_btn = Button(volume_frame, image=plus_vol, borderwidth=0, bg=player_bg_color, command=plus_volume)
less_btn = Button(volume_frame, image=less_vol, borderwidth=0, bg=player_bg_color, command=less_volume)

shuffle_btn = Button(volume_frame, image=shuffle_img, borderwidth=0, bg=player_bg_color, command=shuffle)
repeat_btn = Button(volume_frame, image=repeat_img, borderwidth=0, bg=player_bg_color, command=repeat)

#   Player volume buttons position
less_btn.grid(row=0, column=1, pady=30, padx=10)
plus_btn.grid(row=0, column=2, pady=30, padx=10)

shuffle_btn.grid(row=0, column=4, pady=30, padx=25)
repeat_btn.grid(row=0, column=0, pady=10, padx=25)

repeat_label = Label(root, text='', bg=player_bg_color)
repeat_label.pack()

#   Player Menu
my_menu = Menu(root)
root.config(menu=my_menu)

#   Create Add song(s) to the add song menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Song", menu=add_song_menu)
add_song_menu.add_command(label='Add one song to the playlist', command=add_song)
#   Add many songs menu
add_song_menu.add_command(label='Add many songs to the playlist', command=add_many_songs)
add_song_menu.add_command(label='Download new song', command=download_window)

#   Remove song menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Song", menu=remove_song_menu)
remove_song_menu.add_command(label='Remove one song to the playlist', command=remove_song)
#   Remove many songs menu
remove_song_menu.add_command(label='Remove all songs of the playlist', command=remove_all_songs)

#   Stop menu
my_menu.add_command(label='Stop', command=stop)

# Colors set menu
set_color_menu = Menu(my_menu)
my_menu.add_cascade(label='Colors', menu=set_color_menu)
set_color_menu.add_command(label='Background color', command=bg_color)
set_color_menu.add_command(label='Letters color', command=lt_color)
set_color_menu.add_command(label='Playlist Viewer color', command=viewer_color)
set_color_menu.add_command(label='Playlist Bar Color', command=bar_color)
set_color_menu.add_command(label='Selected letter color', command=slc_letter_color)
set_color_menu.add_command(label='song information color', command=song_label_color_info)

# Buttons colors set
btn_color_menu = Menu(my_menu)
my_menu.add_cascade(label='Buttons', menu=btn_color_menu)
btn_color_menu.add_command(label='Change color of buttons', command=bnt_color)

#   Change buttons color if initial color equal to black
if player_bg_color == 'black':
    btn_white_set()

root.mainloop()

#   Save songs that already have been imported
with open('save_songs.txt', 'w', encoding='utf-8', errors='ignore') as songs:
    for sg in imported_songs:
        songs.write(sg)

#   Saving color configurations
with open('theme.json', 'w', encoding='utf-8', errors='ignore') as theme_file:
    theme = {}

    theme['player_bg_color'] = player_bg_color
    theme['playlist_viewer_color'] = playlist_viewer_color
    theme['playlist_bar_color'] = playlist_bar_color
    theme['letter_color'] = letter_color
    theme['select_letter_color'] = select_letter_color
    theme['song_info_label'] = song_label_color

    json.dump(theme, theme_file)

with open('directory.json', 'w', encoding='utf-8', errors='ignore') as directory:
    json.dump(dict_directory, directory)
