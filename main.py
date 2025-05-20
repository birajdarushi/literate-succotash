import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import yt_dlp
import os

def download_audio():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return

    # Ask user where to save the file
    output_dir = filedialog.askdirectory(title="Select Download Folder")
    if not output_dir:
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [progress_hook],
    }

    def run_download():
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            messagebox.showinfo("Success", "Download complete!")
        except Exception as e:
            messagebox.showerror("Error", f"Download failed: {e}")

    threading.Thread(target=run_download).start()

def progress_hook(d):
    if d['status'] == 'downloading':
        status_var.set(f"Downloading: {d['_percent_str']} at {d['_speed_str']}")
    elif d['status'] == 'finished':
        status_var.set("Converting to mp3...")

def paste_url():
    try:
        url = root.clipboard_get()
        url_entry.delete(0, tk.END)
        url_entry.insert(0, url)
    except:
        pass

# GUI setup
root = tk.Tk()
root.title("YouTube to MP3 Downloader")
root.geometry("400x180")
root.resizable(False, False)

tk.Label(root, text="YouTube URL:").pack(pady=(20, 5))
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

paste_btn = tk.Button(root, text="Paste", command=paste_url)
paste_btn.pack(pady=5)

download_btn = tk.Button(root, text="Download MP3", command=download_audio)
download_btn.pack(pady=10)

status_var = tk.StringVar()
status_label = tk.Label(root, textvariable=status_var, fg="blue")
status_label.pack(pady=5)

# Bind keyboard shortcuts
root.bind('<Control-v>', lambda e: paste_url())
root.bind('<Command-v>', lambda e: paste_url())

root.mainloop() 
