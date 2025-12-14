import pygame
import tkinter as tk
from tkinter import filedialog

# ================= INITIALIZE =================
pygame.mixer.init()

root = tk.Tk()
root.title("Neon Music Player ✨")
root.geometry("700x500")
root.config(bg="#0f0f1a")

# ================= TITLE =================
title_label = tk.Label(
    root,
    text="🎵 Coolest Music Player 🎵",
    font=("Helvetica", 24, "bold"),
    fg="#ff66ff",
    bg="#0f0f1a"
)
title_label.pack(pady=10)

# ================= PANEL =================
panel = tk.Frame(root, bg="#1a1a2e", bd=4, relief="ridge")
panel.pack(fill="both", expand=True, padx=20, pady=10)

# ================= SONG LABEL =================
song_label = tk.Label(
    panel,
    text="Load songs to begin",
    font=("Helvetica", 14),
    fg="white",
    bg="#1a1a2e"
)
song_label.pack(pady=5)

# ================= PLAYLIST =================
playlist = tk.Listbox(
    panel,
    font=("Helvetica", 12),
    bg="#0f0f1a",
    fg="white",
    selectbackground="#ff79c6",
    width=50,
    height=12
)
playlist.pack(pady=10)

songs = []
current_index = -1

# ================= FUNCTIONS =================
def load_songs():
    global songs, current_index
    files = filedialog.askopenfilenames(
        title="Select Songs (Max 50)",
        filetypes=[("Audio Files", "*.mp3 *.wav")]
    )
    if files:
        songs = list(files[:50])
        playlist.delete(0, tk.END)
        for song in songs:
            playlist.insert(tk.END, song.split("/")[-1])
        current_index = -1
        song_label.config(text="Songs loaded. Select one to play.")

def play_song():
    global current_index

    if not songs:
        song_label.config(text="⚠ Load songs first")
        return

    if not playlist.curselection():
        song_label.config(text="⚠ Select a song from playlist")
        return

    current_index = playlist.curselection()[0]
    pygame.mixer.music.load(songs[current_index])
    pygame.mixer.music.play()
    song_label.config(
        text="Playing: " + songs[current_index].split("/")[-1]
    )

def play_song_by_index():
    pygame.mixer.music.load(songs[current_index])
    pygame.mixer.music.play()
    playlist.selection_clear(0, tk.END)
    playlist.selection_set(current_index)
    song_label.config(
        text="Playing: " + songs[current_index].split("/")[-1]
    )

def stop_song():
    pygame.mixer.music.stop()
    song_label.config(text="Stopped")

def pause_song():
    pygame.mixer.music.pause()
    song_label.config(text="Paused")

def resume_song():
    pygame.mixer.music.unpause()
    song_label.config(text="Resumed")

def next_song():
    global current_index
    if not songs:
        return
    if current_index < len(songs) - 1:
        current_index += 1
        play_song_by_index()

def prev_song():
    global current_index
    if not songs:
        return
    if current_index > 0:
        current_index -= 1
        play_song_by_index()

# ================= NEON BUTTON =================
def neon_button(text, color, cmd):
    btn = tk.Label(
        panel,
        text=text,
        font=("Helvetica", 13, "bold"),
        bg="#1a1a2e",
        fg=color,
        bd=2,
        relief="ridge",
        width=14,
        height=2
    )
    btn.bind("<Button-1>", lambda e: cmd())
    btn.bind("<Enter>", lambda e: btn.config(bg="#2a2a40"))
    btn.bind("<Leave>", lambda e: btn.config(bg="#1a1a2e"))
    return btn

# ================= BUTTONS =================
btn_frame = tk.Frame(panel, bg="#1a1a2e")
btn_frame.pack(pady=10)

buttons = [
    neon_button("Load Songs", "#ff79c6", load_songs),
    neon_button("Play ▶", "#50fa7b", play_song),
    neon_button("Pause ⏸", "#f1fa8c", pause_song),
    neon_button("Resume ⏯", "#8be9fd", resume_song),
    neon_button("Stop ⏹", "#ff5555", stop_song),
    neon_button("Prev ⏮", "#bd93f9", prev_song),
    neon_button("Next ⏭", "#bd93f9", next_song),
]

for btn in buttons:
    btn.pack(side="left", padx=5)

root.mainloop()