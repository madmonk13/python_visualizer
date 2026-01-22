"""
GUI Controls - Waveforms Section
"""

import tkinter as tk
from tkinter import ttk
from gui_config import (WAVEFORM_ROTATION_OPTIONS, ROTATION_SPEED_MIN, ROTATION_SPEED_MAX)


def create_section(parent, row, controls_panel):
    """Create the Waveforms section"""
    section = ttk.LabelFrame(parent, text="Waveforms", padding="10")
    section.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
    section.columnconfigure(0, weight=1)
    
    # Orientation
    ttk.Label(section, text="Orientation:").grid(row=0, column=0, sticky=tk.W, pady=2)
    wf_orient_frame = ttk.Frame(section)
    wf_orient_frame.grid(row=1, column=0, sticky=tk.W, pady=2)
    ttk.Radiobutton(wf_orient_frame, text="Horizontal", 
                   variable=controls_panel.waveform_orientation_var, 
                   value="horizontal").pack(side=tk.LEFT, padx=(0, 10))
    ttk.Radiobutton(wf_orient_frame, text="Vertical", 
                   variable=controls_panel.waveform_orientation_var, 
                   value="vertical").pack(side=tk.LEFT)
    
    # Rotation Direction
    ttk.Label(section, text="Rotation Direction:").grid(row=2, column=0, sticky=tk.W, 
                                                        pady=(10, 2))
    wf_rot_combo = ttk.Combobox(section, textvariable=controls_panel.waveform_rot_var, 
                                state="readonly", width=18)
    wf_rot_combo['values'] = WAVEFORM_ROTATION_OPTIONS
    wf_rot_combo.current(0)
    wf_rot_combo.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=2)
    
    # Rotation Speed
    ttk.Label(section, text="Rotation Speed:").grid(row=4, column=0, sticky=tk.W, 
                                                    pady=(10, 2))
    wf_speed_frame = ttk.Frame(section)
    wf_speed_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=2)
    wf_speed_slider = ttk.Scale(wf_speed_frame, from_=ROTATION_SPEED_MIN, 
                                to=ROTATION_SPEED_MAX, 
                                variable=controls_panel.waveform_rot_speed_var, 
                                orient=tk.HORIZONTAL)
    wf_speed_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
    controls_panel.waveform_speed_label = ttk.Label(wf_speed_frame, text="100%", width=5)
    controls_panel.waveform_speed_label.pack(side=tk.LEFT)
    controls_panel.waveform_rot_speed_var.trace_add('write', 
                          lambda *args: controls_panel.waveform_speed_label.config(
                              text=f"{int(controls_panel.waveform_rot_speed_var.get() * 100)}%"))
    
    return section