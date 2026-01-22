"""
GUI Controls - Cover Options Section
"""

import tkinter as tk
from tkinter import ttk
from gui_config import (COVER_SIZE_MIN, COVER_SIZE_MAX, COVER_TIMELINE_OPTIONS)


def create_section(parent, row, controls_panel):
    """Create the Cover Options section"""
    section = ttk.LabelFrame(parent, text="Cover Options", padding="10")
    section.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
    section.columnconfigure(0, weight=1)
    
    # Shape
    ttk.Label(section, text="Shape:").grid(row=0, column=0, sticky=tk.W, pady=2)
    shape_frame = ttk.Frame(section)
    shape_frame.grid(row=1, column=0, sticky=tk.W, pady=2)
    ttk.Radiobutton(shape_frame, text="Square", variable=controls_panel.cover_shape_var, 
                   value="square").pack(side=tk.LEFT, padx=(0, 10))
    ttk.Radiobutton(shape_frame, text="Round", variable=controls_panel.cover_shape_var, 
                   value="round").pack(side=tk.LEFT)
    
    # Size
    ttk.Label(section, text="Size:").grid(row=2, column=0, sticky=tk.W, pady=(10, 2))
    cover_size_frame = ttk.Frame(section)
    cover_size_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=2)
    cover_size_slider = ttk.Scale(cover_size_frame, from_=COVER_SIZE_MIN, to=COVER_SIZE_MAX, 
                                  variable=controls_panel.cover_size_var, orient=tk.HORIZONTAL)
    cover_size_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
    controls_panel.cover_size_label = ttk.Label(cover_size_frame, text="1.0x", width=5)
    controls_panel.cover_size_label.pack(side=tk.LEFT)
    controls_panel.cover_size_var.trace_add('write', 
                                  lambda *args: controls_panel.cover_size_label.config(
                                      text=f"{controls_panel.cover_size_var.get():.1f}x"))
    
    # Animation
    ttk.Label(section, text="Animation:").grid(row=4, column=0, sticky=tk.W, pady=(10, 2))
    timeline_combo = ttk.Combobox(section, textvariable=controls_panel.cover_timeline_var, 
                                  state="readonly", width=18)
    timeline_combo['values'] = COVER_TIMELINE_OPTIONS
    timeline_combo.current(0)
    timeline_combo.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=2)
    
    # Static Option
    ttk.Checkbutton(section, text="Static (no music reaction)", 
                   variable=controls_panel.static_cover_var).grid(row=6, column=0, 
                                                                  sticky=tk.W, pady=(10, 2))
    
    return section