import tkinter as tk
from tkinter import messagebox
from pytube import YouTube
import pygame
from moviepy.editor import *
import audioplayer



class MusicPlayer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PyPlayer")
        self.current_song = None
        self.player = None

        self.create_widgets()

    def create_widgets(self):
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=10)

        self.url_label = tk.Label(self.input_frame, text="URL do vídeo:")
        self.url_label.pack(side="left")

        self.url_entry = tk.Entry(self.input_frame, width=40)
        self.url_entry.pack(side="left")

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.play_button = tk.Button(self.button_frame, text="Play", command=self.play_music)
        self.play_button.pack(side="left")

        self.pause_button = tk.Button(self.button_frame, text="Pause", command=self.pause_music)
        self.pause_button.pack(side="left")

        self.next_button = tk.Button(self.button_frame, text="Next", command=self.next_music)
        self.next_button.pack(side="left")

        self.back_button = tk.Button(self.button_frame, text="Back", command=self.back_music)
        self.back_button.pack(side="left")

        self.slider = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_slider)
        self.slider.pack(pady=10)

        self.root.mainloop()

    def play_music(self):
        url = self.url_entry.get()
        if url:
            try:
                self.current_song = url
                youtube = YouTube(url)
                audio_stream = youtube.streams.filter(only_audio=True).first()
                filename = audio_stream.title+'.mp3'

                audio_stream.download(output_path=".", filename=filename)

                # pygame.mixer.music.load(filename=filename)
                # pygame.mixer.music.play()

                audioplayer.AudioPlayer("08 Slash - Anastasia.mp4").play(block=False)

                audio_duration = VideoFileClip("08 Slash - Anastasia.mp4").duration
                self.slider.config(to=audio_duration)
                self.slider.set(0)
            except Exception as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showwarning("Aviso", "Insira a URL do vídeo!")

    def pause_music(self):
        if self.player:
            self.player.pause()

    def next_music(self):
        messagebox.showinfo("Aviso", "Função Next não implementada!")

    def back_music(self):
        messagebox.showinfo("Aviso", "Função Back não implementada!")

    def update_slider(self, value):
        pass  # Implemente a função de atualização do slider aqui

# Iniciar o player de música
music_player = MusicPlayer()