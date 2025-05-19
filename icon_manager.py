"""
icon_manager.py - Reusable module for properly setting application icons in Tkinter applications
for both window title and Windows taskbar

Usage:
    1. Place this file in your project
    2. Import the set_app_icon function
    3. Call it with your Tk root window and app ID
    
Example:
    import tkinter as tk
    from icon_manager import set_app_icon
    
    root = tk.Tk()
    set_app_icon(root, "mycompany.myapp.version1.0")
    
    # Continue with your application...
    root.mainloop()
"""

import os
import sys
import tkinter as tk


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def set_windows_app_id(app_id):
    """Set the Windows AppUserModelID for taskbar icon grouping"""
    if os.name == 'nt':  # Windows systems only
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
            return True
        except Exception as e:
            print(f"Warning: Could not set AppUserModelID: {e}")
            return False
    return False


def set_app_icon(root, app_id, icon_name="app_icon"):
    """
    Set the application icon for both window title and taskbar
    
    Parameters:
        root (tk.Tk): The root Tkinter window
        app_id (str): Application ID for Windows taskbar grouping (e.g., "company.app.version")
        icon_name (str): Base name of icon files without extension (default: "app_icon")
                         Looks for both .ico and .png versions
    
    Returns:
        bool: True if at least one icon-setting method succeeded
    """
    # Find the icon paths
    ico_path = resource_path(f"{icon_name}.ico")
    png_path = resource_path(f"{icon_name}.png")
    
    # Track success of various methods
    success = False
    
    # Try all methods for maximum compatibility
    try:
        # For most windows (title bar)
        if os.path.exists(ico_path):
            root.iconbitmap(default=ico_path)
            success = True
    except Exception as e:
        print(f"Warning: Could not set icon with iconbitmap(default=): {e}")
    
    try:
        # For Windows taskbar
        if os.path.exists(ico_path):
            root.iconbitmap(ico_path)
            success = True
    except Exception as e:
        print(f"Warning: Could not set icon with iconbitmap(): {e}")
    
    try:
        # Another method for taskbar
        if os.path.exists(ico_path):
            root.wm_iconbitmap(ico_path)
            success = True
    except Exception as e:
        print(f"Warning: Could not set icon with wm_iconbitmap(): {e}")
    
    # Try PhotoImage method (works better with PNG)
    try:
        # Determine which image file to use
        img_path = png_path if os.path.exists(png_path) else ico_path
        if os.path.exists(img_path):
            img = tk.PhotoImage(file=img_path)
            root.iconphoto(True, img)
            success = True
    except Exception as e:
        print(f"Warning: Could not set icon with iconphoto(): {e}")
    
    # Try tk call method
    try:
        img_path = png_path if os.path.exists(png_path) else ico_path
        if os.path.exists(img_path):
            root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file=img_path))
            success = True
    except Exception as e:
        print(f"Warning: Could not set icon with tk.call(): {e}")
    
    return success
