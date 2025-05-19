"""
Example of using the icon_manager in your application

This shows how to implement the icon_manager module in your projects.
"""

import tkinter as tk
from tkinter import messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from scipy.stats import t
import numpy as np
import os
import sys

# Import our icon manager
from icon_manager import set_windows_app_id, set_app_icon

# Set Windows app ID BEFORE creating the Tk root window
set_windows_app_id("ajcodev.criticalrvalue.confidence.1.0")

# Create root window
root = tk.Tk()

# Set the application icon for both window title and taskbar
set_app_icon(root, "ajcodev.criticalrvalue.confidence.1.0", "app_icon")

# Continue with the rest of your application...
root.title("Critical r-value Calculator and Visualizer AJ")
root.geometry("1700x1000")

# ... Rest of your application code ...

# Start the application
root.mainloop()
