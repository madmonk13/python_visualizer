"""
GUI Controls - Colors Section
"""

import tkinter as tk
from tkinter import ttk
from gui_config import PALETTE_OPTIONS


def create_section(parent, row, controls_panel):
    """Create the Colors section"""
    section = ttk.LabelFrame(parent, text="Colors", padding="10")
    section.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
    section.columnconfigure(0, weight=1)
    
    # Palette
    ttk.Label(section, text="Palette:").grid(row=0, column=0, sticky=tk.W, pady=2)
    palette_combo = ttk.Combobox(section, textvariable=controls_panel.palette_var, 
                                 state="readonly", width=18)
    palette_combo['values'] = PALETTE_OPTIONS
    palette_combo.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2)
    
    # Custom Palette
    ttk.Button(section, text="Custom Palette...", 
              command=controls_panel.callback.open_color_picker).grid(row=2, column=0, 
                                                                      sticky=(tk.W, tk.E), 
                                                                      pady=(5, 2))
    
    return section