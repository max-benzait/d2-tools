import tkinter as tk
from tkinter import messagebox
import shutil
import os
import platform
from dotenv import load_dotenv

load_dotenv()

# Detect the operating system
current_os = platform.system()

# Load paths from .env based on the detected OS
if current_os == "Darwin":  # macOS
    src_dir = os.getenv("MAC_SRC")
    dst_dir = os.getenv("MAC_DST")
    os_label = "macOS"
elif current_os == "Linux":  # Ubuntu
    src_dir = os.getenv("UBUNTU_SRC")
    dst_dir = os.getenv("UBUNTU_DST")
    os_label = "Ubuntu"
else:
    src_dir = dst_dir = ""
    os_label = "Unsupported OS"

def copy_files(src, dst, pattern):
    try:
        files_copied = []
        for file in os.listdir(src):
            if file.startswith(pattern):
                full_file_path = os.path.join(src, file)
                if os.path.isfile(full_file_path):
                    shutil.copy(full_file_path, dst)
                    files_copied.append(file)
        return files_copied
    except Exception as e:
        return str(e)

def dupe_to_saved():
    pattern = "Huitlilopochitl"
    files_copied = copy_files(src_dir, dst_dir, pattern)
    messagebox.showinfo("Duplication to Saved Games", f"Copied files: {files_copied}")

def dupe_to_desktop():
    pattern = "Huitlilopochitl"
    files_copied = copy_files(dst_dir, src_dir, pattern)
    messagebox.showinfo("Duplication to Desktop", f"Copied files: {files_copied}")

def clone_all_to_saved():
    try:
        shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)
        messagebox.showinfo("Clone to Saved Games", "All files cloned successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def clone_all_to_desktop():
    try:
        shutil.copytree(dst_dir, src_dir, dirs_exist_ok=True)
        messagebox.showinfo("Clone to Desktop", "All files cloned successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

app = tk.Tk()
app.title("File Duplication GUI")

# Display the detected OS
os_label_text = f"Operating System: {os_label}"
os_label_widget = tk.Label(app, text=os_label_text)
os_label_widget.pack(pady=10)

dupe_to_saved_btn = tk.Button(app, text="Dupe Items to Saved Games", command=dupe_to_saved)
dupe_to_saved_btn.pack(pady=10)

dupe_to_desktop_btn = tk.Button(app, text="Dupe Items to Desktop", command=dupe_to_desktop)
dupe_to_desktop_btn.pack(pady=10)

clone_all_to_saved_btn = tk.Button(app, text="Clone All to Saved Games", command=clone_all_to_saved)
clone_all_to_saved_btn.pack(pady=10)

clone_all_to_desktop_btn = tk.Button(app, text="Clone All to Desktop", command=clone_all_to_desktop)
clone_all_to_desktop_btn.pack(pady=10)

app.mainloop()
