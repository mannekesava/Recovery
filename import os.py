import os
import shutil
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import win32com.client
import pythoncom
from send2trash import send2trash
import matplotlib.pyplot as plt
import psutil

def log_action(action):
    with open("file_recovery_log.txt", "a") as log_file:
        log_file.write(action + "\n")

def list_files():
    try:
        directory = filedialog.askdirectory(title="Select a Folder")
        if not directory:
            return

        if not os.path.exists(directory):
            messagebox.showerror("Error", f"Directory not found: {directory}")
            return

        files = "\n".join(os.listdir(directory))
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Files in {directory}:\n{files}")
        log_action(f"Listed files in {directory}")

    except Exception as e:
        messagebox.showerror("Error", f"Could not list files: {str(e)}")
        log_action(f"Error listing files: {str(e)}")

def show_storage_chart():
    drive = simpledialog.askstring("Input", "Enter Drive Letter (e.g., C):")
    if not drive:
        return

    usage = psutil.disk_usage(f"{drive}:/")
    labels = ["Used Space", "Free Space"]
    sizes = [usage.used, usage.free]
    colors = ["#e74c3c", "#2ecc71"]

    plt.figure(figsize=(5, 5))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, startangle=140)
    plt.title(f"Storage Usage of {drive} Drive")
    plt.show()
    log_action(f"Displayed storage chart for {drive} drive")

def check_disk():
    drive = simpledialog.askstring("Input", "Enter Drive Letter (e.g., C):")
    if drive:
        def run_chkdsk():
            try:
                subprocess.run([
                    "powershell", "-Command", "Start-Process", "cmd", "/k chkdsk", f"{drive}:", "-Verb", "RunAs"
                ], check=True)
                log_action(f"Checked disk {drive}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to check disk:\n{e}")
                log_action(f"Error checking disk {drive}: {str(e)}")
        threading.Thread(target=run_chkdsk, daemon=True).start()

def optimize_disk():
    drive = simpledialog.askstring("Input", "Enter Drive Letter (e.g., C):")
    if drive:
        def run_defrag():
            try:
                subprocess.run([
                    "powershell", "-Command", "Start-Process", "powershell", "-ArgumentList", 
                    f"'Optimize-Volume -DriveLetter {drive} -Verbose'", "-Verb", "RunAs"
                ], check=True)
                log_action(f"Optimized disk {drive}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to optimize disk:\n{e}")
                log_action(f"Error optimizing disk {drive}: {str(e)}")
        threading.Thread(target=run_defrag, daemon=True).start()

def simulate_disk_crash():
    messagebox.showwarning("Warning", "Simulating a disk crash! System recovery tools are recommended.")
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "⚠️ Simulated disk crash. Please proceed with recovery techniques.")
    log_action("Simulated disk crash")

def recover_files():
    messagebox.showinfo("Recovery", "Running recovery algorithms... (Simulation)")
    output_text.insert(tk.END, "✅ Recovery simulation complete. Files restored successfully.")
    log_action("Ran recovery simulation")

root = tk.Tk()
root.title("🗂 File System Recovery & Optimization")
root.geometry("800x550")
root.resizable(False, False)
root.configure(bg="#2C3F3F")

header = tk.Canvas(root, width=800, height=80, bg="#7289DA", highlightthickness=0)
header.create_rectangle(0, 0, 800, 80, fill="#7289DA")
header.create_text(400, 40, text="🗂 File System Recovery & Optimization", fill="white", font=("Arial", 16, "bold"))
header.pack()

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

def on_enter(e):
    ....    e.widget["background"] = "#999AAB"

def on_leave(e):
    e.widget["background"] = e.widget.default_color

buttons = [
    ("📂 List Files", list_files, "#3498db"),
    ("💾 Check Disk", check_disk, "#f39c12"),
    ("📊 Storage Chart", show_storage_chart, "#16a085"),
    ("⚙ Optimize Disk", optimize_disk, "#e74c3c"),
    ("💥 Simulate Disk Crash", simulate_disk_crash, "#c0392b"),
    ("♻ Recover Files", recover_files, "#27ae60")
]

for i, (text, cmd, color) in enumerate(buttons):
    row, col = divmod(i, 2)
    btn = tk.Button(button_frame, text=text, command=cmd, font=("Arial", 11, "bold"),
                    bg=color, fg="white", width=25, height=2, relief="flat")
    btn.default_color = color
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.grid(row=row, column=col, padx=10, pady=5)

output_frame = tk.Frame(root)
output_frame.pack(pady=15, fill="both", expand=True)

output_text = tk.Text(output_frame, height=10, width=90, font=("Arial", 11), bg="#23272A", fg="white", wrap="word")
output_text.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(output_frame, command=output_text.yview)
scrollbar.pack(side="right", fill="y")
output_text.config(yscrollcommand=scrollbar.set)

root.mainloop()
