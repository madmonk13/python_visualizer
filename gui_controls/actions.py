"""
GUI Controls - Actions Section
Creates action buttons and live preview checkbox
"""

import tkinter as tk
from tkinter import ttk
from gui_config import *


def create_section(parent, row, panel):
    """Create the actions section with buttons and live preview checkbox"""
    
    # Update Preview button
    panel.preview_btn = ttk.Button(
        parent,
        text="Update Preview",
        command=panel.callback.update_preview
    )
    panel.preview_btn.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
    
    # Render 30s Preview button
    panel.quick_render_btn = ttk.Button(
        parent,
        text="Render 30s Preview",
        command=panel.callback.render_quick_preview
    )
    panel.quick_render_btn.grid(row=row+1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
    
    # Render Full Video button
    panel.render_btn = ttk.Button(
        parent,
        text="Render Full Video",
        command=panel.callback.render_video
    )
    panel.render_btn.grid(row=row+2, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
    
    # Live Preview Checkbox (can be toggled during render)
    panel.live_preview_var = tk.BooleanVar(value=False)
    panel.live_preview_check = ttk.Checkbutton(
        parent,
        text="Live preview during render",
        variable=panel.live_preview_var
    )
    panel.live_preview_check.grid(row=row+3, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
    
    # Progress section (hidden initially)
    panel.progress_frame = ttk.Frame(parent)
    panel.progress_frame.columnconfigure(0, weight=1)
    
    panel.progress_bar = ttk.Progressbar(
        panel.progress_frame, 
        mode='determinate', 
        maximum=100,
        length=250
    )
    panel.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=2)
    
    panel.progress_label = ttk.Label(
        panel.progress_frame, 
        text="",
        wraplength=250,
        justify=tk.LEFT
    )
    panel.progress_label.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(2, 0))
    
    # Cancel button (hidden initially)
    panel.cancel_btn = ttk.Button(
        parent,
        text="Cancel Render",
        command=panel.callback.cancel_render
    )
    
    # Note: progress_frame and cancel_btn are created but not grid()ed initially
    # They will be shown/hidden by the RenderManager using grid()/grid_forget()