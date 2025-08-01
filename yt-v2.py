import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

# 🔧 Replace this with your full path to ffmpeg.exe
FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"  # Example path

def download_video():
    url = url_var.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube link.")
        return

    folder = filedialog.askdirectory(title="Choose Download Folder")
    if not folder:
        return

    quality = quality_var.get()
    audio_only = mp3_var.get()

    try:
        # Safe output filename template (avoids crashes)
        output_template = os.path.join(folder, "%(title).100s.%(ext)s")

        if audio_only:
            cmd = [
                'yt-dlp',
                '-f', 'bestaudio',
                '--extract-audio',
                '--audio-format', 'mp3',
                '--no-mtime',
                '--no-playlist',
                '--ffmpeg-location', FFMPEG_PATH,
                '-o', output_template,
                url
            ]
        else:
            format_code = {
                'Best': 'bv*+ba/best',
                '2160p': 'bestvideo[height<=1440]+bestaudio/best',
                '1440p': 'bestvideo[height<=1440]+bestaudio/best',
                '1080p': 'bestvideo[height<=1080]+bestaudio/best',
                '720p': 'bestvideo[height<=720]+bestaudio/best',
                '480p': 'bestvideo[height<=480]+bestaudio/best'
            }.get(quality, 'bv*+ba/best')

            cmd = [
                'yt-dlp',
                '-f', format_code,
                '--merge-output-format', 'mp4',
                '--no-mtime',
                '--no-playlist',
                '--ffmpeg-location', FFMPEG_PATH,
                '-o', output_template,
                url
            ]

        subprocess.run(cmd, check=True)
        messagebox.showinfo("Success", "Download completed successfully!")

    except Exception as e:
        messagebox.showerror("Download Error", str(e))

# GUI setup
root = tk.Tk()
root.title("YouTube Downloader (yt-dlp)")
root.geometry("520x300")

url_var = tk.StringVar()
quality_var = tk.StringVar(value="Best")
mp3_var = tk.BooleanVar()

tk.Label(root, text="YouTube Downloader", font=("Arial", 18)).pack(pady=10)
tk.Entry(root, textvariable=url_var, width=60).pack(pady=5)

tk.Label(root, text="Select Quality:").pack(pady=5)
tk.OptionMenu(root, quality_var, "Best","2160p","1440p", "1080p", "720p", "480p").pack()

tk.Checkbutton(root, text="Download as MP3 (Audio only)", variable=mp3_var).pack(pady=5)

tk.Button(root, text="Download", font=("Arial", 14), bg="green", fg="white",
          command=download_video).pack(pady=20)

root.mainloop()
