import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, Label, Entry, Button
from tkinter import ttk
import shutil
import os
import platform
from dotenv import load_dotenv
import subprocess

def update_app():
    subprocess.run(['python', 'update.py'])

update_app()

load_dotenv()

# Detect the operating system and set paths
current_os = platform.system()

if current_os == "Darwin":  # macOS
    dst_dir = os.path.expanduser("~/Library/Application Support/CrossOver/Bottles/Diablo II Resurrected/drive_c/users/crossover/Saved Games/Diablo II Resurrected")
    os_label = "macOS"
elif current_os == "Linux":  # Ubuntu
    dst_dir = os.path.expanduser("~/.local/share/Steam/steamapps/compatdata/2710268825/pfx/drive_c/users/steamuser/Saved Games/Diablo II Resurrected")
    os_label = "Ubuntu"
else:
    dst_dir = ""
    os_label = "Unsupported OS"

# Ensure SRC directories exist
src_base_dir = os.path.join(os.getcwd(), "characters")
if not os.path.exists(src_base_dir):
    os.makedirs(src_base_dir)

shared_src_dir = os.path.join(os.getcwd(), "shared")
if not os.path.exists(shared_src_dir):
    os.makedirs(shared_src_dir)

def autodetect_characters():
    characters = [f.split('.')[0] for f in os.listdir(dst_dir) if f.endswith('.d2s')]
    characters = list(set(characters))  # Remove duplicates
    character_var.set("Select Character")
    character_dropdown['menu'].delete(0, 'end')
    for character in characters:
        character_dropdown['menu'].add_command(label=character, command=tk._setit(character_var, character))
    messagebox.showinfo("Auto-detect", f"Detected characters: {', '.join(characters)}")

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

def version_file(file_path, version_dir, comment):
    if not os.path.exists(version_dir):
        os.makedirs(version_dir)
    version_number = len(os.listdir(version_dir)) + 1
    version_file = os.path.join(version_dir, f"version_{version_number}.bak")
    shutil.copy(file_path, version_file)
    with open(os.path.join(version_dir, f"version_{version_number}.txt"), 'w') as f:
        f.write(comment)
    return version_file

def dupe_to_saved():
    pattern = character_var.get()
    if pattern == "Select Character":
        messagebox.showwarning("No Character Selected", "Please select a character.")
        return
    src_dir = os.path.join(src_base_dir, pattern)
    if not os.path.exists(src_dir):
        os.makedirs(src_dir)
    files_copied = copy_files(src_dir, dst_dir, pattern)
    messagebox.showinfo("Duplication to Saved Games", f"Copied files: {files_copied}")

def dupe_to_desktop():
    pattern = character_var.get()
    if pattern == "Select Character":
        messagebox.showwarning("No Character Selected", "Please select a character.")
        return
    src_dir = os.path.join(src_base_dir, pattern)
    if not os.path.exists(src_dir):
        os.makedirs(src_dir)
    files_copied = copy_files(dst_dir, src_dir, pattern)
    messagebox.showinfo("Duplication to Desktop", f"Copied files: {files_copied}")

