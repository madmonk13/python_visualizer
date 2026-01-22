"""
GUI Controls - Text Section
"""

import tkinter as tk
from tkinter import ttk
from gui_config import (TEXT_SIZE_MIN, TEXT_SIZE_MAX, TEXT_HORIZONTAL_ALIGN_OPTIONS,
                       TEXT_VERTICAL_ALIGN_OPTIONS)


def create_section(parent, row, controls_panel):
    """Create the Text section"""
    section = ttk.LabelFrame(parent, text="Text", padding="10")
    section.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
    section.columnconfigure(0, weight=1)
    
    # Line 1
    ttk.Label(section, text="Line 1 (Optional):").grid(row=0, column=0, sticky=tk.W, pady=2)
    text_entry = ttk.Entry(section, textvariable=controls_panel.text_var, width=25)
    text_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2)
    
    # Line 2
    ttk.Label(section, text="Line 2 (Optional):").grid(row=2, column=0, sticky=tk.W, 
                                                       pady=(10, 2))
    text_entry2 = ttk.Entry(section, textvariable=controls_panel.text_var2, width=25)
    text_entry2.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=2)
    
    # Size
    ttk.Label(section, text="Size:").grid(row=4, column=0, sticky=tk.W, pady=(10, 2))
    text_size_frame = ttk.Frame(section)
    text_size_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=2)
    text_size_slider = ttk.Scale(text_size_frame, from_=TEXT_SIZE_MIN, to=TEXT_SIZE_MAX, 
                                 variable=controls_panel.text_size_var, orient=tk.HORIZONTAL)
    text_size_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
    controls_panel.text_size_label = ttk.Label(text_size_frame, text="1.0x", width=5)
    controls_panel.text_size_label.pack(side=tk.LEFT)
    controls_panel.text_size_var.trace_add('write', 
                                 lambda *args: controls_panel.text_size_label.config(
                                     text=f"{controls_panel.text_size_var.get():.1f}x"))
    
    # Horizontal Alignment
    ttk.Label(section, text="Horizontal Alignment:").grid(row=6, column=0, sticky=tk.W, 
                                                          pady=(10, 2))
    h_align_combo = ttk.Combobox(section, textvariable=controls_panel.text_h_align_var, 
                                 state="readonly", width=18)
    h_align_combo['values'] = TEXT_HORIZONTAL_ALIGN_OPTIONS
    h_align_combo.current(1)  # Center
    h_align_combo.grid(row=7, column=0, sticky=(tk.W, tk.E), pady=2)
    
    # Vertical Alignment
    ttk.Label(section, text="Vertical Alignment:").grid(row=8, column=0, sticky=tk.W, 
                                                        pady=(10, 2))
    v_align_combo = ttk.Combobox(section, textvariable=controls_panel.text_v_align_var, 
                                 state="readonly", width=18)
    v_align_combo['values'] = TEXT_VERTICAL_ALIGN_OPTIONS
    v_align_combo.current(2)  # Bottom
    v_align_combo.grid(row=9, column=0, sticky=(tk.W, tk.E), pady=2)
    
    return section