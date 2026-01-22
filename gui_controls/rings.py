"""
GUI Controls - Rings Section
"""

import tkinter as tk
from tkinter import ttk
from gui_config import (RING_SHAPE_OPTIONS, RING_COUNT_MIN, RING_COUNT_MAX, 
                       RING_SCALE_MIN, RING_SCALE_MAX, RING_STAGGER_OPTIONS,
                       RING_ROTATION_OPTIONS, ROTATION_SPEED_MIN, ROTATION_SPEED_MAX)


def create_section(parent, row, controls_panel):
    """Create the Rings section"""
    section = ttk.LabelFrame(parent, text="Rings", padding="10")
    section.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
    section.columnconfigure(0, weight=1)
    
    # On/Off
    ttk.Checkbutton(section, text="Show Rings", 
                   variable=controls_panel.rings_enabled_var).grid(row=0, column=0, 
                                                                   sticky=tk.W, pady=2)
    
    # Shape
    ttk.Label(section, text="Shape:").grid(row=1, column=0, sticky=tk.W, pady=(10, 2))
    ring_shape_combo = ttk.Combobox(section, textvariable=controls_panel.ring_shape_var, 
                                   state="readonly", width=18)
    ring_shape_combo['values'] = RING_SHAPE_OPTIONS
    ring_shape_combo.current(0)
    ring_shape_combo.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=2)
    
    # Quantity
    ttk.Label(section, text="Quantity:").grid(row=3, column=0, sticky=tk.W, pady=(10, 2))
    ring_count_frame = ttk.Frame(section)
    ring_count_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=2)
    ring_count_slider = ttk.Scale(ring_count_frame, from_=RING_COUNT_MIN, to=RING_COUNT_MAX, 
                                  variable=controls_panel.ring_count_var, 
                                  orient=tk.HORIZONTAL,
                                  command=lambda v: controls_panel.ring_count_var.set(int(float(v))))
    ring_count_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
    controls_panel.ring_count_label = ttk.Label(ring_count_frame, text="3", width=5)
    controls_panel.ring_count_label.pack(side=tk.LEFT)
    controls_panel.ring_count_var.trace_add('write', 
                                  lambda *args: controls_panel.ring_count_label.config(
                                      text=f"{controls_panel.ring_count_var.get()}"))
    
    # Scale
    ttk.Label(section, text="Scale:").grid(row=5, column=0, sticky=tk.W, pady=(10, 2))
    ring_scale_frame = ttk.Frame(section)
    ring_scale_frame.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=2)
    ring_scale_slider = ttk.Scale(ring_scale_frame, from_=RING_SCALE_MIN, to=RING_SCALE_MAX, 
                                  variable=controls_panel.ring_scale_var, orient=tk.HORIZONTAL)
    ring_scale_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
    controls_panel.ring_scale_label = ttk.Label(ring_scale_frame, text="1.0x", width=5)
    controls_panel.ring_scale_label.pack(side=tk.LEFT)
    controls_panel.ring_scale_var.trace_add('write', 
                                  lambda *args: controls_panel.ring_scale_label.config(
                                      text=f"{controls_panel.ring_scale_var.get():.1f}x"))
    
    # Stagger
    ttk.Label(section, text="Stagger:").grid(row=7, column=0, sticky=tk.W, pady=(10, 2))
    ring_stagger_combo = ttk.Combobox(section, textvariable=controls_panel.ring_stagger_var, 
                                     state="readonly", width=18)
    ring_stagger_combo['values'] = RING_STAGGER_OPTIONS
    ring_stagger_combo.current(0)
    ring_stagger_combo.grid(row=8, column=0, sticky=(tk.W, tk.E), pady=2)
    
    # Rotation Direction
    ttk.Label(section, text="Rotation Direction:").grid(row=9, column=0, sticky=tk.W, 
                                                        pady=(10, 2))
    ring_rot_combo = ttk.Combobox(section, textvariable=controls_panel.ring_rot_var, 
                                  state="readonly", width=18)
    ring_rot_combo['values'] = RING_ROTATION_OPTIONS
    ring_rot_combo.current(0)
    ring_rot_combo.grid(row=10, column=0, sticky=(tk.W, tk.E), pady=2)
    
    # Rotation Speed
    ttk.Label(section, text="Rotation Speed:").grid(row=11, column=0, sticky=tk.W, 
                                                    pady=(10, 2))
    ring_speed_frame = ttk.Frame(section)
    ring_speed_frame.grid(row=12, column=0, sticky=(tk.W, tk.E), pady=2)
    ring_speed_slider = ttk.Scale(ring_speed_frame, from_=ROTATION_SPEED_MIN, 
                                  to=ROTATION_SPEED_MAX, 
                                  variable=controls_panel.ring_rot_speed_var, 
                                  orient=tk.HORIZONTAL)
    ring_speed_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
    controls_panel.ring_speed_label = ttk.Label(ring_speed_frame, text="100%", width=5)
    controls_panel.ring_speed_label.pack(side=tk.LEFT)
    controls_panel.ring_rot_speed_var.trace_add('write', 
                          lambda *args: controls_panel.ring_speed_label.config(
                              text=f"{int(controls_panel.ring_rot_speed_var.get() * 100)}%"))
    
    return section