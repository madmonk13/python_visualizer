"""
GUI Controls - Starfield Section
"""

import tkinter as tk
from tkinter import ttk
from gui_config import STARFIELD_ROTATION_OPTIONS


def create_section(parent, row, controls_panel):
    """Create the Starfield section"""
    section = ttk.LabelFrame(parent, text="Starfield", padding="10")
    section.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
    section.columnconfigure(0, weight=1)
    
    # On/Off
    ttk.Checkbutton(section, text="Show Starfield", 
                   variable=controls_panel.starfield_enabled_var).grid(row=0, column=0, 
                                                                       sticky=tk.W, pady=2)
    
    # Rotation
    ttk.Label(section, text="Rotation:").grid(row=1, column=0, sticky=tk.W, pady=(10, 2))
    star_rot_combo = ttk.Combobox(section, textvariable=controls_panel.starfield_rot_var, 
                                  state="readonly", width=18)
    star_rot_combo['values'] = STARFIELD_ROTATION_OPTIONS
    star_rot_combo.current(0)
    star_rot_combo.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=2)
    
    return section