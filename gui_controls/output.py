"""
GUI Controls - Output Section
"""

import tkinter as tk
from tkinter import ttk
from gui_config import RESOLUTION_OPTIONS, FPS_OPTIONS


def create_section(parent, row, controls_panel):
    """Create the Output section"""
    section = ttk.LabelFrame(parent, text="Output", padding="10")
    section.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
    section.columnconfigure(0, weight=1)
    
    # Resolution
    ttk.Label(section, text="Resolution:").grid(row=0, column=0, sticky=tk.W, pady=2)
    res_combo = ttk.Combobox(section, textvariable=controls_panel.resolution_var, 
                            state="readonly", width=18)
    res_combo['values'] = RESOLUTION_OPTIONS
    res_combo.current(0)
    res_combo.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2)
    
    # Frame Rate
    ttk.Label(section, text="Frame Rate:").grid(row=2, column=0, sticky=tk.W, pady=(10, 2))
    fps_combo = ttk.Combobox(section, textvariable=controls_panel.fps_var, 
                            state="readonly", width=18)
    fps_combo['values'] = FPS_OPTIONS
    fps_combo.current(1)
    fps_combo.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=2)
    
    return section