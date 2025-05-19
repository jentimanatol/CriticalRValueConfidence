import tkinter as tk
from tkinter import messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from scipy.stats import t
import numpy as np

from PIL import Image, ImageTk
import os, sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

root = tk.Tk()

try:
    icon_path = resource_path("app_icon.png")  # PNG preferred
    icon_image = Image.open(icon_path)
    tk_icon = ImageTk.PhotoImage(icon_image)
    root.wm_iconphoto(True, tk_icon)
    print("✅ Icon set successfully.")
except Exception as e:
    print(f"⚠️ Could not set icon: {e}")
