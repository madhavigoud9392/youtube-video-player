import tkinter as tk
from tkinter import messagebox
import pywhatkit as pwk
import socket
import os

HISTORY_FILE = "search_history.txt"

# --- Utility Functions ---
def check_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

def save_history(query):
    with open(HISTORY_FILE, "a") as f:
        f.write(query + "\n")

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        lines = f.readlines()
    return [line.strip() for line in lines][-5:]

def clear_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    update_history_list()
    messagebox.showinfo("Cleared", "Search history cleared.")

def update_history_list():
    history = load_history()
    history_listbox.delete(0, tk.END)
    for item in reversed(history):
        history_listbox.insert(tk.END, item)

# --- Main Feature ---
def play_video():
    video_name = entry.get().strip()

    if not check_internet():
        status_label.config(text="❌ No internet connection.", fg="red")
        return

    if not video_name:
        status_label.config(text="⚠️ Please enter a video name.", fg="orange")
        return

    try:
        status_label.config(text=f"🔍 Searching: {video_name}", fg="blue")
        pwk.playonyt(video_name)
        status_label.config(text="✅ Video opened in browser!", fg="green")
        save_history(video_name)
        update_history_list()
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")
        status_label.config(text="❌ Failed to play video.", fg="red")

# --- GUI Setup ---
root = tk.Tk()
root.title("🎬 YouTube Video Player")
root.geometry("500x400")
root.config(bg="#1e1e1e")  # dark background

# Title
title_label = tk.Label(root, text="YouTube Video Search", font=("Helvetica", 16, "bold"), fg="white", bg="#1e1e1e")
title_label.pack(pady=10)

# Search Entry
entry = tk.Entry(root, width=40, font=("Arial", 12), bg="#2b2b2b", fg="white", insertbackground="white")
entry.pack(pady=10)
entry.focus()

# Buttons Frame
button_frame = tk.Frame(root, bg="#1e1e1e")
button_frame.pack(pady=5)

search_button = tk.Button(button_frame, text="🔍 Search & Play", font=("Arial", 12), bg="#4CAF50", fg="white", command=play_video)
search_button.grid(row=0, column=0, padx=5)

clear_button = tk.Button(button_frame, text="🗑 Clear History", font=("Arial", 12), bg="#e53935", fg="white", command=clear_history)
clear_button.grid(row=0, column=1, padx=5)

# Status Label
status_label = tk.Label(root, text="", font=("Arial", 10), bg="#1e1e1e", fg="white")
status_label.pack(pady=10)

# Search History
history_label = tk.Label(root, text="📜 Recent Searches", font=("Arial", 12, "underline"), fg="lightgray", bg="#1e1e1e")
history_label.pack()

history_listbox = tk.Listbox(root, width=50, height=5, bg="#2b2b2b", fg="white", font=("Arial", 10))
history_listbox.pack(pady=5)

# Footer
footer_label = tk.Label(root, text="Built with Python + Tkinter + pywhatkit", font=("Arial", 9), fg="gray", bg="#1e1e1e")
footer_label.pack(side="bottom", pady=5)

update_history_list()

root.mainloop()
