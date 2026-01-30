"""
GUI Controls - Starfield Section
Creates starfield effect controls
"""

import tkinter as tk
from tkinter import ttk
from gui_config import *


def create_section(parent, row, panel):
    """Create the starfield controls section"""
    section_frame = ttk.LabelFrame(parent, text="Starfield", padding="5")
    section_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
    section_frame.columnconfigure(1, weight=1)
    
    # Enable/Disable
    panel.starfield_enabled_var = tk.BooleanVar(value=True)
    starfield_check = ttk.Checkbutton(
        section_frame,
        text="Enable Starfield",
        variable=panel.starfield_enabled_var,
        command=panel.callback.preview_dirty
    )
    starfield_check.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
    
    # Starfield Rotation
    ttk.Label(section_frame, text="Rotation:").grid(row=1, column=0, sticky=tk.W, pady=2)
    panel.starfield_rot_var = tk.StringVar(value=DEFAULT_STARFIELD_ROTATION)
    starfield_rot_combo = ttk.Combobox(
        section_frame,
        textvariable=panel.starfield_rot_var,
        values=STARFIELD_ROTATION_OPTIONS,
        state='readonly',
        width=20
    )
    starfield_rot_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)
    starfield_rot_combo.bind('<<ComboboxSelected>>', lambda e: panel.callback.preview_dirty())
    
    # Starfield Direction
    ttk.Label(section_frame, text="Direction:").grid(row=2, column=0, sticky=tk.W, pady=2)
    panel.starfield_direction_var = tk.StringVar(value=DEFAULT_STARFIELD_DIRECTION)
    starfield_direction_combo = ttk.Combobox(
        section_frame,
        textvariable=panel.starfield_direction_var,
        values=STARFIELD_DIRECTION_OPTIONS,
        state='readonly',
        width=20
    )
    starfield_direction_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2)
    starfield_direction_combo.bind('<<ComboboxSelected>>', lambda e: panel.callback.preview_dirty())