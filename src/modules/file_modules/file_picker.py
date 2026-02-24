import tkinter as tk
from tkinter import filedialog

def file_picker() -> str | bool:
    """
    Open a file dialog (window) and return the selected file path

    Returns:
        str | bool: Selected file path or False if cancelled.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main Tk window
    path = filedialog.askopenfilename(
        title="Select the usernames list file",
        filetypes=[("Text Files", "*.txt")],
        initialdir= "outputs/"  # Default directory
    )
    return path or False  # Returns False if cancelled

