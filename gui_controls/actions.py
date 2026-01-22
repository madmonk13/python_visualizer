"""
GUI Controls - Action Buttons Section
"""

import tkinter as tk
from tkinter import ttk


def create_section(parent, row, controls_panel):
    """Create the Action Buttons section"""
    print(f"DEBUG: actions.create_section() called at row {row}")
    print(f"DEBUG: parent = {parent}")
    print(f"DEBUG: controls_panel = {controls_panel}")
    
    # Check if buttons already exist
    if hasattr(controls_panel, 'preview_btn'):
        print(f"DEBUG: WARNING - preview_btn already exists!")
        return  # Don't create buttons again
    
    button_frame = ttk.Frame(parent)
    button_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
    button_frame.columnconfigure(0, weight=1)
    
    print(f"DEBUG: Creating Update Preview button")
    # Update Preview
    controls_panel.preview_btn = ttk.Button(button_frame, text="Update Preview", 
                                  command=controls_panel.callback.update_preview)
    controls_panel.preview_btn.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
    
    print(f"DEBUG: Creating Render 30s button")
    # Render 30s Preview Video
    controls_panel.quick_render_btn = ttk.Button(button_frame, text="Render 30s Preview Video", 
                                       command=controls_panel.callback.render_quick_preview)
    controls_panel.quick_render_btn.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
    
    print(f"DEBUG: Creating Render Full button")
    # Render Full Video
    controls_panel.render_btn = ttk.Button(button_frame, text="Render Full Video", 
                                 command=controls_panel.callback.render_video)
    controls_panel.render_btn.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
    
    # Progress section (hidden by default) - DON'T grid it yet
    controls_panel.progress_frame = ttk.Frame(button_frame)
    controls_panel.progress_frame.columnconfigure(0, weight=1)
    controls_panel.progress_label = ttk.Label(controls_panel.progress_frame, text="", 
                                   font=('TkDefaultFont', 9))
    controls_panel.progress_label.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 2))
    controls_panel.progress_bar = ttk.Progressbar(controls_panel.progress_frame, 
                                       mode='determinate', 
                                       maximum=100)
    controls_panel.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
    
    # Cancel button (also hidden by default) - DON'T grid it yet
    controls_panel.cancel_btn = ttk.Button(button_frame, text="Cancel Render", 
                                 command=controls_panel.callback.cancel_render)
    
    print(f"DEBUG: Finished creating action buttons")
    
    return button_frame