def clone_all_to_saved():
    try:
        shutil.copytree(shared_src_dir, dst_dir, dirs_exist_ok=True)
        messagebox.showinfo("Clone to Saved Games", "All files cloned successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def clone_all_to_desktop():
    try:
        shutil.copytree(dst_dir, shared_src_dir, dirs_exist_ok=True)
        messagebox.showinfo("Clone to Desktop", "All files cloned successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def version_shared_stash():
    comment = simpledialog.askstring("Input", "Enter version comment:")
    if comment:
        stash_file = os.path.join(dst_dir, "SharedStashSoftCoreV2.d2i")
        settings_file = os.path.join(dst_dir, "Settings.json")
        version_file(stash_file, os.path.join(shared_src_dir, "stash_versions"), comment)
        version_file(settings_file, os.path.join(shared_src_dir, "settings_versions"), comment)
        messagebox.showinfo("Versioning", "Versioning completed successfully.")

def open_env_editor():
    env_editor = Toplevel(app)
    env_editor.title("Edit .env Paths")

    def save_and_reload_env():
        with open(".env", "w") as f:
            f.write(f"MAC_SRC={mac_src_entry.get()}\n")
            f.write(f"MAC_DST={mac_dst_entry.get()}\n")
            f.write(f"UBUNTU_SRC={ubuntu_src_entry.get()}\n")
            f.write(f"UBUNTU_DST={ubuntu_dst_entry.get()}\n")
        load_dotenv()  # Reload the .env file
        messagebox.showinfo("Info", "Paths updated. Please restart the application for changes to take effect.")
        env_editor.destroy()

    Label(env_editor, text="MAC_SRC").grid(row=0, column=0, padx=10, pady=5)
    mac_src_entry = Entry(env_editor, width=50)
    mac_src_entry.grid(row=0, column=1, padx=10, pady=5)
    mac_src_entry.insert(0, os.getenv("MAC_SRC"))

    Label(env_editor, text="MAC_DST").grid(row=1, column=0, padx=10, pady=5)
    mac_dst_entry = Entry(env_editor, width=50)
    mac_dst_entry.grid(row=1, column=1, padx=10, pady=5)
    mac_dst_entry.insert(0, os.getenv("MAC_DST"))

    Label(env_editor, text="UBUNTU_SRC").grid(row=2, column=0, padx=10, pady=5)
    ubuntu_src_entry = Entry(env_editor, width=50)
    ubuntu_src_entry.grid(row=2, column=1, padx=10, pady=5)
    ubuntu_src_entry.insert(0, os.getenv("UBUNTU_SRC"))

    Label(env_editor, text="UBUNTU_DST").grid(row=3, column=0, padx=10, pady=5)
    ubuntu_dst_entry = Entry(env_editor, width=50)
    ubuntu_dst_entry.grid(row=3, column=1, padx=10, pady=5)
    ubuntu_dst_entry.insert(0, os.getenv("UBUNTU_DST"))

    save_button = Button(env_editor, text="Save and Reload", command=save_and_reload_env)
    save_button.grid(row=4, column=0, columnspan=2, pady=10)

app = tk.Tk()
app.title("File Duplication GUI")
style = ttk.Style()
style.theme_use('clam')  # Use a modern theme

# Display the detected OS
os_label_text = f"Operating System: {os_label}"
os_label_widget = ttk.Label(app, text=os_label_text)
os_label_widget.pack(pady=10)

# Add a button to open the .env editor
env_button = ttk.Button(app, text="⚙️", command=open_env_editor)
env_button.pack(side="top", anchor="nw")

character_var = tk.StringVar(app)
character_var.set("Select Character")
character_dropdown = ttk.OptionMenu(app, character_var, "Select Character")
character_dropdown.pack(pady=10)

autodetect_btn = ttk.Button(app, text="Autodetect Characters", command=autodetect_characters)
autodetect_btn.pack(pady=10)

dupe_to_saved_btn = ttk.Button(app, text="Dupe Items to D2R", command=dupe_to_saved)
dupe_to_saved_btn.pack(pady=10)

dupe_to_desktop_btn = ttk.Button(app, text="Dupe Items to d2-tools", command=dupe_to_desktop)
dupe_to_desktop_btn.pack(pady=10)

clone_all_to_saved_btn = ttk.Button(app, text="Clone All to D2R", command=clone_all_to_saved)
clone_all_to_saved_btn.pack(pady=10)

clone_all_to_desktop_btn = ttk.Button(app, text="Clone All d2-tools", command=clone_all_to_desktop)
clone_all_to_desktop_btn.pack(pady=10)

version_shared_btn = ttk.Button(app, text="Version Shared Stash and Settings", command=version_shared_stash)
version_shared_btn.pack(pady=10)

app.mainloop()
